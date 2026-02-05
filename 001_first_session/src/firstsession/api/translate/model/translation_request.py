# 목적: 번역 요청 DTO를 정의한다.
# 설명: 입력 텍스트와 언어 코드를 명시적으로 관리한다.
# 디자인 패턴: DTO
# 참조: firstsession/api/translate/router/translate_router.py

"""번역 요청 모델 모듈."""

from pydantic import BaseModel, Field


class TranslationRequest(BaseModel):
    """번역 요청 데이터 모델."""

    source_language: str = Field(..., description="원문 언어 코드")
    target_language: str = Field(..., description="목표 언어 코드")
    text: str = Field(..., description="번역할 텍스트")
