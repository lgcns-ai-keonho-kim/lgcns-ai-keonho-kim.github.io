# 목적: 잡 서비스 인터페이스를 정의한다.
# 설명: 라우터가 호출할 서비스 메서드 시그니처를 제공한다.
# 디자인 패턴: 서비스 레이어 패턴
# 참조: nextStep.md

"""잡 서비스 모듈."""

from __future__ import annotations

from collections.abc import Iterable

from thirdsession.api.rag.model import (
    JobCancelResponse,
    JobRequest,
    JobResponse,
    JobStatusResponse,
)
from thirdsession.core.common.queue import ChatJobQueue, ChatStreamEventQueue


class RagJobService:
    """잡 서비스."""

    def __init__(
        self,
        job_queue: ChatJobQueue | None = None,
        event_queue: ChatStreamEventQueue | None = None,
    ) -> None:
        """서비스 의존성을 초기화한다.

        Args:
            job_queue: 작업 큐(선택).
            event_queue: 스트리밍 이벤트 큐(선택).
        """
        self._job_queue = job_queue
        self._event_queue = event_queue

    def create_job(self, request: JobRequest) -> JobResponse:
        """잡 작업을 생성한다.

        TODO:
            - job_id/trace_id 생성
            - 워커 큐에 작업 적재
            - thread_id 기반 복구 로직 연결
            - 체크포인터에 thread_id 전달
            - safeguard 분기 결과를 error_code/metadata에 기록
            - 폴백 케이스에서도 스트리밍 이벤트 정상 종료
        """
        _ = request
        raise NotImplementedError("잡 작업 생성 로직을 구현해야 합니다.")

    def stream_events(self, job_id: str) -> Iterable[str]:
        """스트리밍 이벤트를 SSE 라인으로 반환한다.

        TODO:
            - 이벤트 큐에서 이벤트 소비
            - done 이벤트까지 전송
            - seq는 job_id 기준으로 단조 증가
            - type/token/metadata/error/done 포맷 유지
        """
        _ = job_id
        raise NotImplementedError("스트리밍 이벤트 소비 로직을 구현해야 합니다.")

    def get_status(self, job_id: str) -> JobStatusResponse:
        """작업 상태를 조회한다.

        TODO:
            - 상태 저장소 조회
            - 진행률/상태 반환
        """
        _ = job_id
        raise NotImplementedError("작업 상태 조회 로직을 구현해야 합니다.")

    def cancel(self, job_id: str) -> JobCancelResponse:
        """작업을 취소한다.

        TODO:
            - 취소 플래그 기록
            - 워커가 취소를 확인하도록 구성
        """
        _ = job_id
        raise NotImplementedError("작업 취소 로직을 구현해야 합니다.")
