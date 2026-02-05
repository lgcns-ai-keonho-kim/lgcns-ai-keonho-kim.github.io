# 목적: 주택 에이전트 프롬프트 템플릿을 정의한다.
# 설명: 계획/도구 선택/응답 생성에 필요한 프롬프트를 관리한다.
# 디자인 패턴: 템플릿 메서드 패턴
# 참조: fourthsession/core/housing_agent/graph

"""주택 에이전트 프롬프트 모듈."""


class HousingAgentPrompts:
    """주택 에이전트 프롬프트 모음."""

    def plan_prompt(self) -> str:
        """계획 생성 프롬프트를 반환한다.

        Returns:
            str: 계획 생성용 프롬프트.
        """
        # TODO: 계획 생성에 필요한 지시문을 설계한다.
        # - JSON만 출력하도록 강제
        # - steps/id/action/tool/input 규칙 명시
        raise NotImplementedError("TODO: 계획 프롬프트 구현")

    def tool_selection_prompt(self) -> str:
        """도구 선택 프롬프트를 반환한다.

        Returns:
            str: 도구 선택용 프롬프트.
        """
        # TODO: 도구 선택 규칙을 포함한 프롬프트를 작성한다.
        raise NotImplementedError("TODO: 도구 선택 프롬프트 구현")

    def answer_prompt(self) -> str:
        """응답 생성 프롬프트를 반환한다.

        Returns:
            str: 답변 생성용 프롬프트.
        """
        # TODO: 사용자에게 답변을 생성하기 위한 프롬프트를 작성한다.
        raise NotImplementedError("TODO: 답변 프롬프트 구현")
