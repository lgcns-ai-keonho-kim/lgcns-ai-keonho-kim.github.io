# 목적: 주택 작업 서비스 레이어를 정의한다.
# 설명: 작업 생성/취소/상태 조회/스트림 조회를 담당한다.
# 디자인 패턴: 애플리케이션 서비스 패턴
# 참조: fourthsession/core/common/queue

"""주택 작업 서비스 모듈."""

from __future__ import annotations

from fourthsession.api.housing_agent.model.job_cancel_response import (
    HousingJobCancelResponse,
)
from fourthsession.api.housing_agent.model.job_request import HousingJobRequest
from fourthsession.api.housing_agent.model.job_response import HousingJobResponse
from fourthsession.api.housing_agent.model.job_status_response import (
    HousingJobStatusResponse,
)
from fourthsession.api.housing_agent.model.job_stream_response import (
    HousingJobStreamResponse,
)


class HousingJobService:
    """주택 작업 서비스."""

    def __init__(self) -> None:
        """서비스를 초기화한다."""
        # TODO: RedisJobQueue, RedisStreamEventQueue, InMemoryJobStore를 주입한다.
        raise NotImplementedError("TODO: 작업 서비스 초기화 구현")

    def create_job(self, request: HousingJobRequest) -> HousingJobResponse:
        """작업을 생성한다.

        Args:
            request (HousingJobRequest): 작업 생성 요청.

        Returns:
            HousingJobResponse: 작업 생성 응답.
        """
        # TODO: job_id/trace_id 생성 → 작업 저장소 저장 → Redis 큐 rpush.
        raise NotImplementedError("TODO: 작업 생성 구현")

    def cancel_job(self, job_id: str) -> HousingJobCancelResponse:
        """작업을 취소한다.

        Args:
            job_id (str): 작업 식별자.

        Returns:
            HousingJobCancelResponse: 취소 응답.
        """
        # TODO: 작업 상태를 CANCELLED로 갱신한다.
        raise NotImplementedError("TODO: 작업 취소 구현")

    def get_status(self, job_id: str) -> HousingJobStatusResponse:
        """작업 상태를 조회한다.

        Args:
            job_id (str): 작업 식별자.

        Returns:
            HousingJobStatusResponse: 상태 응답.
        """
        # TODO: 작업 저장소에서 상태 조회 후 응답한다.
        raise NotImplementedError("TODO: 작업 상태 조회 구현")

    def stream(self, job_id: str) -> HousingJobStreamResponse:
        """스트림 이벤트를 조회한다.

        Args:
            job_id (str): 작업 식별자.

        Returns:
            HousingJobStreamResponse: 스트림 응답.
        """
        # TODO: Redis 스트림 리스트에서 lpop으로 이벤트를 가져온다.
        raise NotImplementedError("TODO: 스트림 조회 구현")
