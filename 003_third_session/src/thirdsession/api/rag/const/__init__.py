# 목적: rag 상수 패키지를 초기화한다.
# 설명: API 경로/태그 상수를 공개한다.
# 디자인 패턴: 없음
# 참조: thirdsession/api/rag/const/api_constants.py

"""rag 상수 패키지."""

from thirdsession.api.rag.const.api_constants import (
    API_V1_PREFIX,
    JOB_PREFIX,
    JOB_TAG,
    RAG_PREFIX,
    RAG_TAG,
)

__all__ = ["API_V1_PREFIX", "JOB_PREFIX", "JOB_TAG", "RAG_PREFIX", "RAG_TAG"]
