# 05. 메타데이터 기반 PGVector 활용

## 이 챕터에서 배우는 것

- LangChain에서 메타데이터를 포함해 PGVector를 사용하는 흐름
- 필터 조건을 안전하게 적용하는 방법
- 서비스 설계 시 반드시 고려할 메타데이터 전략

---

## 1. 왜 메타데이터가 중요한가?

PGVector는 벡터 검색이 핵심이지만, **메타데이터 필터가 품질과 보안을 결정**합니다.
특히 서비스에서는 아래 기준이 필수입니다.

- **권한 기반 제한**: 내부 문서 노출 방지
- **도메인 구분**: 정책/가이드/FAQ 분리
- **언어/지역**: 사용자 언어에 맞는 문서 선택

---

## 2. LangChain + PGVector 기본 흐름

LangChain에서는 `PGVectorStore`를 통해 문서 저장과 검색을 수행합니다.
이때 `Document.metadata`에 필터링에 필요한 정보를 넣는 것이 핵심입니다.

```python
"""
목적: 메타데이터를 포함한 문서를 PGVector에 저장한다.
설명: metadata 필드에 필터링 조건을 담는다.
디자인 패턴: Repository
"""

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGEngine, PGVectorStore


engine = PGEngine.from_connection_string(
    url="postgresql+psycopg://langchain:langchain@localhost:5432/langchain"
)
engine.init_vectorstore_table(table_name="documents", vector_size=1536)

store = PGVectorStore.create_sync(
    engine=engine,
    table_name="documents",
    embedding_service=OpenAIEmbeddings(model="text-embedding-3-small"),
)

docs = [
    Document(
        page_content="환불 정책 안내",
        metadata={"category": "policy", "access_level": "internal", "language": "ko"},
    ),
    Document(
        page_content="결제 실패 대응 가이드",
        metadata={"category": "guide", "access_level": "internal", "language": "ko"},
    ),
]

store.add_documents(docs)
```

---

## 3. 메타데이터 필터 적용 예시

검색 시 `filter` 인자를 사용해 메타데이터 조건을 적용합니다.
벡터 스토어(vector store)마다 지원하는 필터 문법이 다를 수 있으므로 **간단한 equality 조건부터 시작**하는 것이 안전합니다.

> 주의: 아래 `filter` 문법은 **개념 예시**입니다.  
> 실제 문법은 **벡터 스토어(vector store)/버전**에 따라 다르므로 반드시 공식 문서를 확인하세요.

```python
"""
목적: 메타데이터 필터를 적용해 검색한다.
설명: category와 language 조건을 동시에 적용한다.
디자인 패턴: Facade
"""

results = store.similarity_search(
    "환불 절차가 궁금합니다",
    k=5,
    filter={"category": "policy", "language": "ko"},
)
```

---

## 4. 필터 설계 전략(실무 기준)

- **필수 필터 먼저 정의**: 권한/언어/조직 등
- **불변 속성 중심**: 변하지 않는 필드가 안정적
- **필터 과도 제한 금지**: 결과가 비면 RAG 품질이 급격히 하락
- **도메인별 분리**: 카테고리/제품 라인을 명확히 구분

---

## 5. 복합 조건(AND/OR) 설계 팁

복합 필터는 **조건을 과하게 조합하면 결과가 비어버리는 문제**가 자주 발생합니다.
따라서 다음 원칙을 권장합니다.

- **필수 조건은 AND**로 고정한다(권한, 언어)
- **선택 조건은 OR**로 유연하게 묶는다(태그, 제품)
- OR 그룹이 많아지면 **최소 하나만 만족**하도록 제한한다

### 간단 예시

```python
"""
목적: 필수 조건과 선택 조건을 구분해 필터를 구성한다.
설명: AND로 고정할 조건과 OR로 묶을 조건을 분리한다.
디자인 패턴: Builder
"""

def build_filter(access_level: str, language: str, tags: list[str]) -> dict:
    """필수/선택 조건을 분리해 필터를 구성한다."""
    return {
        "$and": [
            {"access_level": {"$eq": access_level}},
            {"language": {"$eq": language}},
            {"$or": [{"tags": {"$contains": tag}} for tag in tags]},
        ]
    }
```

---

## 6. LLM 기반 필터 식별과 자동 적용(전략)

사용자 질문에서 **메타데이터 기반 필터를 자동 추론**해 적용하는 전략도 가능합니다.
핵심은 LLM이 **허용된 값 목록** 안에서만 선택하도록 만드는 것입니다.

### 1) 전략 개요

1) 테이블에서 **메타데이터 키/유니크 값 목록**을 조회한다  
2) LLM에게 질문과 허용 목록을 함께 제공한다  
3) LLM이 선택한 필터를 **검증**한다  
4) 검증된 값으로 메타데이터 필터를 구성한다  

### 2) 유효 메타데이터 키 조회(개념 코드)

```python
"""
목적: 테이블에서 유효한 메타데이터 키 목록을 조회한다.
설명: DISTINCT 결과를 LLM 프롬프트에 전달한다.
디자인 패턴: Repository
"""

import psycopg


def fetch_metadata_keys(dsn: str, table_name: str = "documents") -> list[str]:
    """유효 메타데이터 키 목록을 조회한다."""
    sql = f"SELECT DISTINCT jsonb_object_keys(metadata) FROM {table_name}"
    with psycopg.connect(dsn) as conn:
        rows = conn.execute(sql).fetchall()
    return [r[0] for r in rows if r[0]]
```

### 3) LLM 선택 결과 검증(개념 코드)

```python
"""
목적: LLM이 선택한 메타데이터 키를 안전하게 검증한다.
설명: 허용 목록에 없는 값은 무시한다.
디자인 패턴: Policy
"""

def validate_metadata_key(predicted: str, allowed: list[str]) -> str | None:
    """허용된 메타데이터 키만 통과시킨다."""
    if predicted in allowed:
        return predicted
    return None
```

### 4) 적용 시 주의사항

- **허용 목록 기반**으로만 필터를 구성해야 안전하다  
- LLM 출력은 반드시 검증하고 **폴백 경로**를 마련한다  
- 허용 목록이 자주 바뀌면 **캐시/갱신 정책**이 필요하다  

### 5) 캐시/갱신 전략(권장)

- **주기적 스냅샷**: 하루 1회 등 고정 주기로 키/값 목록 저장  
- **이벤트 기반 갱신**: 메타데이터 변경 이벤트 발생 시 즉시 갱신  
- **TTL 캐시**: 조회 비용이 큰 경우 1~6시간 TTL을 두고 재계산  

### 6) 메타데이터 키 조회(Repository 예시)

아래 코드는 **JSONB 메타데이터 키의 유니크 값**을 수집해
`{ "<column_name>": {"type": <data_type>, "unique_values": [...] } }`
형태로 반환하는 예시입니다.

```python
"""
목적: 메타데이터 키와 유니크 값을 조회해 LLM 입력으로 제공한다.
설명: 허용된 키만 조회하고, 유니크 값은 제한된 개수만 가져온다.
디자인 패턴: Repository
"""

from dataclasses import dataclass, field
from typing import Any
from psycopg import sql
import psycopg


@dataclass(frozen=True)
class MetadataSpec:
    """메타데이터(JSONB) 조회 설정."""

    column: str = "metadata"
    key_limit: int = 20
    value_limit: int = 50
    allow_keys: list[str] = field(default_factory=list)


class MetadataRepository:
    """메타데이터 정보를 조회하는 저장소."""

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn

    def fetch_metadata_info(
        self,
        table_name: str,
        spec: MetadataSpec,
    ) -> dict[str, dict[str, Any]]:
        """메타데이터(JSONB) 키와 유니크 값을 조회한다."""
        schema: dict[str, dict[str, Any]] = {}
        with psycopg.connect(self._dsn) as conn:
            if spec.allow_keys:
                keys = spec.allow_keys
            else:
                key_query = sql.SQL(
                    "SELECT DISTINCT jsonb_object_keys({col}) FROM {table} LIMIT %s"
                ).format(
                    col=sql.Identifier(spec.column),
                    table=sql.Identifier(table_name),
                )
                rows = conn.execute(key_query, (spec.key_limit,)).fetchall()
                keys = [r[0] for r in rows if r[0]]

            for key in keys:
                value_query = sql.SQL(
                    "SELECT DISTINCT {col} ->> %s FROM {table} "
                    "WHERE {col} ? %s LIMIT %s"
                ).format(
                    col=sql.Identifier(spec.column),
                    table=sql.Identifier(table_name),
                )
                rows = conn.execute(
                    value_query,
                    (key, key, spec.value_limit),
                ).fetchall()
                schema[key] = {
                    "type": "jsonb",
                    "unique_values": [r[0] for r in rows if r[0] is not None],
                }
        return schema
```

**실무 팁**

- LLM 컨텍스트를 위해 **유니크 값 개수는 제한**해야 합니다.
- 자주 쓰는 필터 컬럼은 **물리 컬럼으로 분리**하면 조회/관리 모두 쉬워집니다.
- 메타데이터 키는 **허용 목록(allowlist)**을 두는 것이 가장 안전합니다.
- 대용량에서는 DISTINCT 조회가 무거우므로 **배치 스냅샷/캐시**를 병행하세요.

---

## 7. 간단 프롬프트 템플릿(메타데이터/유니크 값 기반)

LLM에게는 **메타데이터 키와 유니크 값 목록 안에서만** 선택하도록 지시해야 합니다.
아래는 최소한의 프롬프트 템플릿 예시입니다.

```text
너는 필터 생성기다.
다음 메타데이터 키/유니크 값 목록만 사용해서 필터를 만들어라.
메타데이터: {metadata_info}
질문: {query}
출력은 JSON 형식만 허용한다.
형식: {"filters": {"<column_name>": "<allowed_value>"}}
허용 목록 밖의 값이 없으면 {"filters": {}}를 반환하라.
```

---

## 8. 예시 (메타데이터/유니크 값 + 재시도)

아래 예시는 **LLM이 메타데이터/유니크 값 기반으로 필터를 제안**하고,
허용 목록 밖이면 **최대 3번 재시도**하는 흐름을 LangGraph로 표현한 개념 코드입니다.

```python
"""
목적: 메타데이터/유니크 값 기반 필터 생성 그래프를 구성한다.
설명: LLM 제안 → 검증 → 재시도 → 필터 적용 → 검색 순서로 진행된다.
디자인 패턴: State Machine
"""

from dataclasses import dataclass, field
from typing import Any
from langgraph.graph import StateGraph, END


@dataclass
class State:
    """그래프 상태."""

    query: str
    metadata_info: dict[str, dict[str, Any]]
    filters: dict[str, str] = field(default_factory=dict)
    retry_count: int = 0


def fetch_metadata_info() -> dict[str, dict[str, Any]]:
    """메타데이터 키와 유니크 값 목록을 반환한다."""
    return {
        "category": {"type": "text", "unique_values": ["policy", "guide", "faq"]},
        "language": {"type": "text", "unique_values": ["ko", "en"]},
        "access_level": {"type": "text", "unique_values": ["public", "internal"]},
    }


def llm_pick_filters(query: str, metadata_info: dict[str, dict[str, Any]]) -> dict[str, str]:
    """LLM이 필터를 제안한다."""
    return {"category": "policy", "language": "ko"}


def propose_filters(state: State) -> State:
    """LLM으로 필터를 제안한다."""
    filters = llm_pick_filters(state.query, state.metadata_info)
    return State(
        query=state.query,
        metadata_info=state.metadata_info,
        filters=filters,
        retry_count=state.retry_count,
    )


def validate_filters(state: State) -> State:
    """허용 목록 기준으로 필터를 검증한다."""
    valid: dict[str, str] = {}
    for column, value in state.filters.items():
        allowed = state.metadata_info.get(column, {}).get("unique_values", [])
        if value in allowed:
            valid[column] = value
    return State(
        query=state.query,
        metadata_info=state.metadata_info,
        filters=valid,
        retry_count=state.retry_count,
    )


def need_retry(state: State) -> bool:
    """재시도가 필요한지 판단한다."""
    if state.filters:
        return False
    return state.retry_count < 3


def inc_retry(state: State) -> State:
    """재시도 횟수를 증가시킨다."""
    return State(
        query=state.query,
        metadata_info=state.metadata_info,
        filters=state.filters,
        retry_count=state.retry_count + 1,
    )


def build_safe_filter(state: State) -> dict[str, str]:
    """필터가 없으면 안전한 기본 필터를 적용한다."""
    if state.filters:
        return state.filters
    return {"access_level": "public"}


def retrieve(state: State) -> list[dict]:
    """필터를 적용해 검색한다."""
    filters = build_safe_filter(state)
    return [{"content": "샘플 문서", "filters": filters}]


def build_graph() -> StateGraph:
    """LangGraph를 구성한다."""
    graph = StateGraph(State)
    graph.add_node("propose", propose_filters)
    graph.add_node("validate", validate_filters)
    graph.add_node("inc_retry", inc_retry)
    graph.add_node("retrieve", retrieve)

    graph.set_entry_point("propose")
    graph.add_edge("propose", "validate")
    graph.add_conditional_edges(
        "validate",
        need_retry,
        {True: "inc_retry", False: "retrieve"},
    )
    graph.add_edge("inc_retry", "propose")
    graph.add_edge("retrieve", END)
    return graph
```

---

## 9. 흔한 실수

- 메타데이터를 일관되게 넣지 않아 필터가 무의미해짐
- 필터 기준이 변경되었는데 기존 문서를 재색인하지 않음
- 필터를 과도하게 걸어 검색 결과가 비어버림

---

## 10. 체크리스트

- 메타데이터 필드가 표준화되어 있는가?
- 필터가 권한 기준을 강제하는가?
- 필터가 검색 품질을 지나치게 떨어뜨리지 않는가?
- 필터 조건 변경 시 재색인 전략이 있는가?
