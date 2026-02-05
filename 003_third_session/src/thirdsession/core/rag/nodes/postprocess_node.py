# 목적: 후처리 단계를 실행한다.
# 설명: 중복 제거/다양성/재정렬/압축을 노드 내부에서 수행한다.
# 디자인 패턴: Command
# 참조: 없음

"""후처리 노드 모듈."""

from __future__ import annotations

from typing import Any


class PostprocessNode:
    """후처리 노드."""

    def run(self, docs: list[Any]) -> list[Any]:
        """후처리를 수행한다."""
        # TODO: 중복 제거/다양성/재정렬/압축을 노드 내부에서 구현한다.
        raise NotImplementedError
