# 목적: SQLite 연결 제공자를 정의한다.
# 설명: DB 연결 생성과 관리 책임을 캡슐화한다.
# 디자인 패턴: 팩토리 메서드 패턴
# 참조: fourthsession/core/repository/sqlite/housing_repository.py

"""SQLite 연결 제공자 모듈."""

import sqlite3


class SqliteConnectionProvider:
    """SQLite 연결 제공자."""

    def get_connection(self) -> sqlite3.Connection:
        """SQLite 연결을 반환한다.

        Returns:
            sqlite3.Connection: 데이터베이스 연결 객체.
        """
        # TODO: DB 경로와 연결 옵션을 설정해 연결을 생성한다.
        # - data/housing.db 생성
        # - CSV → SQLite 초기 적재 (중복 방지)
        raise NotImplementedError("TODO: SQLite 연결 생성 구현")
