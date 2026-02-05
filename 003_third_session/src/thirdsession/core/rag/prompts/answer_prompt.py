# 목적: 답변 생성 프롬프트를 제공한다.
# 설명: 근거 기반 답변 규칙을 포함하며 싱글턴으로 관리한다.
# 디자인 패턴: Singleton
# 참조: thirdsession/core/rag/nodes/stream_answer_node.py

"""답변 생성 프롬프트 모듈."""

from textwrap import dedent

from langchain_core.prompts import PromptTemplate

_ANSWER_PROMPT = dedent(
    """\
You are a helpful assistant. Answer strictly based on the provided contexts.

[Question]
{question}

[Contexts]
{contexts}

[Rules]
- Use only the contexts for factual claims.
- If the answer is not in the contexts, say you don't know.
- Keep the answer concise and well-structured.

[Output]
Provide the final answer text only.
"""
)

ANSWER_PROMPT = PromptTemplate(
    template=_ANSWER_PROMPT,
    input_variables=["question", "contexts"],
)
