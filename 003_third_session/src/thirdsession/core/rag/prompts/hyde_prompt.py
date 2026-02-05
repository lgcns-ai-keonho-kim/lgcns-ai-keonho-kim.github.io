# 목적: HyDE 생성 프롬프트를 제공한다.
# 설명: 가상 문서 생성 규칙을 포함하며 싱글턴으로 관리한다.
# 디자인 패턴: Singleton
# 참조: thirdsession/core/rag/nodes/hyde_node.py

"""HyDE 프롬프트 모듈."""

from textwrap import dedent

from langchain_core.prompts import PromptTemplate

_HYDE_PROMPT = dedent(
    """\
You are creating a hypothetical document that answers the user's question.

[Question]
{question}

[Rules]
- Write a concise, factual paragraph.
- Do not mention that this is hypothetical.
- Avoid speculation beyond the question.

[Output]
Provide only the generated document text.
"""
)

HYDE_PROMPT = PromptTemplate(
    template=_HYDE_PROMPT,
    input_variables=["question"],
)
