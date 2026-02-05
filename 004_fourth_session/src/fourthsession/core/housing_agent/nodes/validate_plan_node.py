# 목적: 계획 검증 노드를 정의한다.
# 설명: 계획 스키마와 도구 일치 여부를 확인한다.
# 디자인 패턴: 밸리데이터 패턴
# 참조: fourthsession/core/housing_agent/state

"""계획 검증 노드 모듈."""

from fourthsession.core.housing_agent.state.agent_state import HousingAgentState


class ValidatePlanNode:
    """계획 검증 노드."""

    def __call__(self, state: HousingAgentState) -> dict:
        """계획 검증 결과를 상태 업데이트로 반환한다.

        Args:
            state (HousingAgentState): 현재 상태.

        Returns:
            dict: 상태 업데이트 딕셔너리.
        """
        # TODO: 계획 스키마, 도구 존재 여부, 정책을 검증한다.
        # - 실패 시 errors 누적 + retry_count 증가
        raise NotImplementedError("TODO: 계획 검증 노드 구현")
