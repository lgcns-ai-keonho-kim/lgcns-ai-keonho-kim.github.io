# 목적: 대화 스트리밍 라우터를 제공한다.
# 설명: 스트리밍 엔드포인트를 정의한다.
# 디자인 패턴: 라우터 팩토리 패턴
# 참조: secondsession/api/chat/service/chat_service.py

"""대화 스트리밍 라우터 모듈."""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from secondsession.api.chat.service import ChatService


class ChatStreamRouter:
    """대화 스트리밍 라우터를 구성한다."""

    def __init__(self, service: ChatService) -> None:
        """라우터와 의존성을 초기화한다.

        Args:
            service: 대화 서비스.
        """
        self._service = service
        self.router = APIRouter()
        self._register_routes()

    def _register_routes(self) -> None:
        """스트리밍 라우트를 등록한다."""
        self.router.add_api_route(
            "/stream/{job_id}",
            self.stream_chat,
            methods=["GET"],
        )

    def stream_chat(self, job_id: str) -> StreamingResponse:
        """대화 스트리밍 엔드포인트."""
        return StreamingResponse(
            self._service.stream_events(job_id),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache"},
        )
