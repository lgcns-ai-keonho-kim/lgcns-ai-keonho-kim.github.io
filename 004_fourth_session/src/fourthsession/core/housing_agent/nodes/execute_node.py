# 목적: 도구 실행 노드를 정의한다.
# 설명: 계획에 포함된 도구를 호출하고 결과를 저장한다.
# 디자인 패턴: 커맨드 패턴
# 참조: fourthsession/core/housing_agent/state

"""도구 실행 노드 모듈."""

from fourthsession.core.housing_agent.state.agent_state import HousingAgentState


class ExecuteNode:
    """도구 실행 노드."""

    def __call__(self, state: HousingAgentState) -> dict:
        """도구 실행 결과를 상태 업데이트로 반환한다.

        Args:
            state (HousingAgentState): 현재 상태.

        Returns:
            dict: 상태 업데이트 딕셔너리.
        """
        # TODO: 계획에 포함된 도구를 순차/병렬로 실행한다.
        # - ToolRegistry에서 Tool을 조회
        # - 실패 시 errors 누적
        raise NotImplementedError("TODO: 실행 노드 구현")
