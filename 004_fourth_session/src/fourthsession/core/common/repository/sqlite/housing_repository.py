# 목적: 주택 데이터 조회/통계 레포지토리를 정의한다.
# 설명: SQLite 기반의 주택 데이터 접근을 책임진다.
# 디자인 패턴: 리포지토리 패턴
# 참조: fourthsession/core/repository/sqlite/connection_provider.py

"""주택 데이터 레포지토리 모듈."""

from __future__ import annotations

from statistics import mean, median
from typing import Any

from fourthsession.core.repository.sqlite.connection_provider import (
    SqliteConnectionProvider,
)


class HousingRepository:
    """주택 데이터 레포지토리."""

    def __init__(self, connection_provider: SqliteConnectionProvider | None = None) -> None:
        """레포지토리를 초기화한다.

        Args:
            connection_provider (SqliteConnectionProvider | None): 연결 제공자.
        """
        self._connection_provider = connection_provider or SqliteConnectionProvider()

    def list_houses(self, filters: dict) -> list[dict]:
        """필터 조건에 맞는 주택 목록을 조회한다.

        Args:
            filters (dict): 조회 조건.

        Returns:
            list[dict]: 주택 목록.
        """
        where_clause, params = self._build_filters(filters)
        limit = int(filters.get("limit", 10))
        query = f"""
            SELECT
                price,
                area,
                bedrooms,
                bathrooms,
                stories,
                mainroad,
                guestroom,
                basement,
                hotwaterheating,
                airconditioning,
                parking,
                prefarea,
                furnishingstatus
            FROM houses
            {where_clause}
            ORDER BY price ASC
            LIMIT ?
        """
        params.append(limit)
        with self._connection_provider.get_connection() as connection:
            cursor = connection.execute(query, params)
            rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def get_price_stats(self, filters: dict) -> dict:
        """가격 통계 정보를 조회한다.

        Args:
            filters (dict): 통계 대상 조건.

        Returns:
            dict: 통계 결과.
        """
        where_clause, params = self._build_filters(filters)
        query = f"SELECT price FROM houses {where_clause}"
        with self._connection_provider.get_connection() as connection:
            cursor = connection.execute(query, params)
            prices = [row["price"] for row in cursor.fetchall() if row["price"] is not None]
        if not prices:
            return {
                "count": 0,
                "average": None,
                "median": None,
                "min": None,
                "max": None,
            }
        return {
            "count": len(prices),
            "average": round(mean(prices), 2),
            "median": round(median(prices), 2),
            "min": round(min(prices), 2),
            "max": round(max(prices), 2),
        }

    def _build_filters(self, filters: dict) -> tuple[str, list[Any]]:
        """필터 조건에 맞는 WHERE 절을 생성한다."""
        clauses: list[str] = []
        params: list[Any] = []
        if filters.get("min_price") is not None:
            clauses.append("price >= ?")
            params.append(filters["min_price"])
        if filters.get("max_price") is not None:
            clauses.append("price <= ?")
            params.append(filters["max_price"])
        if filters.get("min_area") is not None:
            clauses.append("area >= ?")
            params.append(filters["min_area"])
        if filters.get("max_area") is not None:
            clauses.append("area <= ?")
            params.append(filters["max_area"])
        if filters.get("bedrooms") is not None:
            clauses.append("bedrooms = ?")
            params.append(filters["bedrooms"])
        if not clauses:
            return "", params
        return "WHERE " + " AND ".join(clauses), params
