# 목적: 재번역 프롬프트 템플릿을 제공한다.
# 설명: QC 실패 시 기존 번역을 참고해 다시 번역하도록 지시한다.
# 디자인 패턴: Singleton
# 참조: docs/04_string_tricks/05_retry_logic.md

"""재번역 프롬프트 템플릿 모듈."""

from textwrap import dedent
from langchain_core.prompts import PromptTemplate

_RETRY_TRANSLATE_PROMPT = dedent(
    """\
You are a translation rewriter.

[Rules]
- Refer to the existing translation but do not add new content.
- Preserve the original meaning while improving translation quality.
- Output only the translation (no explanation).

[Source]
{source_text}

[Previous Translation]
{failed_translation}

[Output]
Provide only the improved translation.
"""
)

RETRY_TRANSLATE_PROMPT = PromptTemplate(
    template=_RETRY_TRANSLATE_PROMPT,
    input_variables=["source_text", "failed_translation"],
)
