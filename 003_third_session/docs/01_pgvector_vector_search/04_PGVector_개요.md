# 04. PGVector 개요

## 이 챕터에서 배우는 것

- PGVector의 역할과 도입 이유
- 구성 요소를 요소별로 이해하는 방법
- 테이블 스키마의 각 컬럼이 의미하는 바
- 인덱스/연산자/옵스 클래스 선택 기준
- HNSW 파라미터와 성능 튜닝 포인트
- 청크 전략 설계 기준과 실무 체크포인트

---

## 1. PGVector란?

PGVector는 PostgreSQL에 **벡터 타입과 유사도 검색 기능**을 추가하는 확장입니다.
전용 벡터 DB를 별도로 운영하지 않아도, **기존 SQL 환경에서 임베딩 검색**을 할 수 있습니다.

---

## 2. 주니어를 위한 용어 설명

- **임베딩(Embedding)**: 텍스트를 숫자 벡터로 변환한 값
- **벡터(Vector)**: 여러 숫자로 이루어진 한 묶음 데이터
- **차원(Dimension)**: 벡터가 가진 숫자의 개수
- **유사도(Similarity)**: 두 벡터가 얼마나 비슷한지 나타내는 값
- **거리(Distance)**: 두 벡터가 얼마나 떨어져 있는지 나타내는 값
- **연산자(Operator)**: SQL에서 계산을 수행하는 기호(<=> 등)
- **옵스 클래스(Ops Class)**: 인덱스가 어떤 계산 규칙을 사용할지 정하는 규칙
- **메타데이터(Metadata)**: 문서의 속성 정보(카테고리, 권한, 언어 등)

---

## 3. 구성 요소를 요소별로 보기

PGVector는 아래 요소가 합쳐져서 동작합니다. 각각을 **따로 이해**하는 것이 중요합니다.

### 1) 확장(Extension)

- PostgreSQL에 벡터 타입과 연산자를 추가하는 플러그인
- 설치/활성화가 되어야 `vector` 타입을 쓸 수 있음

```sql
-- 목적: 벡터 타입과 연산자를 활성화한다.
CREATE EXTENSION IF NOT EXISTS vector;
```

### 2) 벡터 타입(Vector Type)

- `vector(n)` 형태로 차원 수를 명시
- **모델 차원과 정확히 일치**해야 함

```sql
-- 목적: 1536차원 임베딩을 저장한다.
embedding VECTOR(1536) NOT NULL
```

### 3) 거리/유사도 연산자

- `<->` : L2 거리(유클리드)
- `<=>` : 코사인 거리
- `<#>` : 내적 기반 거리

> 실무에서 가장 많이 쓰는 것은 **코사인 거리(<=>)** 입니다.

### 4) 옵스 클래스(Ops Class)

옵스 클래스는 **인덱스가 어떤 거리 계산을 기준으로 동작할지**를 정합니다.
연산자와 옵스 클래스가 일치하지 않으면 **인덱스가 무시되거나** 결과 해석이 꼬일 수 있습니다.

- `vector_l2_ops`  → `<->`와 함께 사용
- `vector_cosine_ops` → `<=>`와 함께 사용
- `vector_ip_ops` → `<#>`와 함께 사용

```sql
-- 목적: 코사인 거리 기준 인덱스를 만든다.
CREATE INDEX idx_documents_embedding
ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

**설계 체크포인트**

- 연산자/옵스 클래스/평가 기준을 **하나로 통일**해야 함
- 코사인 거리 기준이면 **쿼리도 <=>로 통일**해야 함

### 5) 인덱스(Index)

검색 속도와 비용을 결정하는 핵심 요소입니다.

- **IVFFlat**: 빠르지만 튜닝 필요
- **HNSW**: 정확도 우수, 메모리 사용 증가

### 6) 메타데이터(JSONB)

- 필터링/권한/버전 관리를 위한 속성 정보
- **검색 정확도와 운영 정책**에 큰 영향

---

## 4. 테이블 스키마 요소별 설명

아래는 실무에서 자주 쓰는 최소 확장 스키마입니다.

```sql
-- 목적: 문서 내용, 임베딩, 메타데이터를 함께 관리한다.
CREATE TABLE documents (
  id BIGSERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  embedding VECTOR(1536) NOT NULL,
  metadata JSONB NOT NULL,
  source_id TEXT NOT NULL,
  chunk_id TEXT NOT NULL,
  chunk_index INT NOT NULL,
  language TEXT NOT NULL DEFAULT 'ko',
  version INT NOT NULL DEFAULT 1,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### 컬럼별 의미

- **id**: 내부 PK, 정렬/조인용
- **content**: 문서 본문
- **embedding**: 본문에 대한 임베딩 벡터
- **metadata**: 도메인별 속성(카테고리, 권한 등)
- **source_id**: 원본 문서 식별자
- **chunk_id**: 분할된 청크 식별자
- **chunk_index**: 원문 내 청크 순서
- **language**: 다국어 검색 대비
- **version**: 문서 업데이트 버전 관리
- **created_at/updated_at**: 변경 이력 관리

> **source_id + chunk_index**는 중복 방지와 재수집에 매우 중요합니다.

**설계 주의사항**

- `language`를 **컬럼과 metadata에 동시에 두면** 정합성이 깨질 수 있다  
- 하나를 **단일 소스 오브 트루스**로 정하고 나머지는 파생으로 취급한다

---

## 5. 메타데이터 설계 요소별 설명

메타데이터는 검색 품질을 좌우합니다. 아래 요소는 **실무에서 자주 쓰는 핵심 필드**입니다.

- **category**: 분류 기준(예: 정책/가이드/FAQ)
- **access_level**: 권한 필터(예: public/internal)
- **product**: 제품/서비스 구분
- **effective_date**: 정책/문서 유효 기간
- **tags**: 키워드 기반 필터

```json
{
  "category": "policy",
  "access_level": "internal",
  "product": "billing",
  "effective_date": "2025-01-01",
  "tags": ["refund", "invoice"]
}
```

---

## 6. 인덱스 요소별 설명

### 1) IVFFlat

- **장점**: 대용량에서 빠른 검색
- **단점**: 튜닝 없으면 정확도 하락

```sql
-- 목적: 대용량 검색을 위한 IVFFlat 인덱스.
CREATE INDEX idx_documents_embedding_ivf
ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

**튜닝 기준**

- `lists`: 클러스터 개수
  - 작으면 속도는 빠르지만 정확도 하락
  - 크면 정확도는 높지만 빌드 비용 증가
- `probes`: 검색 시 탐색 클러스터 수(쿼리 세션에서 조정)

```sql
-- 목적: 검색 정확도를 높이기 위해 탐색 범위를 늘린다.
SET ivfflat.probes = 10;
```

### 2) HNSW

- **장점**: 정확도가 높음
- **단점**: 메모리 사용량 증가

```sql
-- 목적: 정확도 중심의 HNSW 인덱스.
CREATE INDEX idx_documents_embedding_hnsw
ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 200);
```

**파라미터 설명**

- `m`: 각 노드가 연결하는 이웃 수
  - 크면 정확도 향상, 메모리 증가
- `ef_construction`: 인덱스 생성 시 탐색 폭
  - 크면 인덱스 품질 향상, 빌드 시간 증가
- `ef_search`: 검색 시 탐색 폭(쿼리 세션에서 조정)
  - 크면 정확도 향상, 지연 시간 증가

```sql
-- 목적: 검색 정확도를 높이기 위해 탐색 폭을 늘린다.
SET hnsw.ef_search = 80;
```

---

## 7. 청크 전략(Chunking Strategy)

청크 전략은 **검색 성능과 품질을 동시에 결정**합니다.
잘못된 청크 설계는 검색 결과를 왜곡하고, 생성 품질을 떨어뜨립니다.

### 1) 청크 크기(Chunk Size)

- 너무 작으면 문맥이 끊겨 **답변 근거가 약해짐**
- 너무 크면 불필요한 문맥이 늘어 **정확도와 비용 하락**

**실무 기준(출발점)**

- 300~800 토큰 범위에서 시작
- 도메인 문서 길이에 맞춰 조정

### 2) 오버랩(Overlap)

- 인접 청크 간 문맥 연결을 보장
- 10~20% 수준에서 시작해 조정

### 3) 분할 기준

- 문단/헤더 단위가 가장 안정적
- 코드/표가 많은 문서는 **구조 기반 분할** 필요

### 4) 청크 메타데이터

- `source_id`, `chunk_id`, `chunk_index`는 필수
- 원문 회복과 재색인에 반드시 필요

```python
"""
목적: 간단한 청크 분할과 메타데이터 생성을 보여준다.
설명: 문단 단위로 분할하고, 순서를 기록한다.
디자인 패턴: Factory
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    """청크 데이터 모델."""

    source_id: str
    chunk_id: str
    chunk_index: int
    content: str


def build_chunks(source_id: str, text: str) -> list[Chunk]:
    """문단 기준 청크를 생성한다."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[Chunk] = []
    for idx, paragraph in enumerate(paragraphs):
        chunks.append(
            Chunk(
                source_id=source_id,
                chunk_id=f"{source_id}:{idx}",
                chunk_index=idx,
                content=paragraph,
            )
        )
    return chunks
```

---

## 8. 검색 쿼리 요소별 설명

### 1) 단순 벡터 검색

```sql
-- 목적: 코사인 거리 기준 Top-K 검색.
SELECT id, content, metadata
FROM documents
ORDER BY embedding <=> :query_vector
LIMIT 5;
```

- `ORDER BY embedding <=> :query_vector`가 핵심
- **거리가 낮을수록 유사**함

### 2) 메타데이터 필터 + 벡터 검색

```sql
-- 목적: 특정 카테고리 내에서만 검색.
SELECT id, content, metadata
FROM documents
WHERE metadata->>'category' = 'policy'
ORDER BY embedding <=> :query_vector
LIMIT 5;
```

- **사전 필터링**으로 검색 품질과 속도 개선

---

## 9. LangChain 기반 저장/검색

LangChain 생태계와의 호환성을 확보하려면 `langchain-postgres`의
**PGVectorStore**를 사용하는 것이 가장 안전한 선택입니다.
PGVectorStore는 LangChain의 `Document`를 그대로 저장하고 검색할 수 있습니다.

> 참고: LangChain에서는 기존 `PGVector` 대신 `PGVectorStore` 사용이 권장됩니다.
> 주의: `langchain-postgres`/`langchain-core` 버전에 따라 API 이름과 인자 구성이 달라질 수 있습니다.
> 공식 문서/릴리스 노트를 확인하고 예제를 맞춰주세요.

```python
"""
목적: LangChain + PGVectorStore로 문서를 저장하고 검색한다.
설명: PGEngine으로 테이블을 초기화하고, Document를 저장한다.
디자인 패턴: Repository
"""

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGEngine, PGVectorStore


CONNECTION_STRING = (
    "postgresql+psycopg://langchain:langchain@localhost:5432/langchain"
)
TABLE_NAME = "documents"
VECTOR_SIZE = 1536


engine = PGEngine.from_connection_string(url=CONNECTION_STRING)
engine.init_vectorstore_table(
    table_name=TABLE_NAME,
    vector_size=VECTOR_SIZE,
)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

store = PGVectorStore.create_sync(
    engine=engine,
    table_name=TABLE_NAME,
    embedding_service=embeddings,
)

docs = [
    Document(page_content="환불 정책 안내", metadata={"category": "policy"}),
    Document(page_content="결제 실패 대응 가이드", metadata={"category": "guide"}),
]
store.add_documents(docs)

results = store.similarity_search("환불 절차가 궁금합니다", k=5)
```

**실무 팁**

- `VECTOR_SIZE`는 임베딩 모델 차원과 반드시 일치해야 함
- `TABLE_NAME`은 환경별로 명확한 규칙을 정해 고정하는 것이 안전함

---

## 10. OpenAI 임베딩 API 호출 흐름

임베딩을 만들기 위해서는 다음 순서가 필요합니다.

1) API 키 준비 (`OPENAI_API_KEY` 환경 변수)
2) 임베딩 모델 선택 (`text-embedding-3-small` 등)
3) `/v1/embeddings`에 `input`, `model`을 포함해 요청
4) 응답의 `data[0].embedding`을 저장

```python
"""
목적: OpenAI 임베딩 API로 벡터를 생성한다.
설명: requests를 사용해 /v1/embeddings 엔드포인트를 호출한다.
디자인 패턴: Service
"""

import os
import requests


def embed_text(text: str) -> list[float]:
    """텍스트를 임베딩 벡터로 변환한다."""
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "text-embedding-3-small",
        "input": text,
        "encoding_format": "float",
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]
```

**실무 팁**

- 입력 토큰은 모델 제한을 넘기면 실패하므로 사전에 길이 제한 필요
- 한 번에 여러 텍스트를 넣을 수도 있지만, 총합 토큰 한도를 고려해야 함

---

## 11. 순수 psycopg 기반 예제

아래 코드는 **f-string으로 SQL 템플릿을 구성**하는 예시입니다.
다만 사용자 입력을 직접 문자열에 넣으면 SQL 인젝션 위험이 있으므로
**테이블명처럼 고정된 값만 f-string으로 넣고, 데이터는 파라미터로 전달**하세요.
테이블명을 동적으로 조합해야 한다면 `psycopg.sql.Identifier`를 사용해야 합니다.

```python
"""
목적: PGVector 테이블에 임베딩을 저장하고 검색한다.
설명: f-string으로 SQL 템플릿을 구성하되 값은 파라미터로 전달한다.
디자인 패턴: Repository
"""

from dataclasses import dataclass
from typing import Sequence
import psycopg


@dataclass(frozen=True)
class Document:
    """문서 저장용 데이터 모델."""

    content: str
    embedding: Sequence[float]
    metadata: dict


class DocumentRepository:
    """문서 저장과 검색을 담당한다."""

    def __init__(self, dsn: str, table_name: str = "documents") -> None:
        self._dsn = dsn
        self._table_name = table_name

    def save(self, doc: Document) -> None:
        """문서를 저장한다."""
        sql = f"""
        INSERT INTO {self._table_name} (content, embedding, metadata)
        VALUES (%s, %s, %s)
        """
        with psycopg.connect(self._dsn) as conn:
            conn.execute(sql, (doc.content, doc.embedding, doc.metadata))

    def search(self, query_vector: Sequence[float], top_k: int) -> list[tuple]:
        """유사 문서를 검색한다."""
        sql = f"""
        SELECT id, content, metadata
        FROM {self._table_name}
        ORDER BY embedding <=> %s
        LIMIT %s
        """
        with psycopg.connect(self._dsn) as conn:
            rows = conn.execute(sql, (query_vector, top_k)).fetchall()
        return rows
```

---

## 12. 실무 설계 시 고려사항

- **차원 불일치 금지**: 임베딩 차원 수는 모델과 반드시 일치해야 함
- **연산자/옵스 클래스 통일**: 연산자와 인덱스 기준을 하나로 고정
- **인덱스 튜닝 계획**: 데이터 증가 시 `lists/ef_search` 기준 문서화
- **메타데이터 품질**: 필터 기준이 흔들리면 검색 결과도 흔들림
- **청크 전략 명시**: 크기/오버랩/분할 기준을 문서화
- **갱신 정책**: version/updated_at 기반으로 재색인 기준 정의

---

## 13. 흔한 실수

- 임베딩 차원을 잘못 설정해 **검색이 실패**함
- 연산자/옵스 클래스를 섞어 써서 **점수 해석이 꼬임**
- 메타데이터 필터가 느려져 **지연 시간 증가**
- 청크가 과도하게 커서 **검색 품질이 하락**
- 인덱스 튜닝 없이 운영해 **정확도/속도 동시 하락**

---

## 14. 체크리스트

- 벡터 차원 수와 모델이 일치하는가?
- 연산자/옵스 클래스가 일치하는가?
- 메타데이터 필터 기준이 명확한가?
- HNSW/IVF 파라미터 튜닝 계획이 있는가?
- 청크 전략이 문서화되어 있는가?
