# 목적: 계획 생성 노드를 정의한다.
# 설명: 사용자 질문과 도구 목록을 바탕으로 실행 계획을 만든다.
# 디자인 패턴: 플래너 패턴
# 참조: fourthsession/core/housing_agent/state

"""계획 생성 노드 모듈."""

from fourthsession.core.housing_agent.state.agent_state import HousingAgentState


class PlanNode:
    """계획 생성 노드."""

    def __call__(self, state: HousingAgentState) -> dict:
        """계획을 생성하고 상태 업데이트를 반환한다.

        Args:
            state (HousingAgentState): 현재 상태.

        Returns:
            dict: 상태 업데이트 딕셔너리.
        """
        # TODO: LLM을 호출해 계획 JSON을 생성한다.
        # - 도구 카드 기반으로 steps 구성
        # - JSON만 출력하도록 강제
        raise NotImplementedError("TODO: 계획 노드 구현")
