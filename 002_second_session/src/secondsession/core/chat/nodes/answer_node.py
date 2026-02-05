# 목적: 사용자 입력에 대한 답변을 생성한다.
# 설명: LLM 호출을 통해 응답을 만든다.
# 디자인 패턴: 전략 패턴 + 파이프라인 노드
# 참조: secondsession/core/chat/graphs/chat_graph.py

"""대화 응답 생성 노드 모듈."""

from secondsession.core.chat.prompts.answer_prompt import ANSWER_PROMPT
from secondsession.core.chat.state.chat_state import ChatState
from secondsession.core.common.llm_client import LlmClient


class AnswerNode:
    """사용자 입력에 대한 답변을 생성하는 노드."""

    def __init__(self, llm_client: LlmClient | None = None) -> None:
        """노드 의존성을 초기화한다.

        Args:
            llm_client: LLM 클라이언트(선택).
        """
        self._llm_client = llm_client

    def run(self, state: ChatState) -> ChatState:
        """사용자 입력에 대한 답변을 생성한다.

        Args:
            state: 현재 대화 상태.

        Returns:
            ChatState: 답변 결과가 반영된 상태.
        """
        # TODO: LLM 클라이언트를 연결한다.
        # TODO: ANSWER_PROMPT.format으로 사용자 입력을 결합한다.
        # TODO: state["last_user_message"]를 기반으로 답변을 생성한다.
        # TODO: 결과를 last_assistant_message로 반환한다.
        # TODO: 응답 스키마(Pydantic) 검증 실패 시 error_code를 설정한다.
        # TODO: 도구 호출 실패/타임아웃 시 error_code를 설정한다.
        # TODO: error_code가 설정된 경우 폴백 라우팅 흐름을 고려한다.
        # TODO: ErrorCode(Enum)로 에러 유형을 고정한다.
        _ = state["last_user_message"]
        _ = ANSWER_PROMPT
        _ = self._llm_client
        raise NotImplementedError("답변 생성 로직을 구현해야 합니다.")
