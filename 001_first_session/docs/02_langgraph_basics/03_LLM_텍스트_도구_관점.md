# 03. LLM을 "텍스트 도구"로 보는 관점

## 이 챕터에서 다루는 내용

- LLM은 API가 아니라 "텍스트 함수"라는 관점
- 텍스트 출력의 불확실성을 다루는 방법
- LangGraph 노드 설계 시의 안전장치

---

## 1. 왜 "텍스트 도구" 관점이 중요한가?

LLM은 내부적으로 확률적 생성기입니다. 따라서 결과는 다음 특성을 가집니다.

- 입력을 바꾸면 출력이 쉽게 흔들린다.
- 같은 입력에도 출력이 약간씩 달라질 수 있다.
- 규격을 지키지 않는 응답이 발생한다.

이 때문에 LLM을 **정답 함수**로 취급하면 시스템이 불안정해집니다.
LLM을 "텍스트를 반환하는 도구"로 보고, **후처리 파이프라인**을 설계해야 합니다.

---

## 2. 텍스트 도구로서의 안전장치

다음 3단계를 항상 포함하세요.

1. **파싱(Parsing)**: 텍스트를 구조화한다.
2. **검증(Validation)**: 허용 가능한 값인지 확인한다.
3. **정규화(Normalization)**: 표준 표현으로 통일한다.

이 과정이 없으면, 그래프 전체가 불안정해집니다.

---

## 3. LangGraph에서의 안전한 노드 설계 예시

아래 코드는 LLM 응답을 안전하게 처리하기 위한 **어댑터(Adapter)** 예시입니다.
노드에서 직접 LLM 호출을 하지 않고, 텍스트를 가공하는 클래스를 둡니다.

```python
"""
목적: LLM 텍스트 응답을 안전하게 처리하는 어댑터를 제공한다.
설명: 파싱-검증-정규화 과정을 하나의 클래스로 묶는다.
디자인 패턴: Adapter
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TextToolAdapter:
    """LLM 텍스트 응답을 안전하게 다루는 어댑터."""

    allowed: set[str]

    def parse_and_normalize(self, raw_text: str) -> str:
        """텍스트를 파싱하고 검증한 뒤 표준 형식으로 반환한다.

        Args:
            raw_text: LLM이 반환한 원본 텍스트.

        Returns:
            str: 검증된 표준 텍스트.
        """
        cleaned = raw_text.strip().upper()
        if cleaned not in self.allowed:
            raise ValueError(f"허용되지 않은 값: {cleaned}")
        return cleaned
```

### 사용 예 (개념)

```python
adapter = TextToolAdapter(allowed={"YES", "NO"})
normalized = adapter.parse_and_normalize(" yes ")
```

---

## 4. 초보자를 위한 실전 팁

- 노드 내부에서 문자열을 바로 사용하지 말고, 항상 변환 단계를 둔다.
- 검증 실패 시에는 다음 노드로 넘어가지 않도록 설계한다.
- 출력 포맷은 "최대한 단순하게" 만들고, 파싱 난이도를 낮춘다.

이 관점만 지켜도 LangGraph 기반 파이프라인의 안정성이 크게 향상됩니다.

---

## 5. 구현 체크리스트

- 파싱/검증/정규화 3단계가 명확히 분리되어 있는가?
- 허용 가능한 값 목록이 코드에 고정되어 있는가?
- 검증 실패 시 다음 노드로 넘어가지 않도록 설계했는가?
- 실패 로그와 원인 메시지를 남기도록 구성했는가?
