# 목적: 근거 문서 스트리밍을 수행한다.
# 설명: 답변 이후 근거를 전송하는 규칙을 담당한다.
# 디자인 패턴: Command
# 참조: thirdsession/api/rag/model/chat_stream_event.py

"""근거 스트리밍 노드 모듈."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

# TODO: 스트리밍 이벤트/메타데이터/소스 모델을 연결한다.


class StreamSourcesNode:
    """근거 스트리밍 노드."""

    async def run(
        self,
        sources: list[Any],
        trace_id: str,
        seq_start: int,
        node: str | None = "stream_sources",
    ) -> AsyncIterator[str]:
        """근거 문서를 스트리밍한다.

        Args:
            sources: 근거 문서 목록(직렬화 가능 구조).
            trace_id: 스트리밍 추적 식별자.
            seq_start: 시작 시퀀스 번호.
            node: 노드 식별자(선택).

        Yields:
            str: SSE 데이터 라인.
        """
        # TODO: sources를 RagSourceItem으로 정규화한다.
        # TODO: sources 이벤트(타입/메타데이터/seq)를 생성한다.
        _ = sources
        _ = trace_id
        _ = seq_start
        _ = node
        raise NotImplementedError("근거 문서 스트리밍 로직을 구현해야 합니다.")

    def _normalize_sources(self, sources: list[Any]) -> list[Any]:
        """근거 문서 목록을 RagSourceItem으로 정규화한다."""
        # TODO: DocumentModel/dict/기타 타입을 RagSourceItem으로 변환한다.
        _ = sources
        raise NotImplementedError("근거 문서 정규화 로직을 구현해야 합니다.")

    def _from_dict(self, payload: dict[str, Any], index: int) -> Any:
        """dict 기반 소스를 RagSourceItem으로 변환한다."""
        _ = payload
        _ = index
        raise NotImplementedError("dict 기반 소스 변환 로직을 구현해야 합니다.")

    def _from_unknown(self, source: Any, index: int) -> Any:
        """알 수 없는 타입을 기본 구조로 변환한다."""
        _ = source
        _ = index
        raise NotImplementedError("알 수 없는 타입 변환 로직을 구현해야 합니다.")

    def _from_document(self, document: Any, index: int) -> Any:
        """DocumentModel을 RagSourceItem으로 변환한다."""
        _ = document
        _ = index
        raise NotImplementedError("DocumentModel 변환 로직을 구현해야 합니다.")
