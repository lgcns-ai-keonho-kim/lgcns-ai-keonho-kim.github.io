# 목적: 잡 생성 요청 스키마를 정의한다.
# 설명: 요청 본문에서 필요한 최소 필드를 제공한다.
# 디자인 패턴: DTO
# 참조: nextStep.md

"""잡 생성 요청 스키마 모듈."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class JobRequest(BaseModel):
    """잡 생성 요청 스키마."""

    query: str = Field(..., description="사용자 입력 내용")
    history: list[dict[str, Any]] | None = Field(default=None, description="이전 대화 내역")
    turn_count: int | None = Field(default=None, description="누적 대화 턴 수")
    thread_id: str | None = Field(default=None, description="대화 복구용 thread_id")
    session_id: str | None = Field(default=None, description="대화 세션 식별자")
    user_id: str | None = Field(default=None, description="요청 사용자 ID")
    metadata: dict[str, Any] | None = Field(default=None, description="추가 메타데이터")
    collection: str | None = Field(default=None, description="검색 컬렉션(선택)")
