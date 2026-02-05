# 목적: 주택 에이전트 API 상수를 정의한다.
# 설명: 라우팅 경로, 태그, 버전 같은 값을 정리한다.
# 디자인 패턴: 상수 객체 패턴
# 참조: fourthsession/api/housing_agent/router

"""주택 에이전트 API 상수 모듈."""


class HousingApiConstants:
    """주택 에이전트 API 상수."""

    def __init__(self) -> None:
        """상수 값을 초기화한다."""
        # TODO: 아래 항목을 프로젝트 정책에 맞게 채운다.
        # - api_prefix: 예) "/api/v1"
        # - agent_path: 예) "/housing/agent"
        # - job_path: 예) "/housing/jobs"
        # - job_cancel_path: 예) "/housing/jobs/{job_id}/cancel"
        # - job_status_path: 예) "/housing/jobs/{job_id}/status"
        # - job_stream_path: 예) "/housing/jobs/{job_id}/stream"
        # - tag / job_tag: 라우터 태그
        raise NotImplementedError("TODO: API 상수 정의 구현")
