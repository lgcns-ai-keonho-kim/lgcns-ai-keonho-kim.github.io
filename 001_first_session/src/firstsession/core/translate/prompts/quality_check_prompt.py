# 목적: 번역 품질 검사 프롬프트 템플릿을 제공한다.
# 설명: 원문과 번역문을 비교해 YES/NO로 통과 여부를 판단한다.
# 디자인 패턴: Singleton
# 참조: docs/04_string_tricks/01_yes_no_파서.md

"""번역 품질 검사 프롬프트 템플릿 모듈."""

from textwrap import dedent
from langchain_core.prompts import PromptTemplate

_QUALITY_CHECK_PROMPT = dedent(
    """\
You are a translation quality reviewer.

[Criteria]
- Is the meaning of the source preserved without omissions or distortion?
- Are proper nouns, numbers, and code preserved without unnecessary changes?
- Is the translation natural in the target language?

[Rules]
- Output must be exactly one word: YES or NO.
- No explanation, whitespace, punctuation, or quotes.

[Source]
{source_text}

[Translation]
{translated_text}

[Output]
YES or NO
"""
)

QUALITY_CHECK_PROMPT = PromptTemplate(
    template=_QUALITY_CHECK_PROMPT,
    input_variables=["source_text", "translated_text"],
)
