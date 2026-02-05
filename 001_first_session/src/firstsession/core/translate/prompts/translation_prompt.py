# 목적: 번역 프롬프트 템플릿을 제공한다.
# 설명: 일관된 번역 규칙을 유지하기 위해 싱글턴으로 관리한다.
# 디자인 패턴: Singleton
# 참조: firstsession/core/translate/nodes/translate_node.py

"""번역 프롬프트 템플릿 모듈."""

from textwrap import dedent
from langchain_core.prompts import PromptTemplate

_TRANSLATION_PROMPT = dedent(
    """\
You are a professional translator.

[Source Language]
{source_language}

[Target Language]
{target_language}

[Rules]
- Translate naturally without distorting the meaning.
- Preserve proper nouns, code, and numbers when possible.
- Output only the translation (no explanation, no preface or closing).

[Text to Translate]
{text}

[Output]
Provide only the translated text.
"""
)

TRANSLATION_PROMPT = PromptTemplate(
    template=_TRANSLATION_PROMPT,
    input_variables=["source_language", "target_language", "text"],
)
