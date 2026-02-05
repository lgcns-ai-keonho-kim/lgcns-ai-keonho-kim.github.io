# 목적: FastAPI 애플리케이션 진입점을 제공한다.
# 설명: uvicorn에서 \"secondsession.main:app\" 형태로 실행할 수 있는 앱 객체를 정의한다.
# 디자인 패턴: 팩토리 메서드 패턴(애플리케이션 생성 책임 분리)
# 참조: secondsession/api, secondsession/core

"""FastAPI 애플리케이션 진입점 모듈."""

from fastapi import FastAPI

from secondsession.api.chat.router import register_routes as register_chat_routes
from secondsession.api.chat.service.chat_service import ChatService
from secondsession.core.chat.graphs.chat_graph import ChatGraph
from secondsession.core.common.app_config import AppConfig
from secondsession.core.common.llm_client import LlmClient


def create_app() -> FastAPI:
    """FastAPI 애플리케이션을 생성한다.

    Returns:
        FastAPI: 구성된 애플리케이션 인스턴스.
    """
    app = FastAPI(title="secondsession API")

    @app.get("/health", tags=["health"])
    def health() -> dict[str, str]:
        """간단한 헬스 체크 엔드포인트."""
        return {"status": "ok"}

    config = AppConfig.from_env()
    llm_client = LlmClient(config)
    graph = ChatGraph(llm_client=llm_client)
    service = ChatService(graph)
    app.state.chat_service = service
    register_chat_routes(app)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("secondsession.main:app", host="0.0.0.0", port=8000, reload=True)
