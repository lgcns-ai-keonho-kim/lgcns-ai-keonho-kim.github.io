# 목적: SQLite 연결 제공자를 정의한다.
# 설명: DB 연결 생성과 관리 책임을 캡슐화한다.
# 디자인 패턴: 팩토리 메서드 패턴
# 참조: fourthsession/core/repository/sqlite/housing_repository.py

"""SQLite 연결 제공자 모듈."""

import csv
import sqlite3
from pathlib import Path


class SqliteConnectionProvider:
    """SQLite 연결 제공자."""

    def __init__(self, db_path: str | None = None, csv_path: str | None = None) -> None:
        """연결 제공자 설정을 초기화한다.

        Args:
            db_path (str | None): DB 파일 경로.
            csv_path (str | None): CSV 파일 경로.
        """
        self._db_path = Path(db_path) if db_path else self._resolve_db_path()
        self._csv_path = Path(csv_path) if csv_path else self._resolve_csv_path()

    def get_connection(self) -> sqlite3.Connection:
        """SQLite 연결을 반환한다.

        Returns:
            sqlite3.Connection: 데이터베이스 연결 객체.
        """
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self._db_path.as_posix())
        connection.row_factory = sqlite3.Row
        self._initialize_housing_table(connection)
        return connection

    def _resolve_db_path(self) -> Path:
        """프로젝트 루트의 기본 DB 경로를 계산한다."""
        project_root = self._find_project_root()
        return project_root / "data" / "housing.db"

    def _resolve_csv_path(self) -> Path:
        """프로젝트 루트의 기본 CSV 경로를 계산한다."""
        project_root = self._find_project_root()
        return project_root / "data" / "housing.csv"

    def _find_project_root(self) -> Path:
        """src 폴더 기준으로 프로젝트 루트를 찾는다."""
        current = Path(__file__).resolve()
        for parent in current.parents:
            if parent.name == "src":
                return parent.parent
        return current.parent

    def _initialize_housing_table(self, connection: sqlite3.Connection) -> None:
        """주택 테이블을 초기화하고 데이터가 없으면 CSV를 적재한다."""
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS houses (
                price REAL,
                area REAL,
                bedrooms INTEGER,
                bathrooms INTEGER,
                stories INTEGER,
                mainroad TEXT,
                guestroom TEXT,
                basement TEXT,
                hotwaterheating TEXT,
                airconditioning TEXT,
                parking INTEGER,
                prefarea TEXT,
                furnishingstatus TEXT
            )
            """
        )
        cursor.execute("SELECT COUNT(*) AS count FROM houses")
        count = cursor.fetchone()["count"]
        if count == 0:
            self._load_csv(connection)
        connection.commit()

    def _load_csv(self, connection: sqlite3.Connection) -> None:
        """CSV 데이터를 houses 테이블로 적재한다."""
        if not self._csv_path.exists():
            return
        with self._csv_path.open("r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            rows = [self._normalize_row(row) for row in reader]
        if not rows:
            return
        placeholders = ",".join(["?"] * len(rows[0]))
        columns = ",".join(rows[0].keys())
        query = f"INSERT INTO houses ({columns}) VALUES ({placeholders})"
        connection.executemany(query, [tuple(row.values()) for row in rows])

    def _normalize_row(self, row: dict) -> dict:
        """CSV 행을 SQLite 적재 형식으로 변환한다."""
        def to_number(value: str) -> float | None:
            if value is None or value == "":
                return None
            return float(value)

        return {
            "price": to_number(row.get("price")),
            "area": to_number(row.get("area")),
            "bedrooms": self._to_int(row.get("bedrooms")),
            "bathrooms": self._to_int(row.get("bathrooms")),
            "stories": self._to_int(row.get("stories")),
            "mainroad": row.get("mainroad"),
            "guestroom": row.get("guestroom"),
            "basement": row.get("basement"),
            "hotwaterheating": row.get("hotwaterheating"),
            "airconditioning": row.get("airconditioning"),
            "parking": self._to_int(row.get("parking")),
            "prefarea": row.get("prefarea"),
            "furnishingstatus": row.get("furnishingstatus"),
        }

    def _to_int(self, value: str | None) -> int | None:
        """정수 변환을 안전하게 수행한다."""
        if value is None or value == "":
            return None
        return int(float(value))
