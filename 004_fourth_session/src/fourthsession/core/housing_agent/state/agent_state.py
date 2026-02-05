# 목적: 주택 에이전트 상태 스키마를 정의한다.
# 설명: LangGraph 상태에 저장될 필드를 단일 모델로 관리한다.
# 디자인 패턴: 데이터 전송 객체(DTO)
# 참조: fourthsession/core/housing_agent/graph

"""주택 에이전트 상태 모델 모듈."""

from pydantic import BaseModel, Field


class HousingAgentState(BaseModel):
    """주택 에이전트 상태 모델."""

    question: str | None = Field(default=None, description="사용자 질문")
    plan: dict | None = Field(default=None, description="계획 JSON")
    tool_results: list[dict] = Field(default_factory=list, description="도구 실행 결과")
    answer: str | None = Field(default=None, description="최종 답변")
    errors: list[str] = Field(default_factory=list, description="오류 메시지 목록")
    trace_id: str | None = Field(default=None, description="추적 식별자")
    plan_valid: bool = Field(default=False, description="계획 유효성 여부")
    retry_count: int = Field(default=0, description="재시도 횟수")
    max_retries: int = Field(default=2, description="최대 재시도 횟수")
    tool_cards: list[dict] = Field(default_factory=list, description="MCP 도구 카드 목록")
    finalized: bool = Field(default=False, description="종료 여부")

    @classmethod
    def empty(cls) -> "HousingAgentState":
        """빈 상태를 생성한다.

        Returns:
            HousingAgentState: 기본값으로 초기화된 상태.
        """
        # TODO: 최소 필수 필드를 설정한 초기 상태를 만든다.
        raise NotImplementedError("TODO: 상태 초기화 구현")
