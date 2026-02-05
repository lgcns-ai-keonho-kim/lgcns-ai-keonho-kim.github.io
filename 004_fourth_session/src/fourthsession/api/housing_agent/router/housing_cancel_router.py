# 목적: 주택 작업 취소 라우터를 정의한다.
# 설명: 작업 취소 요청을 서비스로 전달한다.
# 디자인 패턴: 라우터 패턴
# 참조: fourthsession/api/housing_agent/service/housing_job_service.py

"""주택 작업 취소 라우터 모듈."""

from fastapi import APIRouter

from fourthsession.api.housing_agent.service.housing_job_service import HousingJobService


class HousingJobCancelRouter:
    """주택 작업 취소 라우터."""

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
        # TODO: POST /housing/jobs/{job_id}/cancel 엔드포인트를 등록한다.
        # - HousingJobCancelResponse 사용
        # - HousingApiConstants.job_cancel_path, job_tag 반영
        raise NotImplementedError("TODO: 작업 취소 라우터 구현")
