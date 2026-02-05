# 목적: 애플리케이션 환경 설정을 정의한다.
# 설명: 환경 변수 기반 설정을 로딩하는 설정 객체이다.
# 디자인 패턴: Configuration Object
# 참조: thirdsession/main.py, thirdsession/core/common/llm_client.py

"""애플리케이션 설정 모듈."""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AppConfig:
    """애플리케이션 설정."""

    openai_api_key: str | None
    google_api_key: str
    redis_url: str | None
    llm_model: str
    llm_temperature: float

    @classmethod
    def from_env(cls) -> "AppConfig":
        """환경 변수에서 설정을 로딩한다.

        Returns:
            AppConfig: 로딩된 설정.
        """
        try:
            from dotenv import load_dotenv

            load_dotenv()
        except ImportError:
            pass

        def require_env(name: str) -> str:
            """필수 환경 변수를 가져온다.

            Args:
                name: 환경 변수 이름.

            Returns:
                str: 환경 변수 값.
            """
            value = os.getenv(name)
            if value is None or value.strip() == "":
                raise ValueError(f"{name} 환경 변수가 필요합니다.")
            return value

        def parse_float(value: str | None) -> float:
            """문자열 값을 float로 변환한다.

            Args:
                value: 변환 대상 문자열.

            Returns:
                float: 변환된 값.
            """
            if value is None or value.strip() == "":
                raise ValueError("LLM_TEMPERATURE 환경 변수가 필요합니다.")
            return float(value)

        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            google_api_key=require_env("GOOGLE_API_KEY"),
            redis_url=os.getenv("REDIS_URL"),
            llm_model=require_env("LLM_MODEL"),
            llm_temperature=parse_float(os.getenv("LLM_TEMPERATURE")),
        )
