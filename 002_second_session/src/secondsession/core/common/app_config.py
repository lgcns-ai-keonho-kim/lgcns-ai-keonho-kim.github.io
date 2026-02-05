# 목적: 애플리케이션 LLM/인프라 설정을 정의한다.
# 설명: 환경 변수 기반으로 모델명/타임아웃/키/Redis 정보를 로딩한다.
# 디자인 패턴: Configuration Object
# 참조: secondsession/main.py, secondsession/core/common/llm_client.py,
#       secondsession/core/common/checkpointer/redis_checkpointer.py

"""애플리케이션 설정 모듈."""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AppConfig:
    """애플리케이션 설정."""

    openai_api_key: str | None
    llm_model: str
    llm_temperature: float
    llm_timeout: float
    redis_url: str | None

    @classmethod
    def from_env(cls) -> "AppConfig":
        """환경 변수에서 설정을 로딩한다."""
        try:
            from dotenv import load_dotenv

            load_dotenv()
        except ImportError:
            pass

        def parse_float(value: str | None, default: float) -> float:
            """문자열 값을 float로 변환한다."""
            if value is None or value.strip() == "":
                return default
            return float(value)

        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            llm_model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
            llm_temperature=parse_float(os.getenv("LLM_TEMPERATURE"), 0.0),
            llm_timeout=parse_float(os.getenv("LLM_TIMEOUT"), 30.0),
            redis_url=os.getenv("REDIS_URL"),
        )
