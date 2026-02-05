# 목적: 대화 작업 큐를 정의한다.
# 설명: Redis 리스트 기반으로 작업을 적재/소비한다.
# 디자인 패턴: Repository, Producer-Consumer
# 참조: docs/02_backend_service_layer/04_Redis_캐시_rpush_lpop.md

"""대화 작업 큐 모듈."""

import json
from typing import Any


class ChatJobQueue:
    """대화 작업 큐."""

    def __init__(self, redis_client: Any, key: str = "chat:jobs") -> None:
        """큐를 초기화한다.

        Args:
            redis_client: Redis 클라이언트.
            key: 작업 큐 키.
        """
        self._redis = redis_client
        self._key = key

    async def enqueue(self, payload: dict) -> None:
        """작업을 큐에 적재한다.

        TODO:
            - payload 필수 필드(job_id, trace_id, thread_id, query)를 검증한다.
            - JSON 문자열로 직렬화한다(UTF-8, ensure_ascii=False).
            - rpush로 큐에 적재한다.
            - 직렬화 실패/Redis 오류 정책을 정의한다(로깅/예외).
        """
        _ = json.dumps(payload, ensure_ascii=False)
        raise NotImplementedError("대화 작업 큐 적재 로직을 구현해야 합니다.")

    async def dequeue(self) -> dict | None:
        """작업을 큐에서 꺼낸다.

        TODO:
            - lpop으로 큐에서 하나를 가져온다.
            - 값이 없으면 None을 반환한다.
            - JSON을 dict로 역직렬화한다.
            - 역직렬화 실패 시 스킵/로깅 규칙을 정의한다.
            - 필수 필드가 없으면 에러 처리 정책을 정의한다.
        """
        raise NotImplementedError("대화 작업 큐 소비 로직을 구현해야 합니다.")
