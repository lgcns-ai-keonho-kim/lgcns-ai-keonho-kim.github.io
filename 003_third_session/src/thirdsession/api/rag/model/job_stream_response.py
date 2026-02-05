# 목적: 잡 스트리밍 응답 스키마를 정의한다.
# 설명: 스트리밍 이벤트의 표준 형태를 고정한다.
# 디자인 패턴: DTO
# 참조: docs/04_rag_pipeline_design/03_생성_단계_설계.md

"""잡 스트리밍 응답 스키마 모듈."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class JobStreamResponse(BaseModel):
    """잡 스트리밍 응답 스키마."""

    type: str = Field(..., description="이벤트 타입(token/references/error/DONE)")
    status: str | None = Field(default=None, description="이벤트 상태(in_progress/end)")
    content: str | None = Field(default=None, description="토큰/메시지 내용")
    index: int | None = Field(default=None, description="토큰 순서(선택)")
    items: list[dict[str, Any]] | None = Field(default=None, description="근거 문서 목록(선택)")

    def todo_extend_fields(self) -> None:
        """스트리밍 필드 확장을 위한 자리표시자."""
        # TODO: 이벤트 타입별 필드 규칙을 문서에 맞게 확정한다.
        raise NotImplementedError
