# 목적: 답변 생성과 스트리밍을 수행한다.
# 설명: 근거 기반 답변을 만든 뒤 토큰 단위 스트리밍 규칙을 적용한다.
# 디자인 패턴: Command
# 참조: thirdsession/core/rag/prompts/answer_prompt.py, thirdsession/api/rag/model/chat_stream_event.py

"""답변 생성/스트리밍 노드 모듈."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from thirdsession.core.common.llm_client import LlmClient
from thirdsession.core.rag.prompts.answer_prompt import ANSWER_PROMPT

# TODO: 스트리밍 이벤트 모델/타입을 활용하도록 연결한다.


class StreamAnswerNode:
    """답변 생성/스트리밍 노드."""

    def __init__(self, llm_client: LlmClient | None = None) -> None:
        """노드 의존성을 초기화한다.

        Args:
            llm_client: LLM 클라이언트(선택).
        """
        self._llm_client = llm_client

    async def run(
        self,
        question: str,
        contexts: list[Any],
        trace_id: str,
        seq_start: int = 1,
        node: str | None = "stream_answer",
    ) -> AsyncIterator[str]:
        """답변을 생성한 뒤 스트리밍한다.

        Args:
            question: 사용자 질문.
            contexts: 검색/후처리된 컨텍스트.
            trace_id: 스트리밍 추적 식별자.
            seq_start: 시작 시퀀스 번호.
            node: 노드 식별자(선택).

        Yields:
            str: SSE 데이터 라인.
        """
        # TODO: LLM 응답을 스트림으로 바로 흘리는 모드도 추가한다.
        answer = await self._generate_answer(question, contexts)
        # TODO: answer를 토큰 단위로 분리해 SSE 이벤트를 생성한다.
        # TODO: seq 단조 증가와 trace_id 포함 규칙을 반영한다.
        _ = self._split_answer(answer)
        _ = trace_id
        _ = seq_start
        _ = node
        raise NotImplementedError("답변 생성/스트리밍 로직을 구현해야 합니다.")

    async def _generate_answer(self, question: str, contexts: list[Any]) -> str:
        """근거 기반 답변을 생성한다."""
        # TODO: LLM 호출과 출력 포맷 규칙을 구현한다.
        # TODO: 필요 시 컨텍스트 압축/정규화 규칙을 먼저 적용한다.
        formatted_contexts = self._format_contexts(contexts)
        _ = question
        _ = formatted_contexts
        _ = self._llm_client
        _ = ANSWER_PROMPT
        raise NotImplementedError("답변 생성 로직을 구현해야 합니다.")

    def _split_answer(self, answer: str) -> list[str]:
        """답변을 토큰 단위로 분리한다."""
        # TODO: 토큰 분할 규칙(공백/문장/모델 토큰)을 확정한다.
        _ = answer
        raise NotImplementedError("토큰 분할 규칙을 구현해야 합니다.")

    def _format_contexts(self, contexts: list[Any]) -> str:
        """컨텍스트 목록을 LLM 입력 문자열로 변환한다."""
        # TODO: 컨텍스트 포맷 규칙을 확정한다.
        _ = contexts
        raise NotImplementedError("컨텍스트 포맷 규칙을 구현해야 합니다.")
