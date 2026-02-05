# 목적: 주택 데이터 조회/통계 레포지토리를 정의한다.
# 설명: SQLite 기반의 주택 데이터 접근을 책임진다.
# 디자인 패턴: 리포지토리 패턴
# 참조: fourthsession/core/repository/sqlite/connection_provider.py

"""주택 데이터 레포지토리 모듈."""


class HousingRepository:
    """주택 데이터 레포지토리."""

    def list_houses(self, filters: dict) -> list[dict]:
        """필터 조건에 맞는 주택 목록을 조회한다.

        Args:
            filters (dict): 조회 조건.

        Returns:
            list[dict]: 주택 목록.
        """
        # TODO: 필터 조건에 맞는 SQL을 구성하고 실행한다.
        raise NotImplementedError("TODO: 주택 목록 조회 구현")

    def get_price_stats(self, filters: dict) -> dict:
        """가격 통계 정보를 조회한다.

        Args:
            filters (dict): 통계 대상 조건.

        Returns:
            dict: 통계 결과.
        """
        # TODO: 평균/중앙값/최소/최대 통계를 계산한다.
        raise NotImplementedError("TODO: 가격 통계 조회 구현")
