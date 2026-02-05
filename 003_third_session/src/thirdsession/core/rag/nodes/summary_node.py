# 목적: 대화 요약을 생성한다.
# 설명: 누적된 history를 요약해 summary를 갱신한다.
# 디자인 패턴: Command
# 참조: nextStep.md

"""대화 요약 노드 모듈."""

from __future__ import annotations

from typing import Any


class SummaryNode:
    """대화 요약 노드."""

    def run(self, history: list[dict[str, Any]], previous_summary: str | None) -> str:
        """대화 요약을 생성한다."""
        _ = history
        _ = previous_summary
        raise NotImplementedError("요약 생성 로직을 구현해야 합니다.")
