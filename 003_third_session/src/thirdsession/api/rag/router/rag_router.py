# 목적: rag 요청 라우터를 제공한다.
# 설명: rag 요청 핸들러를 등록한다.
# 디자인 패턴: 라우터 팩토리 패턴
# 참조: thirdsession/api/rag/service/rag_service.py

"""rag 라우터 모듈."""

from fastapi import APIRouter

from thirdsession.api.rag.model.request import RagRequest
from thirdsession.api.rag.model.response import RagResponse
from thirdsession.api.rag.service.rag_service import RagService


class RagRouter:
    """rag API 라우터를 구성한다."""

    def __init__(self, service: RagService) -> None:
        """라우터와 의존성을 초기화한다.

        Args:
            service: rag 서비스.
        """
        self._service = service
        self.router = APIRouter()
        self.router.add_api_route(
            "",
            self.rag,
            methods=["POST"],
            response_model=RagResponse,
        )
        self.router.add_api_route(
            "/stream",
            self.rag_stream,
            methods=["POST"],
        )

    def rag(self, request: RagRequest) -> RagResponse:
        """rag 요청을 처리한다.

        Args:
            request: rag 요청 모델.

        Returns:
            RagResponse: 응답 모델.
        """
        # TODO: 인증/권한 확인, 요청 유효성 검사를 강화한다.
        _ = request
        raise NotImplementedError("rag 요청 처리 로직을 구현해야 합니다.")

    def rag_stream(self, request: RagRequest) -> None:
        """rag 스트리밍 요청을 처리한다.

        Args:
            request: rag 요청 모델.
        """
        # TODO: SSE 스트리밍 응답을 구성한다.
        # - 답변 SSE → 근거 SSE → done 순서를 보장한다.
        _ = request
        raise NotImplementedError("rag 스트리밍 로직을 구현해야 합니다.")
