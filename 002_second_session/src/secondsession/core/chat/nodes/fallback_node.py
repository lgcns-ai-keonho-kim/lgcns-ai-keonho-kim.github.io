# 목적: 폴백 응답 노드를 정의한다.
# 설명: 안전/에러 상황에서 사용자에게 최소 안내를 제공한다.
# 디자인 패턴: 전략 패턴 + 파이프라인 노드
# 참조: secondsession/core/chat/graphs/chat_graph.py

"""폴백 응답 노드 모듈."""

from secondsession.core.chat.state.chat_state import ChatState


class FallbackNode:
    """폴백 응답을 생성하는 노드."""

    def run(self, state: ChatState) -> ChatState:
        """폴백 응답을 생성한다.

        Args:
            state: 현재 대화 상태.

        Returns:
            ChatState: 폴백 응답이 반영된 상태.
        """
        # TODO: error_code와 safeguard_label을 기반으로 폴백 메시지를 결정한다.
        # TODO: last_assistant_message에 폴백 응답을 담아 반환한다.
        # TODO: 필요한 경우 로그/메트릭을 추가한다.
        # TODO: 사용자 메시지 정책(톤/완화)을 enum 테이블로 관리한다.
        # TODO: ErrorCode/SafeguardLabel(Enum)을 기준으로 정책을 분기한다.
        _ = state.get("error_code")
        _ = state.get("safeguard_label")
        raise NotImplementedError("폴백 응답 로직을 구현해야 합니다.")
