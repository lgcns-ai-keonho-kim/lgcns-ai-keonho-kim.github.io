# 목적: 주택 에이전트 응답 모델을 정의한다.
# 설명: API 응답 스키마를 고정해 반환 구조를 일관되게 한다.
# 디자인 패턴: 데이터 전송 객체(DTO)
# 참조: fourthsession/api/housing_agent/service

"""주택 에이전트 응답 모델 모듈."""

from pydantic import BaseModel, Field


class HousingAgentResponse(BaseModel):
    """주택 에이전트 응답 모델."""

    answer: str = Field(description="최종 답변")
    trace_id: str | None = Field(default=None, description="추적 식별자")
    metadata: dict | None = Field(default=None, description="추가 메타데이터")

    @classmethod
    def from_result(cls, result: dict) -> "HousingAgentResponse":
        """실행 결과에서 응답 모델을 생성한다.

        Args:
            result (dict): 에이전트 실행 결과.

        Returns:
            HousingAgentResponse: 응답 모델.
        """
        # TODO: 실행 결과를 응답 스키마로 매핑한다.
        raise NotImplementedError("TODO: 응답 모델 생성 구현")
