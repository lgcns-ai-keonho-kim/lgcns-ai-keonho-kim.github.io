# 목적: 대화 그래프를 구성한다.
# 설명: 답변 생성 → 대화 누적 → 요약 여부 판단 흐름을 정의한다.
# 디자인 패턴: 파이프라인 + 빌더
# 참조: secondsession/core/chat/nodes/answer_node.py, secondsession/core/chat/nodes/append_history_node.py

"""대화 그래프 구성 모듈."""

from __future__ import annotations

from typing import Any

from langgraph.graph import END, StateGraph

from secondsession.core.chat.nodes.answer_node import AnswerNode
from secondsession.core.chat.nodes.append_history_node import AppendHistoryNode
from secondsession.core.chat.nodes.decide_summary_node import DecideSummaryNode
from secondsession.core.chat.nodes.fallback_node import FallbackNode
from secondsession.core.chat.nodes.safeguard_node import SafeguardNode
from secondsession.core.chat.nodes.summary_node import SummaryNode
from secondsession.core.chat.state.chat_state import ChatState
from secondsession.core.common.llm_client import LlmClient


class ChatGraph:
    """대화 그래프 실행기."""

    def __init__(
        self,
        checkpointer: Any | None = None,
        llm_client: LlmClient | None = None,
    ) -> None:
        """그래프를 초기화한다.

        Args:
            checkpointer: LangGraph 체크포인터 인스턴스.
            llm_client: LLM 클라이언트(선택).
        """
        self._checkpointer = checkpointer
        self._llm_client = llm_client
        self._app = self._build_graph()

    def run(self, state: ChatState) -> ChatState:
        """대화 그래프를 실행한다.

        Args:
            state: 대화 입력 상태.

        Returns:
            ChatState: 대화 결과 상태.
        """
        # TODO: thread_id를 config에 넣어 체크포인트 복구를 활성화하세요.
        # TODO: 복구된 history를 기반으로 답변을 이어가도록 구성하세요.
        return self._app.invoke(state)

    def _route_by_safeguard(self, state: ChatState) -> str:
        """안전 라벨에 따른 분기 정책을 정의한다.

        TODO:
            - safeguard_label 기준 분기 정책을 구현한다.
            - PASS가 아닌 경우 error_code를 설정하도록 연결한다.
            - 정책/규제 요구사항을 반영한다.
            - 라벨별로 폴백 메시지/차단 로직을 분리한다.
            - SafeguardLabel(Enum)을 사용해 분기 값을 고정한다.
        """
        label = state.get("safeguard_label")
        # 임시 정책: PASS만 통과, 그 외는 폴백으로 라우팅
        if label == "PASS":
            return "answer"
        return "fallback"

    def _build_graph(self) -> object:
        """대화 그래프를 구성한다.

        Returns:
            object: 컴파일된 LangGraph 애플리케이션.
        """
        graph = StateGraph(ChatState)
        safeguard_node = SafeguardNode(self._llm_client)
        answer_node = AnswerNode(self._llm_client)
        fallback_node = FallbackNode()
        append_history_node = AppendHistoryNode()
        decide_summary_node = DecideSummaryNode()
        summary_node = SummaryNode(self._llm_client)

        graph.add_node("safeguard", safeguard_node.run)
        graph.add_node("answer", answer_node.run)
        graph.add_node("fallback", fallback_node.run)
        graph.add_node("append_history", append_history_node.run)
        graph.add_node("decide_summary", decide_summary_node.run)
        graph.add_node("summarize", summary_node.run)

        graph.set_entry_point("safeguard")
        graph.add_conditional_edges("safeguard", self._route_by_safeguard, {
            "answer": "answer",
            "fallback": "fallback",
        })
        graph.add_edge("answer", "append_history")
        graph.add_edge("append_history", "decide_summary")

        graph.add_conditional_edges("decide_summary", lambda s: s["route"], {
            "summarize": "summarize",
            "end": END,
        })
        graph.add_edge("fallback", END)
        graph.add_edge("summarize", END)

        # TODO:
        # - 폴백 응답도 필요한 경우 history에 기록하도록 정책을 정하세요.
        # - answer 단계의 에러(error_code)를 fallback으로 라우팅하는 경로를 추가하세요.

        if self._checkpointer is None:
            return graph.compile()
        return graph.compile(checkpointer=self._checkpointer)
