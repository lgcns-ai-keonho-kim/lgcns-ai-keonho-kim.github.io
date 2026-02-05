# 목적: MCP Tool 레지스트리를 정의한다.
# 설명: 등록된 Tool 정보를 관리하고 도구 카드를 제공한다.
# 디자인 패턴: 레지스트리 패턴
# 참조: fourthsession/core/common/tools/base_tool.py

"""MCP Tool 레지스트리 모듈."""


class HousingToolRegistry:
    """주택 에이전트 Tool 레지스트리."""

    def register_tools(self) -> None:
        """Tool 목록을 등록한다."""
        # TODO: Tool 인스턴스를 생성하고 레지스트리에 등록한다.
        raise NotImplementedError("TODO: Tool 등록 구현")

    def list_tool_cards(self) -> list[dict]:
        """도구 카드 목록을 반환한다.

        Returns:
            list[dict]: 도구 카드 목록.
        """
        # TODO: 스키마/힌트/예시를 포함한 도구 카드 생성 로직을 구현한다.
        raise NotImplementedError("TODO: 도구 카드 목록 구현")

    def get_tool(self, name: str):
        """이름으로 Tool을 조회한다."""
        # TODO: Tool 이름으로 인스턴스를 반환한다.
        raise NotImplementedError("TODO: Tool 조회 구현")
