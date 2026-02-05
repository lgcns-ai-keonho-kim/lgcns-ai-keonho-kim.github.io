# 목적: 주택 에이전트 라우터 등록 함수를 제공한다.
# 설명: app.state에 있는 서비스 객체를 사용해 라우터를 등록한다.
# 디자인 패턴: 레지스트리 패턴
# 참조: fourthsession/api/housing_agent/router/*

"""주택 에이전트 라우터 등록 모듈."""

from fastapi import FastAPI


def register_routes(app: FastAPI) -> None:
    """주택 에이전트 라우터를 앱에 등록한다.

    Args:
        app (FastAPI): FastAPI 애플리케이션.
    """
    # TODO: app.state에서 HousingAgentService, HousingJobService를 꺼낸다.
    # TODO: HousingAgentRouter + Job 라우터 4종을 include_router로 등록한다.
    raise NotImplementedError("TODO: 라우터 등록 구현")
