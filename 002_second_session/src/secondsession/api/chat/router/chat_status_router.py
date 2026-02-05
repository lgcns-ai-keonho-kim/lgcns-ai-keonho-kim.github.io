# 목적: 대화 작업 상태 라우터를 제공한다.
# 설명: 상태 조회 엔드포인트를 정의한다.
# 디자인 패턴: 라우터 팩토리 패턴
# 참조: secondsession/api/chat/service/chat_service.py
#       secondsession/api/chat/model/__init__.py

"""대화 작업 상태 라우터 모듈."""

from fastapi import APIRouter

from secondsession.api.chat.model import ChatJobStatusResponse
from secondsession.api.chat.service import ChatService


class ChatStatusRouter:
    """대화 작업 상태 라우터를 구성한다."""

    def __init__(self, service: ChatService) -> None:
        """라우터와 의존성을 초기화한다.

        Args:
            service: 대화 서비스.
        """
        self._service = service
        self.router = APIRouter()
        self._register_routes()

    def _register_routes(self) -> None:
        """상태 조회 라우트를 등록한다."""
        self.router.add_api_route(
            "/status/{job_id}",
            self.get_chat_status,
            methods=["GET"],
            response_model=ChatJobStatusResponse,
        )

    def get_chat_status(self, job_id: str) -> ChatJobStatusResponse:
        """대화 작업 상태를 조회한다."""
        return self._service.get_status(job_id)
