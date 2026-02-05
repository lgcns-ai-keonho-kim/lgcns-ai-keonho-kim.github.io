# 목적: 동기 워커의 실행 뼈대를 정의한다.
# 설명: 작업 루프의 공통 흐름을 고정하고 하위 클래스가 세부 구현을 제공한다.
# 디자인 패턴: 템플릿 메서드 패턴
# 참조: nextStep.md

"""동기 워커 베이스 모듈."""

from __future__ import annotations

from typing import Any


class WorkerBase:
    """동기 워커 베이스 클래스."""

    def run_forever(self) -> None:
        """작업 루프를 실행한다."""
        # TODO: 루프 생명주기, 예외 처리, 종료 조건을 정의한다.
        raise NotImplementedError("워커 실행 루프를 구현해야 합니다.")

    def fetch_job(self) -> dict[str, Any] | None:
        """작업을 가져온다."""
        # TODO: 큐/스토리지에서 작업을 가져오는 로직을 정의한다.
        raise NotImplementedError("작업 조회 로직을 구현해야 합니다.")

    def handle_job(self, payload: dict[str, Any]) -> None:
        """작업을 처리한다.

        Args:
            payload: 작업 페이로드.
        """
        # TODO: 작업 처리 로직과 체크포인트 연계를 정의한다.
        raise NotImplementedError("작업 처리 로직을 구현해야 합니다.")
