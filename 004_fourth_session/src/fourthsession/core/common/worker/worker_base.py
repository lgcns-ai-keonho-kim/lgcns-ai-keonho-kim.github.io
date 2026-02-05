# 목적: 워커 베이스 클래스를 정의한다.
# 설명: 큐 기반 작업 처리 흐름을 표준화한다.
# 디자인 패턴: 템플릿 메서드 패턴
# 참조: fourthsession/core/common/queue/job_queue.py

"""워커 베이스 모듈."""

from abc import ABC, abstractmethod


class WorkerBase(ABC):
    """워커 실행 베이스 클래스."""

    def __init__(self, poll_interval: float = 1.0) -> None:
        """워커 설정을 초기화한다.

        Args:
            poll_interval (float): 폴링 간격(초).
        """
        self._poll_interval = poll_interval

    def run(self) -> None:
        """워커 루프를 실행한다.

        TODO:
        - run_once()를 반복 호출하는 루프를 구현한다.
        - 처리할 작업이 없으면 poll_interval만큼 대기한다.
        """
        raise NotImplementedError("TODO: 워커 실행 루프 구현")

    def stop(self) -> None:
        """워커를 중지한다."""
        # TODO: 워커 중지 플래그를 구현한다.
        raise NotImplementedError("TODO: 워커 중지 구현")

    @abstractmethod
    def run_once(self) -> bool:
        """작업을 한 번 처리한다.

        Returns:
            bool: 작업 처리 여부.
            - True: 작업을 실제로 처리함(큐에서 1건 이상 소비).
            - False: 처리할 작업이 없음(큐 비어 있음).
        """
        raise NotImplementedError("TODO: run_once 구현")
