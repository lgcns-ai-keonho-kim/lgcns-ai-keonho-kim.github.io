# 목적: FastAPI 애플리케이션 진입점을 제공한다.
# 설명: uvicorn에서 "fourthsession.main:app" 형태로 실행할 수 있는 앱 객체를 정의한다.
# 디자인 패턴: 팩토리 메서드 패턴(애플리케이션 생성 책임 분리)
# 참조: fourthsession/api, fourthsession/core

"""FastAPI 애플리케이션 진입점 모듈."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """FastAPI 애플리케이션을 생성한다.

    Returns:
        FastAPI: 구성된 애플리케이션 인스턴스.
    """
    app = FastAPI(title="fourthSession API")

    @app.get("/health", tags=["health"])
    def health() -> dict[str, str]:
        """간단한 헬스 체크 엔드포인트."""
        return {"status": "ok"}

    # TODO: 아래 흐름을 구현한다.
    # 1) HousingAgentService, HousingJobService 생성
    # 2) app.state에 서비스 저장
    # 3) register_routes(app) 호출로 라우터 등록
    raise NotImplementedError("TODO: 애플리케이션 구성 구현")


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("fourthsession.main:app", host="0.0.0.0", port=8000, reload=True)
