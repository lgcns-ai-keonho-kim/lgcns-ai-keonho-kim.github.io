# 목적: 안전 분류 노드를 정의한다.
# 설명: 사용자 입력을 안전 라벨로 분류한다.
# 디자인 패턴: 전략 패턴 + 파이프라인 노드
# 참조: secondsession/core/chat/graphs/chat_graph.py

"""안전 분류 노드 모듈."""

from secondsession.core.chat.prompts.safeguard_prompt import SAFEGUARD_PROMPT
from secondsession.core.chat.state.chat_state import ChatState
from secondsession.core.common.llm_client import LlmClient


class SafeguardNode:
    """사용자 입력을 안전 라벨로 분류하는 노드."""

    def __init__(self, llm_client: LlmClient | None = None) -> None:
        """노드 의존성을 초기화한다.

        Args:
            llm_client: LLM 클라이언트(선택).
        """
        self._llm_client = llm_client

    def run(self, state: ChatState) -> ChatState:
        """사용자 입력을 안전 라벨로 분류한다.

        Args:
            state: 현재 대화 상태.

        Returns:
            ChatState: 안전 라벨이 반영된 상태.
        """
        # TODO: LLM 클라이언트를 연결한다.
        # TODO: SAFEGUARD_PROMPT.format으로 사용자 입력을 결합한다.
        # TODO: 결과 라벨을 safeguard_label로 반환한다.
        # TODO: PASS가 아닌 경우 error_code를 설정하는 정책을 정의한다.
        # TODO: 라벨별 사용자 메시지/차단 정책을 문서화한다.
        # TODO: SafeguardLabel/ErrorCode(Enum)을 사용해 값을 고정한다.
        _ = SAFEGUARD_PROMPT
        _ = state.get("last_user_message", "")
        _ = self._llm_client
        raise NotImplementedError("안전 분류 로직을 구현해야 합니다.")
