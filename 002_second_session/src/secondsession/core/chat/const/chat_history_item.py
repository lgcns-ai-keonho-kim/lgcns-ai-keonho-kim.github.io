# 목적: 대화 내역 항목 스키마를 정의한다.
# 설명: history에 저장되는 항목을 검증하기 위한 모델이다.
# 디자인 패턴: DTO
# 참조: secondsession/core/chat/state/chat_state.py

"""대화 내역 항목 스키마 모듈."""

from pydantic import BaseModel, Field


class ChatHistoryItem(BaseModel):
    """대화 내역 항목."""

    role: str = Field(..., description="역할(user/assistant/system)")
    content: str = Field(..., description="메시지 내용")
    created_at: str | None = Field(default=None, description="생성 시각(ISO8601)")


# TODO:
# - role을 Literal로 제한한다.
# - content 길이 제한 정책을 추가한다.
