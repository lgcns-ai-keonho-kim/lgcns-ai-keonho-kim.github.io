# 목적: Redis 기반 작업 큐를 정의한다.
# 설명: 작업 요청을 리스트에 적재하고 소비한다.
# 디자인 패턴: 큐 패턴
# 참조: fourthsession/core/common/queue/redis_connection_provider.py

"""작업 큐 모듈."""


class RedisJobQueue:
    """Redis 작업 큐."""

    def __init__(self) -> None:
        """작업 큐를 초기화한다."""
        # TODO: RedisConnectionProvider를 주입한다.
        raise NotImplementedError("TODO: 작업 큐 초기화 구현")

    def enqueue(self, payload: dict) -> int:
        """작업을 큐에 적재한다.

        Args:
            payload (dict): 작업 페이로드.

        Returns:
            int: 큐 길이.
        """
        # TODO: Redis 리스트에 rpush로 payload를 적재한다.
        raise NotImplementedError("TODO: 작업 큐 enqueue 구현")

    def dequeue(self) -> dict | None:
        """작업을 큐에서 가져온다.

        Returns:
            dict | None: 작업 페이로드.
        """
        # TODO: Redis 리스트에서 lpop으로 payload를 꺼낸다.
        raise NotImplementedError("TODO: 작업 큐 dequeue 구현")
