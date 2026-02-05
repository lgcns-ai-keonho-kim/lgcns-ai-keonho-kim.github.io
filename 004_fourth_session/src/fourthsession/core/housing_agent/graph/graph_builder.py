# 목적: 주택 에이전트 그래프를 구성한다.
# 설명: LangGraph의 StateGraph를 빌드하는 책임을 가진다.
# 디자인 패턴: 빌더 패턴
# 참조: fourthsession/core/housing_agent/nodes, fourthsession/core/housing_agent/state

"""주택 에이전트 그래프 빌더 모듈."""

from langgraph.graph import StateGraph

from fourthsession.core.housing_agent.state.agent_state import HousingAgentState


class HousingAgentGraphBuilder:
    """주택 에이전트 그래프 빌더."""

    def build(self) -> StateGraph:
        """그래프를 구성해 반환한다.

        Returns:
            StateGraph: 구성된 LangGraph 그래프.
        """
        # TODO: 노드 추가, 엣지 연결, 시작/종료 노드 구성을 구현한다.
        # - Plan → Validate → Execute → Merge → Feedback → End
        raise NotImplementedError("TODO: 그래프 빌더 구현")
