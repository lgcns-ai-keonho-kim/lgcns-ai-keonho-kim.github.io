# 목적: 대화 내역을 상태에 누적한다.
# 설명: turn_count를 증가시키고 history를 업데이트한다.
# 디자인 패턴: 파이프라인 노드
# 참조: secondsession/core/chat/graphs/chat_graph.py

"""대화 내역 업데이트 노드 모듈."""

from secondsession.core.chat.state.chat_state import ChatState


class AppendHistoryNode:
    """대화 내역을 갱신하는 노드."""

    def run(self, state: ChatState) -> ChatState:
        """대화 내역을 갱신한다.

        Args:
            state: 현재 대화 상태.

        Returns:
            ChatState: 대화 내역이 반영된 상태.
        """
        # TODO: history에 사용자/어시스턴트 메시지를 추가한다.
        # TODO: turn_count를 1 증가시킨다.
        # TODO: reducer가 누적하므로 history는 신규 항목만 반환한다.
        # TODO: reducer가 누적하므로 turn_count는 증가분만 반환한다.
        # TODO: ChatHistoryItem(Pydantic)으로 항목을 검증한다.
        _ = state.get("history", [])
        _ = state.get("last_user_message")
        _ = state.get("last_assistant_message")
        raise NotImplementedError("대화 내역 갱신 로직을 구현해야 합니다.")
