# 목적: 주택 작업 생성 요청 모델을 정의한다.
# 설명: 작업 큐에 적재할 입력 스키마를 제공한다.
# 디자인 패턴: 데이터 전송 객체(DTO)
# 참조: fourthsession/api/housing_agent/service/housing_job_service.py

"""주택 작업 요청 모델 모듈."""

from pydantic import BaseModel, Field


class HousingJobRequest(BaseModel):
    """주택 작업 생성 요청 모델."""

    question: str = Field(description="사용자 질문")
    trace_id: str | None = Field(default=None, description="추적 식별자")
    preferred_tools: list[str] | None = Field(default=None, description="우선 사용 도구 목록")
    max_steps: int | None = Field(default=None, description="최대 실행 단계 수")
