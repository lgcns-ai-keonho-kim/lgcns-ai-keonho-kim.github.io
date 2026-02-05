# 목적: 번역 응답 DTO를 정의한다.
# 설명: 번역 결과와 언어 정보를 반환한다.
# 디자인 패턴: DTO
# 참조: firstsession/api/translate/router/translate_router.py

"""번역 응답 모델 모듈."""

from pydantic import BaseModel, Field


class TranslationResponse(BaseModel):
    """번역 응답 데이터 모델."""

    source_language: str = Field(..., description="원문 언어 코드")
    target_language: str = Field(..., description="목표 언어 코드")
    translated_text: str = Field(..., description="번역된 텍스트")
