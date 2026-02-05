# 목적: 안전 분류 실패 시 응답을 구성한다.
# 설명: 차단 메시지를 표준화하여 상태에 기록한다.
# 디자인 패턴: 파이프라인 노드
# 참조: firstsession/core/translate/const/safeguard_messages.py

"""안전 분류 실패 응답 노드 모듈."""

from firstsession.core.translate.state.translation_state import TranslationState


class SafeguardFailResponseNode:
    """안전 분류 실패 응답을 담당하는 노드."""

    def run(self, state: TranslationState) -> TranslationState:
        """차단 응답을 구성한다.

        Args:
            state: 현재 번역 상태.

        Returns:
            TranslationState: 차단 응답이 포함된 상태.
        """
        # TODO: 차단 메시지를 응답 필드로 설정한다.
        # TODO: 차단 사유 로깅 규칙을 정의한다.
        raise NotImplementedError("안전 분류 실패 응답 로직을 구현해야 합니다.")
