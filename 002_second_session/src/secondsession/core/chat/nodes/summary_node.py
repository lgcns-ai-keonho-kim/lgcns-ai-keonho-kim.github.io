# 목적: 대화 요약 노드를 정의한다.
# 설명: 대화 내역을 요약해 summary에 저장한다.
# 디자인 패턴: 전략 패턴 + 파이프라인 노드
# 참조: secondsession/core/chat/graphs/chat_graph.py

"""대화 요약 노드 모듈."""

from secondsession.core.chat.prompts.summary_prompt import SUMMARY_PROMPT
from secondsession.core.chat.state.chat_state import ChatState
from secondsession.core.common.llm_client import LlmClient


class SummaryNode:
    """대화 요약을 생성하는 노드."""

    def __init__(self, llm_client: LlmClient | None = None) -> None:
        """노드 의존성을 초기화한다.

        Args:
            llm_client: LLM 클라이언트(선택).
        """
        self._llm_client = llm_client

    def run(self, state: ChatState) -> ChatState:
        """대화 요약을 생성한다.

        Args:
            state: 현재 대화 상태.

        Returns:
            ChatState: 요약 결과가 반영된 상태.
        """
        # TODO: LLM 클라이언트를 연결한다.
        # TODO: SUMMARY_PROMPT.format으로 state["history"]를 결합한다.
        # TODO: summary 값을 반환한다.
        _ = SUMMARY_PROMPT
        _ = state.get("history", [])
        _ = self._llm_client
        raise NotImplementedError("요약 노드 로직을 구현해야 합니다.")
