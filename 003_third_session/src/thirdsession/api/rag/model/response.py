# 목적: rag 응답 모델을 정의한다.
# 설명: FastAPI 응답 스키마를 명확히 하기 위한 DTO이다.
# 디자인 패턴: DTO
# 참조: thirdsession/api/rag/router/rag_router.py, thirdsession/api/rag/service/rag_service.py

"""rag 응답 모델 모듈."""

from __future__ import annotations

from pydantic import BaseModel, Field


class RagResponse(BaseModel):
    """rag 응답 모델."""

    answer: str = Field(..., description="최종 답변")
    citations: list[str] = Field(default_factory=list, description="근거 source_id 목록")
    trace_id: str | None = Field(None, description="추적 ID(선택)")

    def todo_extend_fields(self) -> None:
        """응답 필드 확장을 위한 자리표시자."""
        # TODO: 응답 포맷(요약/상세/메타)을 요구사항에 맞게 확장한다.
        raise NotImplementedError
