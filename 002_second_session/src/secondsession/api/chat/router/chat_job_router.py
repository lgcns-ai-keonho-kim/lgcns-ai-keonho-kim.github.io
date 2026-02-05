# 목적: 대화 작업 생성 라우터를 제공한다.
# 설명: 작업 생성 엔드포인트를 정의한다.
# 디자인 패턴: 라우터 팩토리 패턴
# 참조: secondsession/api/chat/service/chat_service.py
#       secondsession/api/chat/model/__init__.py

"""대화 작업 생성 라우터 모듈."""

from fastapi import APIRouter

from secondsession.api.chat.model import ChatJobRequest, ChatJobResponse
from secondsession.api.chat.service import ChatService


class ChatJobRouter:
    """대화 작업 생성 라우터를 구성한다."""

    def __init__(self, service: ChatService) -> None:
        """라우터와 의존성을 초기화한다.

        Args:
            service: 대화 서비스.
        """
        self._service = service
        self.router = APIRouter()
        self._register_routes()

    def _register_routes(self) -> None:
        """작업 생성 라우트를 등록한다."""
        self.router.add_api_route(
            "/jobs",
            self.create_chat_job,
            methods=["POST"],
            response_model=ChatJobResponse,
        )

    def create_chat_job(self, payload: ChatJobRequest) -> ChatJobResponse:
        """대화 작업을 생성한다."""
        return self._service.create_job(payload)
