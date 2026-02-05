# 목적: RAG 상수 패키지를 초기화한다.
# 설명: 에러 코드/안전 라벨 상수를 노출한다.
# 디자인 패턴: 없음
# 참조: thirdsession/core/rag/const/error_code.py, safeguard_label.py

"""RAG 상수 패키지."""

from thirdsession.core.rag.const.error_code import ErrorCode
from thirdsession.core.rag.const.safeguard_label import SafeguardLabel

__all__ = ["ErrorCode", "SafeguardLabel"]
