# 목적: 서비스 수준 RAG 파이프라인 그래프를 정의한다.
# 설명: 검색 → 정규화 → 병합 → 후처리 → 생성 → 스트리밍 순서를 담는다.
# 디자인 패턴: 파이프라인 + 빌더
# 참조: thirdsession/core/rag/nodes/postprocess_node.py

"""RAG 파이프라인 그래프 모듈."""

from __future__ import annotations

from typing import Any

from thirdsession.core.rag.state.chat_state import ChatState
from thirdsession.core.common.llm_client import LlmClient


class RagPipelineGraph:
    """RAG 파이프라인 그래프."""

    def __init__(self, llm_client: LlmClient | None = None) -> None:
        """그래프 의존성을 초기화한다.

        Args:
            llm_client: LLM 클라이언트(선택).
        """
        self._llm_client = llm_client

    def run(self, state: ChatState) -> ChatState:
        """RAG 파이프라인을 실행한다.

        Args:
            state: 입력 상태.

        Returns:
            ChatState: 실행 결과 상태.
        """
        # TODO: RAG 검색 → 생성 → 히스토리/요약 흐름을 구성한다.
        # TODO: SSE 순서(답변 → 근거 → done)와 연계되는 결과 필드를 채운다.
        _ = state
        _ = self._llm_client
        raise NotImplementedError("RAG 파이프라인 실행 로직을 구현해야 합니다.")

    def _build_graph(self) -> Any:
        """그래프를 구성한다.

        Returns:
            Any: LangGraph 애플리케이션.
        """
        # TODO: LangGraph 그래프와 노드 연결을 구현한다.
        _ = self._llm_client
        raise NotImplementedError
