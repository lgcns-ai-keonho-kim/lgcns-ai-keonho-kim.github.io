# 목적: 대화 작업 생성 응답 스키마를 정의한다.
# 설명: job_id와 trace_id를 반환해 스트리밍 연결에 사용한다.
# 디자인 패턴: DTO
# 참조: secondsession/api/chat/router/chat_router.py

"""대화 작업 생성 응답 스키마 모듈."""

from pydantic import BaseModel, Field


class ChatJobResponse(BaseModel):
    """대화 작업 생성 응답 스키마."""

    job_id: str = Field(..., description="작업 식별자")
    trace_id: str = Field(..., description="스트리밍 추적 식별자")
    thread_id: str | None = Field(default=None, description="대화 복구용 thread_id")
