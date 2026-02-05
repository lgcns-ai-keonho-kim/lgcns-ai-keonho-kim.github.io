# 목적: rag 요청 모델을 정의한다.
# 설명: FastAPI 요청 바디 스키마를 명확히 하기 위한 DTO이다.
# 디자인 패턴: DTO
# 참조: thirdsession/api/rag/router/rag_router.py, thirdsession/api/rag/service/rag_service.py

"""rag 요청 모델 모듈."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class RagRequest(BaseModel):
    """rag 요청 모델."""

    question: str = Field(..., description="사용자 질문")
    user_id: str | None = Field(None, description="사용자 식별자(선택)")
    metadata: dict[str, Any] | None = Field(None, description="추가 메타데이터(선택)")

    def todo_extend_fields(self) -> None:
        """요청 필드 확장을 위한 자리표시자."""
        # TODO: 입력 필드를 서비스 요구사항에 맞게 확장한다.
        raise NotImplementedError
