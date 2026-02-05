# 목적: 스트리밍 이벤트 큐를 정의한다.
# 설명: Redis 리스트 기반으로 이벤트를 적재/소비한다.
# 디자인 패턴: Repository, Producer-Consumer
# 참조: docs/02_backend_service_layer/04_Redis_캐시_rpush_lpop.md

"""스트리밍 이벤트 큐 모듈."""

import json
from typing import Any


class ChatStreamEventQueue:
    """스트리밍 이벤트 큐."""

    def __init__(self, redis_client: Any, key_prefix: str = "chat:stream") -> None:
        """큐를 초기화한다.

        Args:
            redis_client: Redis 클라이언트.
            key_prefix: job_id별 이벤트 키 접두사.
        """
        self._redis = redis_client
        self._key_prefix = key_prefix

    async def push_event(self, job_id: str, event: dict) -> None:
        """이벤트를 큐에 적재한다.

        TODO:
            - job_id별 키를 생성한다(f\"{key_prefix}:{job_id}\").
            - event 필수 필드(type, trace_id, seq)를 검증한다.
            - event를 JSON 문자열로 직렬화한다(UTF-8, ensure_ascii=False).
            - rpush로 이벤트를 적재한다.
            - seq 단조 증가 규칙을 보장한다(워커 측에서 증가).
        """
        _ = job_id
        _ = json.dumps(event, ensure_ascii=False)
        raise NotImplementedError("스트리밍 이벤트 적재 로직을 구현해야 합니다.")

    async def pop_event(self, job_id: str) -> dict | None:
        """이벤트를 큐에서 꺼낸다.

        TODO:
            - job_id별 키를 생성한다.
            - lpop으로 이벤트를 소비한다.
            - 값이 없으면 None을 반환한다.
            - JSON을 dict로 역직렬화한다.
            - 역직렬화 실패 시 스킵/로깅 규칙을 정의한다.
        """
        _ = job_id
        raise NotImplementedError("스트리밍 이벤트 소비 로직을 구현해야 합니다.")
