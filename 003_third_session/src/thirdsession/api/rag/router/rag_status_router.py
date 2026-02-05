# 목적: 잡 상태 라우터를 제공한다.
# 설명: 상태 조회 엔드포인트를 정의한다.
# 디자인 패턴: 라우터 팩토리 패턴
# 참조: thirdsession/api/rag/service/rag_job_service.py

"""잡 상태 라우터 모듈."""

from fastapi import APIRouter

from thirdsession.api.rag.model.job_status_response import JobStatusResponse
from thirdsession.api.rag.service.rag_job_service import RagJobService


class RagStatusRouter:
    """잡 상태 라우터를 구성한다."""

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
            "/status/{job_id}",
            self.get_status,
            methods=["GET"],
            response_model=JobStatusResponse,
        )

    def get_status(self, job_id: str) -> JobStatusResponse:
        """잡 상태를 조회한다."""
        return self._job_service.get_status(job_id)
