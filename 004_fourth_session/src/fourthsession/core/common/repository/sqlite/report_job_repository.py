# 목적: 리포트 작업 레포지토리를 정의한다.
# 설명: 비동기 리포트 작업 생성/조회/갱신을 담당한다.
# 디자인 패턴: 리포지토리 패턴
# 참조: fourthsession/core/repository/sqlite/connection_provider.py

"""리포트 작업 레포지토리 모듈."""

from __future__ import annotations

import json
from datetime import datetime
from uuid import uuid4

from fourthsession.core.repository.sqlite.connection_provider import (
    SqliteConnectionProvider,
)


class ReportJobRepository:
    """리포트 작업 레포지토리."""

    def __init__(self, connection_provider: SqliteConnectionProvider | None = None) -> None:
        """레포지토리를 초기화한다.

        Args:
            connection_provider (SqliteConnectionProvider | None): 연결 제공자.
        """
        self._connection_provider = connection_provider or SqliteConnectionProvider()
        self._initialize_table()

    def create_job(self, payload: dict) -> dict:
        """리포트 작업을 생성한다.

        Args:
            payload (dict): 작업 생성 입력.

        Returns:
            dict: 생성된 작업 정보.
        """
        job_id = f"job-{uuid4()}"
        now = datetime.utcnow().isoformat()
        with self._connection_provider.get_connection() as connection:
            connection.execute(
                """
                INSERT INTO report_jobs (job_id, status, payload, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (job_id, "CREATED", json.dumps(payload, ensure_ascii=False), now, now),
            )
            connection.commit()
        return {"job_id": job_id, "status": "CREATED"}

    def get_job_status(self, job_id: str) -> dict:
        """작업 상태를 조회한다.

        Args:
            job_id (str): 작업 식별자.

        Returns:
            dict: 작업 상태 정보.
        """
        with self._connection_provider.get_connection() as connection:
            cursor = connection.execute(
                "SELECT job_id, status, payload, created_at, updated_at FROM report_jobs WHERE job_id = ?",
                (job_id,),
            )
            row = cursor.fetchone()
        if row is None:
            return {"job_id": job_id, "status": "NOT_FOUND"}
        return {
            "job_id": row["job_id"],
            "status": row["status"],
            "payload": json.loads(row["payload"]),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }

    def update_job_status(self, job_id: str, status: str) -> None:
        """작업 상태를 갱신한다.

        Args:
            job_id (str): 작업 식별자.
            status (str): 변경할 상태.
        """
        now = datetime.utcnow().isoformat()
        with self._connection_provider.get_connection() as connection:
            connection.execute(
                "UPDATE report_jobs SET status = ?, updated_at = ? WHERE job_id = ?",
                (status, now, job_id),
            )
            connection.commit()

    def _initialize_table(self) -> None:
        """리포트 작업 테이블을 생성한다."""
        with self._connection_provider.get_connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS report_jobs (
                    job_id TEXT PRIMARY KEY,
                    status TEXT,
                    payload TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
                """
            )
            connection.commit()
