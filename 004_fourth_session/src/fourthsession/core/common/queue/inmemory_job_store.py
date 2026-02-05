# 목적: 인메모리 작업 저장소를 정의한다.
# 설명: 작업 상태를 프로세스 메모리에 저장한다.
# 디자인 패턴: 리포지토리 패턴
# 참조: fourthsession/core/common/queue/job_record.py

"""인메모리 작업 저장소 모듈."""

from fourthsession.core.common.queue.job_record import JobRecord


class InMemoryJobStore:
    """인메모리 작업 저장소."""

    def __init__(self) -> None:
        """저장소를 초기화한다."""
        # TODO: 내부 저장 구조(딕셔너리, Lock)를 준비한다.
        raise NotImplementedError("TODO: 저장소 초기화 구현")

    def create(self, job_id: str, payload: dict) -> JobRecord:
        """작업 레코드를 생성한다.

        Args:
            job_id (str): 작업 식별자.
            payload (dict): 작업 페이로드.

        Returns:
            JobRecord: 생성된 레코드.
        """
        # TODO: JobRecord를 생성하고 저장한다.
        raise NotImplementedError("TODO: 작업 생성 구현")

    def update_status(self, job_id: str, status: str) -> JobRecord | None:
        """작업 상태를 갱신한다.

        Args:
            job_id (str): 작업 식별자.
            status (str): 변경 상태.

        Returns:
            JobRecord | None: 갱신된 레코드.
        """
        # TODO: 저장된 레코드의 상태/시간을 갱신한다.
        raise NotImplementedError("TODO: 작업 상태 갱신 구현")

    def get(self, job_id: str) -> JobRecord | None:
        """작업 레코드를 조회한다.

        Args:
            job_id (str): 작업 식별자.

        Returns:
            JobRecord | None: 작업 레코드.
        """
        # TODO: job_id로 레코드를 조회한다.
        raise NotImplementedError("TODO: 작업 조회 구현")
