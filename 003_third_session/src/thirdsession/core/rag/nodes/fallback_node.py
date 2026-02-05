# 목적: 폴백 응답을 생성한다.
# 설명: 에러 코드/안전 라벨에 따른 기본 응답을 만든다.
# 디자인 패턴: Command
# 참조: thirdsession/core/rag/const/error_code.py

"""폴백 응답 노드 모듈."""

from thirdsession.core.rag.const import ErrorCode


class FallbackNode:
    """폴백 응답 노드."""

    def run(self, error_code: ErrorCode | None) -> str:
        """에러 코드 기반 폴백 응답을 생성한다."""
        if error_code is None:
            return ErrorCode.UNKNOWN.user_message
        return error_code.user_message
