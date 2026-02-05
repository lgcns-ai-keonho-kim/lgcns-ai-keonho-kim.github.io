# 목적: 작업 상태 조회 응답 스키마를 정의한다.
# 설명: 비동기 실행 상태를 간단히 반환한다.
# 디자인 패턴: DTO
# 참조: nextStep.md

"""잡 상태 응답 스키마 모듈."""

from pydantic import BaseModel, Field


class JobStatusResponse(BaseModel):
    """작업 상태 응답 스키마."""

    job_id: str = Field(..., description="작업 식별자")
    status: str = Field(..., description="작업 상태")
    last_seq: int | None = Field(default=None, description="마지막 이벤트 순서")
