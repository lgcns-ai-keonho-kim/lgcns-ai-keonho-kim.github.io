# 목적: LangChain 기반 LLM 클라이언트를 구성한다.
# 설명: 설정을 기반으로 ChatOpenAI 인스턴스를 생성하고 보관한다.
# 디자인 패턴: Factory Method
# 참조: secondsession/core/common/app_config.py, secondsession/main.py

"""LLM 클라이언트 모듈."""

from __future__ import annotations

import os

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI

from secondsession.core.common.app_config import AppConfig


class LlmClient:
    """LangChain LLM 클라이언트."""

    def __init__(self, config: AppConfig) -> None:
        """LLM 클라이언트를 초기화한다.

        Args:
            config: 애플리케이션 설정.
        """
        self._config = config
        self._chat_model = self._build_chat_model()

    def chat_model(self) -> BaseChatModel:
        """Chat 모델 인스턴스를 반환한다.

        Returns:
            BaseChatModel: LangChain Chat 모델.
        """
        return self._chat_model

    def _build_chat_model(self) -> BaseChatModel:
        """ChatOpenAI 인스턴스를 생성한다.

        Returns:
            BaseChatModel: ChatOpenAI 기반 모델.
        """
        if self._config.openai_api_key:
            os.environ.setdefault("OPENAI_API_KEY", self._config.openai_api_key)

        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY 환경 변수가 필요합니다.")

        return ChatOpenAI(
            model=self._config.llm_model,
            temperature=self._config.llm_temperature,
            timeout=self._config.llm_timeout,
        )
