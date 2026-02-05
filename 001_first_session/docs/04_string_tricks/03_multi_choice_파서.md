# 03. 복수 선택(B, D) 응답 처리

## 이 문서의 목표

- 프롬프트로 **복수 선택**을 안정적으로 유도하는 방법을 익힌다.
- 출력 결과를 **라우팅 Enum 리스트**로 변환해 분기한다.
- 실패 시 재요청/보정/기본값 등 **재시도 전략**은 05 문서에서 통합적으로 다룬다.

---

## 1) 프롬프트로 복수 선택을 유도하는 방법

복수 선택은 LLM이 설명을 섞어 출력하기 때문에 파싱 난도가 높습니다.
따라서 프롬프트에서 **구분자, 정렬 규칙, 예시**까지 자세히 제공해야 합니다.

### 예시 시나리오

고객 리뷰에서 문제 유형을 복수 선택으로 분류합니다.

- A: 가격
- B: 품질
- C: 배송
- D: 서비스
- NONE: 해당 없음

### 프롬프트 설계 원칙

- 출력은 **쉼표로 구분된 대문자**만 허용한다.
- 정렬 규칙을 고정한다(예: A,B,C,D 순서).
- 선택이 없으면 **NONE**만 출력하게 한다.

### 프롬프트 설계 예시 (LangChain)

```python
"""
목적: 복수 선택 결과를 안정적으로 출력하게 한다.
설명: 구분자와 정렬 규칙을 명시한다.
디자인 패턴: 모듈 싱글턴
"""

from langchain_core.prompts import PromptTemplate

_prompt = """너는 리뷰 분류기다. 해당되는 항목을 모두 선택해라.

[선택지]
A: 가격
B: 품질
C: 배송
D: 서비스

[규칙]
- 해당되는 항목을 모두 선택한다.
- 선택이 없으면 NONE만 출력한다.
- 출력은 대문자와 쉼표만 허용된다.
- 정렬 규칙: A,B,C,D 순서로 나열한다.
- 설명, 공백, 구두점(쉼표 제외)은 금지한다.

[입력]
{text}

[출력]
A,B 또는 B,D 또는 NONE"""
prompt = PromptTemplate(
    template=_prompt,
    input_variables=["text"],
)
```

---

## 2) 라우팅 Enum으로 반환 받는 방법

복수 선택은 **Enum 리스트**로 변환해 라우팅하는 것이 안전합니다.

### Enum 정의

```python
"""
목적: 리뷰 이슈 라벨을 Enum으로 정의한다.
설명: 복수 선택 결과를 표준화한다.
디자인 패턴: Enum
참조: docs/04_string_tricks/03_multi_choice_파서.md
"""

from enum import Enum


class IssueTag(Enum):
    """리뷰 이슈 라벨."""

    PRICE = "A"
    QUALITY = "B"
    DELIVERY = "C"
    SERVICE = "D"
    NONE = "NONE"
```

### 파싱 및 라우팅 예시

```python
"""
목적: 복수 선택 응답을 Enum 리스트로 변환한다.
설명: 중복 제거와 정렬을 적용한다.
디자인 패턴: Strategy
참조: docs/04_string_tricks/03_multi_choice_파서.md
"""

import re
from dataclasses import dataclass
from src.examples.issue_tag_enum import IssueTag


@dataclass(frozen=True)
class MultiChoiceRouter:
    """복수 선택 결과를 Enum 리스트로 변환한다."""

    order: list[IssueTag]

    def parse(self, raw_text: str) -> list[IssueTag]:
        """원본 텍스트를 Enum 리스트로 변환한다."""
        text = raw_text.strip().upper()
        if text == "NONE":
            return [IssueTag.NONE]
        found = re.findall(r"[A-D]", text)
        unique = {value for value in found}
        if not unique:
            return [IssueTag.NONE]
        mapping = {
            "A": IssueTag.PRICE,
            "B": IssueTag.QUALITY,
            "C": IssueTag.DELIVERY,
            "D": IssueTag.SERVICE,
        }
        selected = {mapping[value] for value in unique if value in mapping}
        return [tag for tag in self.order if tag in selected]
```

### 라우팅 예시

- DELIVERY 포함 → 배송 팀으로 라우팅
- SERVICE 포함 → 상담 팀으로 라우팅
- NONE → 일반 처리

---

불량 응답 재시도와 복구 흐름은 `docs/04_string_tricks/05_retry_logic.md`에서 통합적으로 설명합니다.

---

## 3) 구현 체크리스트

- 출력 구분자와 정렬 규칙이 프롬프트에 명시되었는가?
- 복수 선택 결과를 Enum 리스트로 변환하는가?
- NONE 처리 규칙이 명확한가?
- 파싱 실패 시 재요청 또는 안전 기본값이 있는가?
