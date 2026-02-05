# 목적: 공통 Tool 인터페이스를 정의한다.
# 설명: 입력/출력 스키마와 실행 규약을 표준화한다.
# 디자인 패턴: 템플릿 메서드 패턴
# 참조: fourthsession/mcp/tool_registry.py

"""공통 Tool 인터페이스 모듈."""

from abc import ABC, abstractmethod


class BaseTool(ABC):
    """모든 Tool이 따라야 하는 기본 인터페이스."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool 이름을 반환한다."""
        raise NotImplementedError("Tool 이름 구현이 필요합니다.")

    @property
    @abstractmethod
    def description(self) -> str:
        """Tool 설명을 반환한다."""
        raise NotImplementedError("Tool 설명 구현이 필요합니다.")

    @property
    @abstractmethod
    def input_schema(self) -> dict:
        """입력 스키마를 반환한다."""
        raise NotImplementedError("입력 스키마 구현이 필요합니다.")

    @abstractmethod
    def execute(self, payload: dict) -> dict:
        """Tool을 실행한다.

        Args:
            payload (dict): 입력 데이터.

        Returns:
            dict: 실행 결과.
        """
        raise NotImplementedError("Tool 실행 구현이 필요합니다.")
