# 목적: 검색 결과를 병합한다.
# 설명: 정규화/중복 제거 규칙을 노드 내부에서 처리한다.
# 디자인 패턴: Command
# 참조: 없음

"""결과 병합 노드 모듈."""

from __future__ import annotations

from typing import Any


class MergeNode:
    """결과 병합 노드."""

    def run(self, groups: list[list[Any]]) -> list[Any]:
        """검색 결과를 병합한다."""
        # TODO: 병합/정규화/중복 제거 규칙을 노드 내부에서 구현한다.
        raise NotImplementedError
