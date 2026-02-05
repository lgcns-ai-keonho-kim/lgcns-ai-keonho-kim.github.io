# 목적: 안전 분류 라벨을 정의한다.
# 설명: 안전 분기 정책에서 일관된 라벨을 사용한다.
# 디자인 패턴: Value Object
# 참조: nextStep.md

"""안전 분류 라벨 상수 모듈."""

from enum import Enum


class SafeguardLabel(Enum):
    """안전 분류 라벨."""

    PASS = "PASS"
    PII = "PII"
    HARMFUL = "HARMFUL"
    PROMPT_INJECTION = "PROMPT_INJECTION"


# TODO:
# - 라벨별 정책(차단/완화/리다이렉트)을 문서화한다.
