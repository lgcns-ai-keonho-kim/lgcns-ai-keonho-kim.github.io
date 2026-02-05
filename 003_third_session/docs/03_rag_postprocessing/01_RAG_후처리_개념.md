# 01. RAG 후처리 개념

## 이 챕터에서 배우는 것

- RAG 후처리의 역할과 위치
- 메타데이터가 있는 경우의 후처리 흐름
- 여러 데이터 소스를 병합할 때의 후처리 구조
- LLM 기반 Reranker와 비-LLM Reranker의 차이
- 후처리 설계를 위한 슈도 코드 패턴

---

## 1. RAG 후처리란?

RAG 후처리는 **검색 결과를 생성 단계에 넣기 전에 정제하는 과정**입니다.
검색 결과는 항상 노이즈를 포함하므로, **정확도/일관성/안전성**을 확보하기 위해 필수입니다.

---

## 2. 후처리의 큰 목표

- **정확도 향상**: 관련 없는 문서 제거
- **중복 제거**: 동일/유사 문서 통합
- **일관성 확보**: 다양한 출처의 품질 편차 완화
- **안전성 강화**: 민감/정책 위반 문서 제거

---

## 3. 메타데이터가 있는 경우의 후처리

메타데이터가 있는 경우, 후처리는 단순 점수 기준이 아니라
**정책/권한/버전 기준을 우선 적용**해야 합니다.

```python
"""
목적: 메타데이터 정책을 우선 적용하는 후처리 흐름을 보여준다.
설명: 권한/언어/버전 필터를 먼저 적용하고 재정렬한다.
디자인 패턴: Pipeline
"""

def filter_by_access(docs: list[dict], level: str) -> list[dict]:
    """권한 필터를 적용한다."""
    return [d for d in docs if d.get("metadata", {}).get("access_level") == level]


def filter_by_language(docs: list[dict], language: str) -> list[dict]:
    """언어 필터를 적용한다."""
    return [d for d in docs if d.get("metadata", {}).get("language") == language]


def filter_by_version(docs: list[dict], min_version: int) -> list[dict]:
    """버전 기준 필터를 적용한다."""
    return [d for d in docs if d.get("metadata", {}).get("version", 0) >= min_version]


def postprocess_with_metadata(
    docs: list[dict],
    access_level: str,
    language: str,
    min_version: int,
) -> list[dict]:
    """메타데이터 우선 후처리 흐름."""
    docs = filter_by_access(docs, access_level)
    docs = filter_by_language(docs, language)
    docs = filter_by_version(docs, min_version)
    docs = rerank(docs)  # 실제 구현에서는 Reranker 적용
    return docs
```

---

## 4. 여러 데이터 소스를 병합할 때의 후처리

여러 검색 소스(벡터/키워드/하이브리드)를 병합할 때는 **정규화와 다양성 확보**가 핵심입니다.
아래 예시의 `rerank`는 **개념 함수**이며 실제 구현에서는 별도 Reranker가 필요합니다.
또한 점수 스케일이 다르면 **거리 → 유사도 변환** 등 사전 변환을 먼저 수행해야 합니다.

```python
"""
목적: 다중 소스 결과를 정규화하고 병합한다.
설명: 점수 정규화 → 중복 제거 → 다양성 확보 → 재정렬 순서로 처리한다.
디자인 패턴: Pipeline
"""

def normalize_scores(docs: list[dict]) -> list[dict]:
    """점수를 0~1 범위로 정규화한다."""
    scores = [d.get("score", 0.0) for d in docs]
    if not scores:
        return docs
    min_v, max_v = min(scores), max(scores)
    if min_v == max_v:
        return [{**d, "score": 1.0} for d in docs]
    normalized = []
    for d in docs:
        normalized.append(
            {**d, "score": (d.get("score", 0.0) - min_v) / (max_v - min_v)}
        )
    return normalized


def deduplicate_by_source_id(docs: list[dict]) -> list[dict]:
    """source_id 기준으로 중복을 제거한다."""
    seen: set[str] = set()
    result = []
    for d in docs:
        source_id = d.get("metadata", {}).get("source_id", "")
        if source_id and source_id in seen:
            continue
        if source_id:
            seen.add(source_id)
        result.append(d)
    return result
```

> 중복 제거 기준은 **청크 단위**인지 **문서 단위**인지 먼저 정해야 합니다.  
> 서비스 목적에 따라 기준이 달라질 수 있습니다.

```python
def diversify_by_source(docs: list[dict], max_per_source: int = 2) -> list[dict]:
    """출처별 문서 수를 제한해 다양성을 확보한다."""
    counts: dict[str, int] = {}
    result = []
    for d in docs:
        source_id = d.get("metadata", {}).get("source_id", "unknown")
        counts[source_id] = counts.get(source_id, 0)
        if counts[source_id] >= max_per_source:
            continue
        counts[source_id] += 1
        result.append(d)
    return result


def merge_multi_sources(docs_from_sources: list[list[dict]]) -> list[dict]:
    """다중 소스 후처리 흐름."""
    docs = [d for group in docs_from_sources for d in group]
    docs = normalize_scores(docs)
    docs = deduplicate_by_source_id(docs)
    docs = diversify_by_source(docs)
    docs = rerank(docs)  # 실제 구현에서는 Reranker 적용
    return docs
```

---

## 5. Reranker 유형 비교

### 1) LLM 기반 Reranker

- 문맥 이해력이 높아 정밀도가 높음
- 비용과 지연 시간이 증가

```python
"""
목적: LLM 기반 재정렬 흐름을 개념적으로 표현한다.
설명: 문서별 점수를 계산해 정렬한다.
디자인 패턴: Strategy
"""

def llm_score(question: str, doc: dict) -> float:
    """LLM 점수를 계산한다."""
    return float(doc.get("score", 0.0))


def llm_rerank(question: str, docs: list[dict], top_k: int = 5) -> list[dict]:
    """LLM 점수 기반으로 재정렬한다."""
    scored = [(llm_score(question, d), d) for d in docs]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for score, d in scored[:top_k]]
```

### 2) 비-LLM Reranker (Cross-Encoder 등)

- 빠르고 비용이 낮음
- 도메인 적응은 제한될 수 있음

```python
"""
목적: Cross-Encoder 기반 재정렬 흐름을 개념적으로 표현한다.
설명: 비교 모델 점수로 정렬한다.
디자인 패턴: Strategy
"""

def cross_encoder_score(question: str, doc: dict) -> float:
    """Cross-Encoder 점수를 계산한다."""
    return float(doc.get("score", 0.0))


def cross_encoder_rerank(question: str, docs: list[dict], top_k: int = 5) -> list[dict]:
    """Cross-Encoder 점수 기반으로 재정렬한다."""
    scored = [(cross_encoder_score(question, d), d) for d in docs]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for score, d in scored[:top_k]]
```

---

## 6. 후처리 단계의 표준 패턴(슈도 코드)

```python
"""
목적: 표준 후처리 파이프라인의 개념 흐름을 보여준다.
설명: 정책 필터 → 중복 제거 → 재정렬 → 압축 순서로 처리한다.
디자인 패턴: Pipeline
"""

def apply_policy_filters(docs: list[dict]) -> list[dict]:
    """정책 필터를 적용한다."""
    return docs


def remove_duplicates(docs: list[dict]) -> list[dict]:
    """중복 문서를 제거한다."""
    return docs


def rerank(docs: list[dict]) -> list[dict]:
    """재정렬을 수행한다."""
    return docs


def compress_context(docs: list[dict], limit: int = 5) -> list[dict]:
    """컨텍스트 길이를 제한한다."""
    return docs[:limit]


def postprocess_pipeline(question: str, docs: list[dict]) -> list[dict]:
    """표준 후처리 파이프라인."""
    docs = apply_policy_filters(docs)
    docs = remove_duplicates(docs)
    docs = rerank(docs)
    docs = compress_context(docs)
    return docs
```

---

## 7. 체크리스트

- 후처리 단계의 목적이 명확한가?
- 메타데이터 정책이 우선 적용되는가?
- 다중 소스 병합 시 정규화 전략이 있는가?
- Reranker 선택 기준이 정의되어 있는가?
