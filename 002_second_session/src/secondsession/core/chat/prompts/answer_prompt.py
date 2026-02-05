# 목적: 대화 응답 프롬프트 템플릿을 제공한다.
# 설명: 사용자 질문에 대한 응답 품질을 높이기 위한 기본 프롬프트를 정의한다.
# 디자인 패턴: Singleton
# 참조: secondsession/core/chat/nodes/answer_node.py

"""대화 응답 프롬프트 모듈."""

from textwrap import dedent

from langchain_core.prompts import PromptTemplate

_ANSWER_PROMPT = dedent(
    """\
당신은 친절한 서비스 어시스턴트입니다.

[규칙]
- 사용자의 질문에 명확하고 간결하게 답변하세요.
- 불필요한 추측은 피하고, 필요한 경우 간단히 확인 질문을 하세요.

[사용자 입력]
{user_message}

[출력]
답변만 출력하세요.
"""
)

ANSWER_PROMPT = PromptTemplate(
    template=_ANSWER_PROMPT,
    input_variables=["user_message"],
)

# TODO:
# - 서비스 톤 앤 매너에 맞게 규칙을 구체화하세요.
# - 시스템 메시지/도메인 정책을 추가하세요.
