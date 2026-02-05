# 목적: 스트리밍 이벤트 큐를 정의한다.
# 설명: 이벤트를 적재/소비하는 인터페이스를 제공한다.
# 디자인 패턴: Repository, Producer-Consumer
# 참조: nextStep.md

"""스트리밍 이벤트 큐 모듈."""

import json
from typing import Any


class ChatStreamEventQueue:
    """스트리밍 이벤트 큐."""

    def __init__(self, backend: Any | None = None, key_prefix: str = "chat:stream") -> None:
        """큐를 초기화한다.

        Args:
            backend: 큐 백엔드(예: Redis).
            key_prefix: job_id별 이벤트 키 접두사.
        """
        self._backend = backend
        self._key_prefix = key_prefix

    async def push_event(self, job_id: str, event: dict[str, Any]) -> None:
        """이벤트를 큐에 적재한다."""
        _ = job_id
        _ = json.dumps(event, ensure_ascii=False)
        raise NotImplementedError("스트리밍 이벤트 적재 로직을 구현해야 합니다.")

    async def pop_event(self, job_id: str) -> dict[str, Any] | None:
        """이벤트를 큐에서 꺼낸다."""
        _ = job_id
        raise NotImplementedError("스트리밍 이벤트 소비 로직을 구현해야 합니다.")
