# 목적: 질문을 하위 쿼리로 분해한다.
# 설명: 쿼리 분해 프롬프트를 이용하는 노드이다.
# 디자인 패턴: Command
# 참조: thirdsession/core/rag/prompts/query_decompose_prompt.py

"""쿼리 분해 노드 모듈."""

from __future__ import annotations

from thirdsession.core.common.llm_client import LlmClient


class QueryDecomposeNode:
    """쿼리 분해 노드."""

    def __init__(self, llm_client: LlmClient | None = None) -> None:
        """노드 의존성을 초기화한다.

        Args:
            llm_client: LLM 클라이언트(선택).
        """
        self._llm_client = llm_client

    def run(self, question: str) -> list[str]:
        """질문을 하위 쿼리로 분해한다."""
        # TODO: LLM 호출과 파싱 로직을 구현한다.
        _ = self._llm_client
        raise NotImplementedError
