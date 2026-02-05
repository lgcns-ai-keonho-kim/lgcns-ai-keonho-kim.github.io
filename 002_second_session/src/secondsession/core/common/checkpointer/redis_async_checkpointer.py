"""참고용 자료: 본 구현에서는 사용하지 않으며, 공식 라이브러리 기반 구현 방향을 정리한다.

AsyncRedisClusterCheckpointSaver - LangGraph용 Redis Cluster 기반 비동기 체크포인트 저장소

이 모듈은 LangGraph의 상태 관리를 위한 Redis Cluster 기반 비동기 체크포인트 저장소를 제공합니다.
Redis Cluster 환경에서 안정적으로 동작하며, TTL 기반 자동 만료 기능을 지원합니다.

주요 기능:
    - Redis Cluster 연결 관리 및 자동 초기화
    - LangGraph 체크포인트의 비동기 저장/조회/삭제
    - TTL 기반 자동 만료 (checkpoint_ttl, latest_ttl)
    - 환경별 설정 지원 (개발/운영)
    - 선택적 암호화 지원

Example:
    기본 사용법::

        # Redis 연결 초기화
        redis_conn = await RedisConnection.create()

        # 체크포인터 생성
        checkpointer = AsyncRedisClusterCheckpointSaver(
            redis_cluster=redis_conn.client,
            checkpoint_ttl=1440,  # 24시간
            latest_ttl=86400      # 1일
        )

        # LangGraph에 적용
        graph = StateGraph(...)
        compiled_graph = graph.compile(checkpointer=checkpointer)
"""

import pickle
from typing import Optional, AsyncIterator
from redis.asyncio.cluster import RedisCluster
from langgraph.checkpoint.base import BaseCheckpointSaver, Checkpoint, CheckpointTuple

class AsyncRedisClusterCheckpointSaver(BaseCheckpointSaver):
    """LangGraph용 Redis Cluster 기반 비동기 체크포인트 저장소

    이 클래스는 LangGraph의 BaseCheckpointSaver를 확장하여 Redis Cluster에
    체크포인트를 저장하고 관리하는 기능을 제공합니다. TTL 기반 자동 만료를 지원합니다.

    Attributes:
        redis (RedisCluster): Redis Cluster 클라이언트 인스턴스
        ttl (int): 기본 TTL 값 (분 단위)
        checkpoint_ttl (int): 체크포인트 데이터의 TTL (분 단위)
        latest_ttl (int): 최신 체크포인트 ID의 TTL (분 단위)

    Example:
        체크포인터 생성 및 사용::

            redis_conn = await RedisConnection.create()
            checkpointer = AsyncRedisClusterCheckpointSaver(
                redis_cluster=redis_conn.client,
                checkpoint_ttl=1440,  # 24시간
                latest_ttl=86400      # 1일
            )

            graph = StateGraph(...)
            compiled_graph = graph.compile(checkpointer=checkpointer)
    """

    def __init__(
        self,
        redis_cluster: RedisCluster,
        ttl: Optional[int] = 1440,
        checkpoint_ttl: Optional[int] = 1440,
        latest_ttl: Optional[int] = 1440,
    ):
        """AsyncRedisClusterCheckpointSaver를 초기화합니다.

        Args:
            redis_cluster (RedisCluster): Redis Cluster 클라이언트 인스턴스
            ttl (Optional[int]): 기본 TTL 값 (분 단위). 기본값은 1440 (24시간)
            checkpoint_ttl (Optional[int]): 체크포인트 데이터의 TTL (분 단위).
                                             지정하지 않으면 ttl 값 사용
            latest_ttl (Optional[int]): 최신 체크포인트 ID의 TTL (분 단위).
                                         지정하지 않으면 ttl 값 사용

        Note:
            - TTL이 None이면 해당 키는 만료되지 않습니다.
            - checkpoint_ttl과 latest_ttl을 다르게 설정하여 최신 참조를 더 오래 유지할 수 있습니다.
        """
        # Redis 클라이언트 할당 (파라미터 우선, 없으면 전역 변수 사용)
        self.redis = redis_cluster
        self.ttl = ttl
        # checkpoint_ttl이 지정되지 않으면 기본 ttl 사용
        self.checkpoint_ttl = checkpoint_ttl or ttl
        # latest_ttl이 지정되지 않으면 기본 ttl 사용
        self.latest_ttl = latest_ttl or ttl

    async def aput(
        self,
        config: dict,
        checkpoint: Checkpoint,
        metadata: dict,
        new_versions: dict | None = None
    ) -> dict:
        """체크포인트를 Redis에 비동기로 저장합니다.

        체크포인트 데이터와 메타데이터를 직렬화하여 Redis에 저장하고,
        최신 체크포인트 ID를 별도 키에 저장합니다.

        Args:
            config (dict): 체크포인트 설정. "configurable.thread_id" 필수
            checkpoint (Checkpoint): 저장할 체크포인트 객체
            metadata (dict): 체크포인트 메타데이터
            new_versions (dict, optional): 새로운 버전 정보. 기본값은 None

        Returns:
            dict: 입력받은 config를 그대로 반환

        Note:
            - Redis 키 형식: "checkpoint:{thread_id}:{checkpoint_id}"
            - 최신 체크포인트 키 형식: "latest:{thread_id}"
            - TTL이 설정되어 있으면 setex로 저장, 없으면 set으로 저장
        """
        # config에서 thread_id와 checkpoint_id 추출
        thread_id = config["configurable"]["thread_id"]
        checkpoint_id = checkpoint["id"]

        # 체크포인트 Redis 키 생성
        key = f"checkpoint:{thread_id}:{checkpoint_id}"
        # 체크포인트 데이터 직렬화 (pickle)
        data = pickle.dumps(
            {
                "checkpoint" : checkpoint,
                "metadata" : metadata,
                "new_versions" : new_versions
            }
        )

        # TTL 설정에 따라 저장 방식 선택
        if self.checkpoint_ttl:
            # TTL이 있으면 만료 시간과 함께 저장
            await self.redis.setex(key, self.checkpoint_ttl, data)
        else:
            # TTL이 없으면 영구 저장
            await self.redis.set(key, data)

        # 최신 체크포인트 ID 저장 키
        latest_key = f"latest:{thread_id}"

        # 최신 체크포인트 ID 저장 (빠른 조회용)
        if self.latest_ttl:
            await self.redis.setex(latest_key, self.latest_ttl, checkpoint_id)
        else:
            await self.redis.set(latest_key, checkpoint_id)

        return config

    async def aput_writes(
        self,
        config: dict,
        writes: dict,
        task_id: str,
    ) -> None:
        """체크포인트 쓰기 작업을 Redis에 비동기로 저장합니다.

        특정 태스크의 쓰기 작업 내역을 직렬화하여 Redis에 저장합니다.
        pending 상태의 체크포인트에 대한 쓰기 작업도 지원합니다.

        Args:
            config (dict): 체크포인트 설정. "configurable.thread_id" 필수
            writes (dict): 저장할 쓰기 작업 데이터
            task_id (str): 태스크 고유 식별자

        Returns:
            None

        Note:
            - Redis 키 형식: "writes:{thread_id}:{checkpoint_id}:{task_id}"
            - checkpoint_id가 없으면 "pending" 사용
            - checkpoint_ttl 설정에 따라 만료 시간 적용
        """
        # config에서 thread_id 추출
        thread_id = config["configurable"]["thread_id"]
        # checkpoint_id가 없으면 "pending" 사용
        checkpoint_id = config["configurable"].get("checkpoint_id", "pending")

        # 쓰기 작업 Redis 키 생성
        writes_key = f"writes:{thread_id}:{checkpoint_id}:{task_id}"
        # 쓰기 작업 데이터 직렬화 (pickle)
        data = pickle.dumps(writes)

        # TTL 설정에 따라 저장 방식 선택
        if self.checkpoint_ttl:
            # TTL이 있으면 만료 시간과 함께 저장
            await self.redis.setex(writes_key, self.checkpoint_ttl, data)

        else:
            # TTL이 없으면 영구 저장
            await self.redis.set(writes_key, data)

    async def aget(
        self,
        config: dict
    ) -> Optional[CheckpointTuple]:
        """체크포인트를 Redis에서 비동기로 조회합니다.

        특정 checkpoint_id를 조회하거나, 지정되지 않은 경우 최신 체크포인트를 반환합니다.

        Args:
            config (dict): 체크포인트 설정
                - "configurable.thread_id" (필수): 스레드 ID
                - "configurable.checkpoint_id" (선택): 특정 체크포인트 ID

        Returns:
            Optional[Checkpoint]: CheckpointTuple 객체 또는 None (없을 경우)

        Note:
            - checkpoint_id가 없으면 "latest:{thread_id}"에서 최신 ID를 조회
            - 최신 체크포인트도 없으면 None 반환
            - bytes 타입의 checkpoint_id는 자동으로 UTF-8 디코딩
        """
        # config에서 thread_id 추출
        thread_id = config["configurable"]["thread_id"]
        checkpoint_id = config["configurable"].get("checkpoint_id")

        # checkpoint_id가 지정되지 않은 경우 최신 체크포인트 ID 조회
        if not checkpoint_id:
            checkpoint_id = await self.redis.get(f"latest:{thread_id}")
            if not checkpoint_id:
                # 최신 체크포인트도 없으면 None 반환
                return None

            # bytes 타입이면 문자열로 디코딩
            if isinstance(checkpoint_id, bytes):
                checkpoint_id = checkpoint_id.decode('utf-8')

        # 체크포인트 Redis 키 생성 및 조회
        key = f"checkpoint:{thread_id}:{checkpoint_id}"
        data = await self.redis.get(key)

        # 데이터가 없으면 None 반환
        if not data:
            return None

        # 직렬화된 데이터 역직렬화 (pickle)
        result = pickle.loads(data)

        # 체크포인트 설정 구성
        checkpoint_config = {
            "configurable" : {
                "thread_id" : thread_id,
                "checkpoint_id" : checkpoint_id
            }
        }

        # CheckpointTuple 객체 반환
        return CheckpointTuple(
            config=checkpoint_config,
            checkpoint=result["checkpoint"],
            metadata=result["metadata"]
        )

    async def alist(
        self,
        config: dict,
        *,
        before: Optional[dict] = None,
        limit: Optional[dict] = None,
        filter: Optional[dict] = None
    ) -> AsyncIterator[CheckpointTuple]:
        """특정 스레드의 체크포인트 목록을 비동기로 조회합니다.

        Redis에서 패턴 매칭을 사용하여 스레드의 모든 체크포인트를 조회하고,
        필터링 및 제한 조건을 적용하여 반환합니다.

        Args:
            config (dict): 체크포인트 설정. "configurable.thread_id" 필수
            before (Optional[dict]): 이 체크포인트 이전의 것만 조회. 기본값은 None
            limit (Optional[dict]): 반환할 최대 개수. 기본값은 None (무제한)
            filter (Optional[dict]): 메타데이터 필터 조건. 기본값은 None

        Yields:
            Iterator[Checkpoint]: CheckpointTuple 객체 이터레이터

        Note:
            - 체크포인트는 ID 기준 내림차순으로 정렬됩니다.
            - before 파라미터가 주어지면 해당 checkpoint_id 이전의 것만 반환
            - filter 파라미터는 메타데이터의 키-값 쌍을 검증하여 일치하는 것만 반환
            - Redis scan_iter를 사용하여 메모리 효율적으로 조회
        """
        # config에서 thread_id 추출
        thread_id = config["configurable"]["thread_id"]
        # 체크포인트 패턴 생성
        pattern = f"checkpoint:{thread_id}:*"

        # Redis에서 패턴에 일치하는 모든 키 조회
        keys = []
        async for key in self.redis.scan_iter(match=pattern):
            keys.append(key)

        # 키 역순 정렬 (최신 체크포인트 우선)
        keys.sort(reverse=True)

        # 반환된 체크포인트 개수 카운터
        count = 0

        # 각 키에 대해 반복
        for key in keys:
            # before 조건 확인 (특정 체크포인트 이전 것만)
            if before:
                checkpoint_id = key.decode('utf-8').split(':')[-1]
                before_checkpoint_id = before.get("configurable", {}).get("checkpoint_id")

                # checkpoint_id가 before_checkpoint_id 이상이면 스킵
                if before_checkpoint_id and checkpoint_id >= before_checkpoint_id:
                    continue

            # 체크포인트 데이터 조회
            data = await self.redis.get(key)

            if data:
                # 데이터 역직렬화
                result = pickle.loads(data)
                checkpoint_id = key.decode('utf-8').split(":")[-1]

                # 체크포인트 설정 구성
                checkpoint_config = {
                    "configurable" : {
                        "thread_id" : thread_id,
                        "checkpoint_id" : checkpoint_id
                    }
                }

            # filter 조건 확인 (메타데이터 필터링)
            if filter:
                metadata = result.get("metadata", {})
                # 모든 필터 조건이 일치하지 않으면 스킵
                if not all(metadata.get(k) == v for k, v in filter.items()):
                    continue

            # CheckpointTuple 반환 (yield)
            yield CheckpointTuple(
                config = checkpoint_config,
                checkpoint = result["checkpoint"],
                metadata = result["metadata"],
                parent_config=None
            )

            # 개수 증가 및 limit 확인
            count += 1
            if limit and count >= limit:
                break

    async def adelete(
        self,
        thread_id: str
    ) -> None:
        """특정 스레드의 모든 체크포인트를 Redis에서 비동기로 삭제합니다.

        주어진 thread_id에 해당하는 모든 체크포인트 데이터와 최신 체크포인트 참조를 삭제합니다.

        Args:
            thread_id (str): 삭제할 스레드의 고유 식별자

        Returns:
            None

        Note:
            - "checkpoint:{thread_id}:*" 패턴에 일치하는 모든 키 삭제
            - "latest:{thread_id}" 키도 함께 삭제
            - 대량의 키를 한 번에 삭제하므로 주의 필요
            - 삭제할 키가 없어도 에러 없이 안전하게 실행됨
        """
        # 체크포인트 패턴 생성
        pattern = f"checkpoint:{thread_id}:*"
        # 패턴에 일치하는 모든 키 조회 (list comprehension with async for)
        keys = [key async for key in self.redis.scan_iter(match=pattern)]
        # 최신 체크포인트 참조 키도 삭제 목록에 추가
        keys.append(f"latest:{thread_id}")

        # 키가 존재하면 일괄 삭제
        if keys:
            await self.redis.delete(*keys)
