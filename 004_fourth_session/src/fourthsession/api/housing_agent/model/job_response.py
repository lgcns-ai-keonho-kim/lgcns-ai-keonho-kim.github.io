# 목적: 주택 작업 생성 응답 모델을 정의한다.
# 설명: 작업 식별자와 상태를 반환한다.
# 디자인 패턴: 데이터 전송 객체(DTO)
# 참조: fourthsession/api/housing_agent/service/housing_job_service.py

"""주택 작업 응답 모델 모듈."""

from pydantic import BaseModel, Field


class HousingJobResponse(BaseModel):
    """주택 작업 생성 응답 모델."""

    job_id: str = Field(description="작업 식별자")
    status: str = Field(description="작업 상태")
    trace_id: str | None = Field(default=None, description="추적 식별자")
