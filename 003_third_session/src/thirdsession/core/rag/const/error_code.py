# 목적: 서비스 전역 에러 코드를 정의한다.
# 설명: 에러 코드/사용자 메시지를 함께 관리해 일관성을 유지한다.
# 디자인 패턴: Value Object
# 참조: nextStep.md, thirdsession/core/rag/state/chat_state.py

"""에러 코드 상수 모듈."""

from enum import Enum


class ErrorCode(Enum):
    """에러 코드와 사용자 메시지 정의."""

    VALIDATION = ("validation_error", "출력 형식 오류로 간단 요약을 제공합니다.")
    TOOL = ("tool_error", "외부 도구 호출에 실패했습니다. 기본 안내만 제공합니다.")
    RETRIEVAL_EMPTY = ("retrieval_empty", "관련 정보를 찾지 못했습니다. 일반 설명을 제공합니다.")
    TIMEOUT = ("timeout", "처리가 지연되었습니다. 잠시 후 다시 시도해 주세요.")
    SAFEGUARD = ("safeguard_blocked", "요청을 처리할 수 없습니다. 다른 질문을 해주세요.")
    UNKNOWN = ("unknown_error", "처리 중 문제가 발생했습니다. 잠시 후 다시 시도해 주세요.")

    @property
    def code(self) -> str:
        """시스템 식별자 문자열을 반환한다."""
        return self.value[0]

    @property
    def user_message(self) -> str:
        """사용자에게 노출할 메시지를 반환한다."""
        return self.value[1]


# TODO:
# - 도메인별 에러 코드를 추가한다.
# - API/로그에서 사용할 공통 매핑 규칙을 정의한다.
