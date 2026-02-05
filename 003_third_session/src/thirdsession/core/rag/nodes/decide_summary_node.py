# 목적: 요약 실행 여부를 결정한다.
# 설명: turn_count 기준으로 요약 실행 여부를 반환한다.
# 디자인 패턴: Command
# 참조: nextStep.md

"""요약 결정 노드 모듈."""


class DecideSummaryNode:
    """요약 결정 노드."""

    def __init__(self, summary_threshold: int = 5) -> None:
        """결정 기준을 초기화한다.

        Args:
            summary_threshold: 요약 실행 기준 턴 수.
        """
        self._summary_threshold = summary_threshold

    def run(self, turn_count: int) -> bool:
        """요약 실행 여부를 판단한다."""
        return turn_count >= self._summary_threshold
