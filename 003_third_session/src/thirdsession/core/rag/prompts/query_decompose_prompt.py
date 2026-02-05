# 목적: 쿼리 분해 프롬프트를 제공한다.
# 설명: 하위 질문 생성 규칙을 포함하며 싱글턴으로 관리한다.
# 디자인 패턴: Singleton
# 참조: thirdsession/core/rag/nodes/query_decompose_node.py

"""쿼리 분해 프롬프트 모듈."""

from textwrap import dedent

from langchain_core.prompts import PromptTemplate

_QUERY_DECOMPOSE_PROMPT = dedent(
    """\
You are decomposing a complex user question into smaller, focused sub-questions.

[Question]
{question}

[Rules]
- Produce 3 to 5 sub-questions.
- Each sub-question should be answerable on its own.
- Do not include numbering or extra commentary.

[Output]
Return each sub-question on a new line.
"""
)

QUERY_DECOMPOSE_PROMPT = PromptTemplate(
    template=_QUERY_DECOMPOSE_PROMPT,
    input_variables=["question"],
)
