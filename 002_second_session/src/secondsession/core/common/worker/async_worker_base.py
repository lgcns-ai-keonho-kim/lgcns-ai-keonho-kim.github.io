# 목적: 비동기 워커 실행 루프의 공통 흐름을 정의한다.
# 설명: 비동기 큐 폴링과 작업 처리 흐름을 템플릿 메서드로 제공한다.
# 디자인 패턴: Template Method
# 참조: secondsession/core/chat/worker/chat_worker.py

"""비동기 워커 베이스 모듈."""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod


class AsyncWorkerBase(ABC):
    """비동기 큐 기반 워커의 공통 실행 흐름을 제공하는 베이스 클래스."""

    def __init__(self, poll_interval: float = 0.1) -> None:
        """워커를 초기화한다.

        Args:
            poll_interval: 큐 폴링 간격(초).
        """
        self._poll_interval = poll_interval

    async def run_forever(self) -> None:
        """워커를 비동기 루프 형태로 실행한다.

        TODO:
            - 종료 신호를 위한 정책(예: stop 플래그)을 정의한다.
            - 예외 발생 시 재시도/백오프 정책을 정의한다.
        """
        _ = asyncio
        raise NotImplementedError("비동기 워커 실행 루프를 구현해야 합니다.")

    @abstractmethod
    async def _dequeue_job(self) -> dict | None:
        """큐에서 작업을 꺼낸다.

        Returns:
            작업 dict 또는 None.
        """

    @abstractmethod
    async def _process_job(self, job: dict) -> None:
        """단일 작업을 처리한다.

        Args:
            job: 큐에서 꺼낸 작업 페이로드.
        """
