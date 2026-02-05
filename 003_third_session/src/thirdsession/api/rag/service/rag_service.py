# 목적: rag 서비스 그래프 호출을 담당한다.
# 설명: API 계층에서 코어 그래프를 호출하고 응답 모델로 변환한다.
# 디자인 패턴: Service
# 참조: thirdsession/core/rag/graphs/rag_pipeline_graph.py

"""rag 서비스 모듈."""

from __future__ import annotations

from collections.abc import AsyncIterator

from thirdsession.api.rag.model.request import RagRequest
from thirdsession.api.rag.model.response import RagResponse
from thirdsession.core.rag.graphs.rag_pipeline_graph import RagPipelineGraph


class RagService:
    """rag 서비스 클래스."""

    def __init__(self, graph: RagPipelineGraph) -> None:
        """서비스 의존성을 초기화한다.

        Args:
            graph: rag 그래프 실행기.
        """
        self._graph = graph

    def handle(self, request: RagRequest) -> RagResponse:
        """rag 요청을 처리한다.

        Args:
            request: rag 요청 모델.

        Returns:
            RagResponse: 응답 모델.
        """
        # TODO: 요청을 그래프 입력 상태로 변환한다.
        # TODO: graph.run으로 파이프라인을 실행한다.
        # TODO: 결과를 RagResponse로 매핑한다.
        _ = request
        _ = self._graph
        raise NotImplementedError("rag 요청 처리 로직을 구현해야 합니다.")

    async def stream(self, request: RagRequest) -> AsyncIterator[str]:
        """rag 스트리밍을 처리한다.

        Args:
            request: rag 요청 모델.

        Yields:
            str: SSE 이벤트 라인.
        """
        # TODO: SSE 스트리밍 순서를 구현한다.
        # - 답변 토큰 이벤트 전송
        # - 근거(sources) 이벤트 전송
        # - done 이벤트 전송
        _ = request
        raise NotImplementedError("rag 스트리밍 로직을 구현해야 합니다.")

    # TODO: 요청 → 상태 변환 로직을 분리한다.
    # TODO: 컨텍스트 → 근거 소스 변환 로직을 분리한다.
