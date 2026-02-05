# 목적: 결과 합성 노드를 정의한다.
# 설명: 여러 도구 결과를 하나의 응답 데이터로 합성한다.
# 디자인 패턴: 머저 패턴
# 참조: fourthsession/core/housing_agent/state

"""결과 합성 노드 모듈."""

from fourthsession.core.housing_agent.state.agent_state import HousingAgentState


class MergeResultNode:
    """결과 합성 노드."""

    def __call__(self, state: HousingAgentState) -> dict:
        """합성 결과를 상태 업데이트로 반환한다.

        Args:
            state (HousingAgentState): 현재 상태.

        Returns:
            dict: 상태 업데이트 딕셔너리.
        """
        # TODO: 도구 결과를 합성하고 답변 생성에 필요한 구조를 만든다.
        raise NotImplementedError("TODO: 합성 노드 구현")
