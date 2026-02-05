# 목적: 채팅 작업 큐를 정의한다.
# 설명: 비동기 잡을 적재/소비하는 인터페이스를 제공한다.
# 디자인 패턴: Repository, Producer-Consumer
# 참조: nextStep.md

"""채팅 작업 큐 모듈."""

from typing import Any


class ChatJobQueue:
    """채팅 작업 큐."""

    def __init__(self, backend: Any | None = None) -> None:
        """큐 의존성을 초기화한다.

        Args:
            backend: 큐 백엔드(예: Redis, 인메모리 큐).
        """
        self._backend = backend

    async def push_job(self, payload: dict[str, Any]) -> str:
        """작업을 큐에 적재한다."""
        _ = payload
        raise NotImplementedError("작업 큐 적재 로직을 구현해야 합니다.")

    async def pop_job(self) -> dict[str, Any] | None:
        """작업을 큐에서 꺼낸다."""
        raise NotImplementedError("작업 큐 소비 로직을 구현해야 합니다.")
