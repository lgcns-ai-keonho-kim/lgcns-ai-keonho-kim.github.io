# 목적: 주택 가격 통계 Tool을 정의한다.
# 설명: 필터 조건에 맞는 가격 통계를 계산한다.
# 디자인 패턴: 커맨드 패턴
# 참조: fourthsession/core/repository/sqlite/housing_repository.py

"""주택 가격 통계 Tool 모듈."""

from fourthsession.core.common.tools.base_tool import BaseTool


class HousingPriceStatsTool(BaseTool):
    """주택 가격 통계 Tool."""

    @property
    def name(self) -> str:
        """Tool 이름을 반환한다."""
        # TODO: Tool 이름을 고정 값으로 반환한다.
        raise NotImplementedError("TODO: Tool 이름 구현")

    @property
    def description(self) -> str:
        """Tool 설명을 반환한다."""
        # TODO: Tool 설명을 반환한다.
        raise NotImplementedError("TODO: Tool 설명 구현")

    @property
    def input_schema(self) -> dict:
        """입력 스키마를 반환한다."""
        # TODO: 입력 스키마를 딕셔너리로 반환한다.
        raise NotImplementedError("TODO: 입력 스키마 구현")

    @property
    def example_request(self) -> dict:
        """예시 요청을 반환한다."""
        # TODO: 예시 요청을 구성한다.
        raise NotImplementedError("TODO: 예시 요청 구현")

    @property
    def example_response(self) -> dict:
        """예시 응답을 반환한다."""
        # TODO: 예시 응답을 구성한다.
        raise NotImplementedError("TODO: 예시 응답 구현")

    @property
    def hints(self) -> dict:
        """도구 힌트를 반환한다."""
        # TODO: 필드별 입력 힌트를 정의한다.
        raise NotImplementedError("TODO: 힌트 구현")

    def execute(self, payload: dict) -> dict:
        """Tool을 실행한다.

        Args:
            payload (dict): 입력 데이터.

        Returns:
            dict: 실행 결과.
        """
        # TODO: HousingRepository.get_price_stats를 호출한다.
        raise NotImplementedError("TODO: Tool 실행 구현")
