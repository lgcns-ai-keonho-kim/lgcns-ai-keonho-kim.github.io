# 목적: 주택 에이전트 MCP 서버를 정의한다.
# 설명: MCP 서버 생성과 실행 책임을 캡슐화한다.
# 디자인 패턴: 팩토리 메서드 패턴
# 참조: fourthsession/mcp/tool_registry.py

"""주택 에이전트 MCP 서버 모듈."""

from mcp.server.fastmcp import FastMCP

from fourthsession.mcp.tool_registry import HousingToolRegistry


class HousingMcpServer:
    """주택 에이전트 MCP 서버."""

    def __init__(self, registry: HousingToolRegistry | None = None) -> None:
        """MCP 서버 구성 객체를 초기화한다.

        Args:
            registry (HousingToolRegistry | None): 도구 레지스트리.
        """
        self._registry = registry or HousingToolRegistry()

    def build(self) -> FastMCP:
        """MCP 서버 인스턴스를 구성한다.

        Returns:
            FastMCP: MCP 서버 인스턴스.
        """
        # TODO: Tool 등록과 정책 설정을 포함한 MCP 서버를 구성한다.
        # - FastMCP 인스턴스를 만든다.
        # - @mcp.tool()로 Tool을 등록한다.
        raise NotImplementedError("TODO: MCP 서버 구성 구현")

    def run(self) -> None:
        """MCP 서버를 실행한다."""
        # TODO: 전송 방식(stdio/http)을 선택하고 서버를 기동한다.
        raise NotImplementedError("TODO: MCP 서버 실행 구현")
