# 목적: 잡 스트리밍 라우터를 제공한다.
# 설명: 스트리밍 엔드포인트를 정의한다.
# 디자인 패턴: 라우터 팩토리 패턴
# 참조: thirdsession/api/rag/service/rag_job_service.py

"""잡 스트리밍 라우터 모듈."""

from fastapi import APIRouter

from fastapi.responses import StreamingResponse

from thirdsession.api.rag.service.rag_job_service import RagJobService


class RagStreamRouter:
    """잡 스트리밍 라우터를 구성한다."""

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
            "/stream/{job_id}",
            self.stream_job,
            methods=["GET"],
        )

    def stream_job(self, job_id: str) -> StreamingResponse:
        """잡 스트리밍 응답을 반환한다."""
        return StreamingResponse(
            self._job_service.stream_events(job_id),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache"},
        )
