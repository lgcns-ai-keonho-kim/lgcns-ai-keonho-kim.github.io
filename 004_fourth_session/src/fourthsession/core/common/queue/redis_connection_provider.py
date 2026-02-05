# 목적: Redis 연결 제공자를 정의한다.
# 설명: 환경 변수 기반으로 Redis 클라이언트를 생성한다.
# 디자인 패턴: 팩토리 메서드 패턴
# 참조: fourthsession/core/common/queue/job_queue.py

"""Redis 연결 제공자 모듈."""

import redis


class RedisConnectionProvider:
    """Redis 연결 제공자."""

    def __init__(self, host: str | None = None, port: int | None = None, db: int | None = None) -> None:
        """연결 정보를 초기화한다.

        Args:
            host (str | None): Redis 호스트.
            port (int | None): Redis 포트.
            db (int | None): Redis DB 인덱스.
        """
        # TODO: 환경 변수 기반 기본값을 설정한다.
        raise NotImplementedError("TODO: Redis 연결 설정 구현")

    def get_client(self) -> redis.Redis:
        """Redis 클라이언트를 반환한다.

        Returns:
            redis.Redis: Redis 클라이언트.
        """
        # TODO: redis.Redis 인스턴스를 생성한다.
        raise NotImplementedError("TODO: Redis 클라이언트 생성 구현")
