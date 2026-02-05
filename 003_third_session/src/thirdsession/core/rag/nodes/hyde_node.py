# 목적: HyDE 기반 재검색을 수행한다.
# 설명: 가상 문서를 생성해 재검색하는 노드이다.
# 디자인 패턴: Command
# 참조: thirdsession/core/rag/prompts/hyde_prompt.py

"""HyDE 노드 모듈."""

from __future__ import annotations

from typing import Any

from thirdsession.core.common.llm_client import LlmClient


class HydeNode:
    """HyDE 노드."""

    def __init__(self, llm_client: LlmClient | None = None) -> None:
        """노드 의존성을 초기화한다.

        Args:
            llm_client: LLM 클라이언트(선택).
        """
        self._llm_client = llm_client

    def run(self, question: str, store: Any) -> list[Any]:
        """가상 문서로 재검색한다."""
        # TODO: HyDE 문서 생성 및 재검색 로직을 구현한다.
        _ = self._llm_client
        raise NotImplementedError
