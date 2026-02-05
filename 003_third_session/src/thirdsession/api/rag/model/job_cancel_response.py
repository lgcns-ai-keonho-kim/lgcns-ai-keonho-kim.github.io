# 목적: 작업 취소 응답 스키마를 정의한다.
# 설명: 취소 요청 결과를 간단히 반환한다.
# 디자인 패턴: DTO
# 참조: nextStep.md

"""잡 취소 응답 스키마 모듈."""

from pydantic import BaseModel, Field


class JobCancelResponse(BaseModel):
    """작업 취소 응답 스키마."""

    job_id: str = Field(..., description="작업 식별자")
    status: str = Field(..., description="취소 결과 상태")
