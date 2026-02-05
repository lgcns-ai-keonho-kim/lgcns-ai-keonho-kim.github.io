# 목적: 리포트 작업 레포지토리를 정의한다.
# 설명: 비동기 리포트 작업 생성/조회/갱신을 담당한다.
# 디자인 패턴: 리포지토리 패턴
# 참조: fourthsession/core/repository/sqlite/connection_provider.py

"""리포트 작업 레포지토리 모듈."""


class ReportJobRepository:
    """리포트 작업 레포지토리."""

    def create_job(self, payload: dict) -> dict:
        """리포트 작업을 생성한다.

        Args:
            payload (dict): 작업 생성 입력.

        Returns:
            dict: 생성된 작업 정보.
        """
        # TODO: 작업 레코드를 저장하고 job_id를 반환한다.
        raise NotImplementedError("TODO: 작업 생성 구현")

    def get_job_status(self, job_id: str) -> dict:
        """작업 상태를 조회한다.

        Args:
            job_id (str): 작업 식별자.

        Returns:
            dict: 작업 상태 정보.
        """
        # TODO: job_id로 상태를 조회한다.
        raise NotImplementedError("TODO: 작업 상태 조회 구현")

    def update_job_status(self, job_id: str, status: str) -> None:
        """작업 상태를 갱신한다.

        Args:
            job_id (str): 작업 식별자.
            status (str): 변경할 상태.
        """
        # TODO: 상태를 업데이트하고 변경 이력을 기록한다.
        raise NotImplementedError("TODO: 작업 상태 갱신 구현")
