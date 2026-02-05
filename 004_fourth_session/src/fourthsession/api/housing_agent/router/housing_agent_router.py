# 목적: 주택 에이전트 라우터를 정의한다.
# 설명: API 엔드포인트와 서비스 호출을 연결한다.
# 디자인 패턴: 라우터 패턴
# 참조: fourthsession/api/housing_agent/service

"""주택 에이전트 라우터 모듈."""

from fastapi import APIRouter

from fourthsession.api.housing_agent.service.housing_agent_service import (
    HousingAgentService,
)


class HousingAgentRouter:
    """주택 에이전트 라우터."""

    def __init__(self, service: HousingAgentService) -> None:
        """라우터를 초기화한다.

        Args:
            service (HousingAgentService): 주택 에이전트 서비스.
        """
        self._service = service

    def build(self) -> APIRouter:
        """라우터를 생성해 반환한다.

        Returns:
            APIRouter: 구성된 라우터.
        """
        # TODO: 아래 항목을 연결해 라우터를 구성한다.
        # - HousingApiConstants 값 적용
        # - POST /housing/agent 엔드포인트 등록
        # - HousingAgentRequest/Response 사용
        raise NotImplementedError("TODO: 라우터 구성 구현")
