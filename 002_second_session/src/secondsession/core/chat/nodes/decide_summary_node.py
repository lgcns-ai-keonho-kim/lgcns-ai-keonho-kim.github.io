# 목적: 요약 수행 여부를 결정한다.
# 설명: turn_count 기준으로 요약 경로를 선택한다.
# 디자인 패턴: 파이프라인 노드
# 참조: secondsession/core/chat/graphs/chat_graph.py

"""요약 여부 결정 노드 모듈."""

from secondsession.core.chat.state.chat_state import ChatState


class DecideSummaryNode:
    """요약 경로를 결정하는 노드."""

    def run(self, state: ChatState) -> ChatState:
        """요약 경로를 결정한다.

        Args:
            state: 현재 대화 상태.

        Returns:
            ChatState: 요약 라우팅 정보가 반영된 상태.
        """
        # TODO: turn_count가 5를 초과하면 route를 "summarize"로 설정한다.
        # TODO: 그렇지 않으면 route를 "end"로 설정한다.
        # TODO: error_code가 존재할 때는 폴백 라우팅으로 전환하는 정책을 추가한다.
        _ = state.get("turn_count", 0)
        raise NotImplementedError("요약 경로 결정 로직을 구현해야 합니다.")
