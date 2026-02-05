# 목적: 주택 에이전트 서비스 레이어를 정의한다.
# 설명: 요청을 받아 에이전트 실행을 조정하고 응답을 만든다.
# 디자인 패턴: 애플리케이션 서비스 패턴
# 참조: fourthsession/core/housing_agent/graph

"""주택 에이전트 서비스 모듈."""

from fourthsession.api.housing_agent.model.request import HousingAgentRequest
from fourthsession.api.housing_agent.model.response import HousingAgentResponse


class HousingAgentService:
    """주택 에이전트 서비스."""

    def handle(self, request: HousingAgentRequest) -> HousingAgentResponse:
        """요청을 처리하고 응답을 반환한다.

        Args:
            request (HousingAgentRequest): 요청 모델.

        Returns:
            HousingAgentResponse: 응답 모델.
        """
        # TODO: 그래프 실행 및 결과 매핑을 구현한다.
        # - HousingToolRegistry로 도구를 등록한다.
        # - HousingAgentGraphBuilder로 그래프를 빌드/컴파일한다.
        # - HousingAgentState 초기값을 만들고 invoke 결과를 응답으로 매핑한다.
        raise NotImplementedError("TODO: 서비스 처리 구현")
