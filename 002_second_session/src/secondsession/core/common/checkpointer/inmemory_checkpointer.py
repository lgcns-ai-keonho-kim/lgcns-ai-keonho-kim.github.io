# 목적: 인메모리 체크포인터를 제공한다.
# 설명: thread_id 기준으로 상태 스냅샷을 저장/복구한다.
# 디자인 패턴: Repository, Memento
# 참조: docs/03_langgraph_checkpoint/03_인메모리_체크포인터.md

"""인메모리 체크포인터 모듈."""

from __future__ import annotations

from typing import Any


class InMemoryCheckpointer:
    """인메모리 체크포인터."""

    def __init__(self, keep_last: int | None = None) -> None:
        """체크포인터를 초기화한다.

        Args:
            keep_last: thread_id별로 유지할 최신 체크포인트 개수. None이면 제한 없음.
        """
        self._store: dict[str, dict[str, dict[str, Any]]] = {}
        self._version: dict[str, int] = {}
        self._keep_last = keep_last

    def save(self, thread_id: str, state: dict[str, Any], metadata: dict[str, Any]) -> str:
        """상태 스냅샷을 저장한다.

        TODO:
            - thread_id별 버전을 증가시키고 checkpoint_id를 생성한다.
            - state/metadata를 저장하고 checkpoint_id를 반환한다.
            - keep_last 정책으로 오래된 스냅샷을 정리한다.
        """
        _ = thread_id
        _ = state
        _ = metadata
        raise NotImplementedError("인메모리 체크포인터 저장 로직을 구현해야 합니다.")

    def load(self, thread_id: str, checkpoint_id: str) -> dict[str, Any] | None:
        """특정 checkpoint_id의 스냅샷을 복구한다.

        TODO:
            - thread_id와 checkpoint_id로 저장된 스냅샷을 조회한다.
            - 없으면 None을 반환한다.
        """
        _ = thread_id
        _ = checkpoint_id
        raise NotImplementedError("인메모리 체크포인터 복구 로직을 구현해야 합니다.")

    def load_latest(self, thread_id: str) -> dict[str, Any] | None:
        """가장 최신 스냅샷을 복구한다.

        TODO:
            - thread_id의 최신 checkpoint_id를 찾는다.
            - 최신 스냅샷이 없으면 None을 반환한다.
        """
        _ = thread_id
        raise NotImplementedError("인메모리 최신 스냅샷 복구 로직을 구현해야 합니다.")
