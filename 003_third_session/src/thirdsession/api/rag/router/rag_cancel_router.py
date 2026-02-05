# 목적: 잡 취소 라우터를 제공한다.
# 설명: 취소 엔드포인트를 정의한다.
# 디자인 패턴: 라우터 팩토리 패턴
# 참조: thirdsession/api/rag/service/rag_job_service.py

"""잡 취소 라우터 모듈."""

from fastapi import APIRouter

from thirdsession.api.rag.model.job_cancel_response import JobCancelResponse
from thirdsession.api.rag.service.rag_job_service import RagJobService


class RagCancelRouter:
    """잡 취소 라우터를 구성한다."""

    def __init__(self, service: RagJobService) -> None:
        """라우터와 의존성을 초기화한다.

        Args:
            service: 잡 서비스.
        """
        self._service = service
        self._job_service = service
        self.router = APIRouter()
        self._register_routes()

    def _register_routes(self) -> None:
        """라우트 등록을 수행한다."""
        self.router.add_api_route(
            "/cancel/{job_id}",
            self.cancel_job,
            methods=["POST"],
            response_model=JobCancelResponse,
        )

    def cancel_job(self, job_id: str) -> JobCancelResponse:
        """잡 작업을 취소한다."""
        return self._job_service.cancel(job_id)
