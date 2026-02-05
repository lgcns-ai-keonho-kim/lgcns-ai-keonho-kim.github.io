# 목적: 입력 안전 검사를 수행한다.
# 설명: 질문을 안전 라벨로 분류한다.
# 디자인 패턴: Command
# 참조: thirdsession/core/rag/const/safeguard_label.py

"""입력 안전 검사 노드 모듈."""

from thirdsession.core.rag.const import SafeguardLabel


class SafeguardNode:
    """입력 안전 검사 노드."""

    def run(self, question: str) -> SafeguardLabel:
        """질문을 안전 라벨로 분류한다."""
        _ = question
        raise NotImplementedError("안전 분류 로직을 구현해야 합니다.")
