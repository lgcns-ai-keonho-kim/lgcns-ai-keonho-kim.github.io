# 목적: 주택 에이전트 요청 모델을 정의한다.
# 설명: API 입력 스키마를 고정해 일관된 요청을 보장한다.
# 디자인 패턴: 데이터 전송 객체(DTO)
# 참조: fourthsession/api/housing_agent/service

"""주택 에이전트 요청 모델 모듈."""

from pydantic import BaseModel, Field


class HousingAgentRequest(BaseModel):
    """주택 에이전트 요청 모델."""

    question: str = Field(description="사용자 질문")
    trace_id: str | None = Field(default=None, description="추적 식별자")
    user_id: str | None = Field(default=None, description="사용자 식별자")
    preferred_tools: list[str] | None = Field(default=None, description="우선 사용 도구 목록")
    max_steps: int | None = Field(default=None, description="최대 실행 단계 수")

    @classmethod
    def from_payload(cls, payload: dict) -> "HousingAgentRequest":
        """딕셔너리 입력으로부터 요청 모델을 생성한다.

        Args:
            payload (dict): 원본 입력.

        Returns:
            HousingAgentRequest: 요청 모델.
        """
        # TODO: 입력 검증과 변환 규칙을 정의한다.
        raise NotImplementedError("TODO: 요청 모델 생성 구현")
