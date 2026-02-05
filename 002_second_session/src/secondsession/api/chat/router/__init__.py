# 목적: 대화 API 라우터를 FastAPI에 등록한다.
# 설명: 대화 관련 세부 라우터를 합성해 애플리케이션에 포함한다.
# 디자인 패턴: 컴포지트 패턴 + 등록자 패턴
# 참조: secondsession/api/chat/router/chat_job_router.py
#       secondsession/api/chat/router/chat_stream_router.py
#       secondsession/api/chat/router/chat_status_router.py
#       secondsession/api/chat/router/chat_cancel_router.py
#       secondsession/main.py

"""대화 라우터 등록 모듈."""

from fastapi import APIRouter, FastAPI

from secondsession.api.chat.router.chat_cancel_router import ChatCancelRouter
from secondsession.api.chat.router.chat_job_router import ChatJobRouter
from secondsession.api.chat.router.chat_status_router import ChatStatusRouter
from secondsession.api.chat.router.chat_stream_router import ChatStreamRouter
from secondsession.api.chat.service.chat_service import ChatService


def register_routes(app: FastAPI) -> None:
    """대화 API 라우터를 애플리케이션에 등록한다.

    Args:
        app: FastAPI 애플리케이션 인스턴스.
    """
    if not hasattr(app.state, "chat_service"):
        raise ValueError("app.state.chat_service가 설정되어야 합니다.")
    service = app.state.chat_service
    if not isinstance(service, ChatService):
        raise TypeError("app.state.chat_service는 ChatService 인스턴스여야 합니다.")
    chat_router = APIRouter(prefix="/chat", tags=["chat"])

    job_router = ChatJobRouter(service)
    stream_router = ChatStreamRouter(service)
    status_router = ChatStatusRouter(service)
    cancel_router = ChatCancelRouter(service)

    chat_router.include_router(job_router.router)
    chat_router.include_router(stream_router.router)
    chat_router.include_router(status_router.router)
    chat_router.include_router(cancel_router.router)

    app.include_router(chat_router)