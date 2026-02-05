# 목적: 주택 작업 스트림 라우터를 정의한다.
# 설명: 스트림 이벤트를 조회한다.
# 디자인 패턴: 라우터 패턴
# 참조: fourthsession/api/housing_agent/service/housing_job_service.py

"""주택 작업 스트림 라우터 모듈."""

from fastapi import APIRouter

from fourthsession.api.housing_agent.service.housing_job_service import HousingJobService


class HousingJobStreamRouter:
    """주택 작업 스트림 라우터."""

    def __init__(self, service: HousingJobService) -> None:
        """라우터를 초기화한다.

        Args:
            service (HousingJobService): 작업 서비스.
        """
        self._service = service

    def build(self) -> APIRouter:
        """라우터를 생성해 반환한다.

        Returns:
            APIRouter: 구성된 라우터.
        """
        # TODO: GET /housing/jobs/{job_id}/stream 엔드포인트를 등록한다.
        # - HousingJobStreamResponse 사용
        # - Redis 스트림은 rpush/lpop 정책 사용
        # - HousingApiConstants.job_stream_path, job_tag 반영
        raise NotImplementedError("TODO: 작업 스트림 라우터 구현")
