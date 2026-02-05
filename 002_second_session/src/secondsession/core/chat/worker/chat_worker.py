# 목적: 대화 워커 실행 흐름을 정의한다.
# 설명: 큐 소비 → 그래프 실행 → 스트리밍 이벤트 적재를 담당한다.
# 디자인 패턴: Worker, Producer-Consumer, Template Method(상속)
# 참조: docs/02_backend_service_layer/05_비동기_엔드포인트_분리_전략.md

"""대화 워커 모듈."""

from __future__ import annotations

from typing import Any

from secondsession.core.chat.graphs import ChatGraph
from secondsession.core.common.queue import ChatJobQueue, ChatStreamEventQueue
from secondsession.core.common.worker import WorkerBase


class ChatWorker(WorkerBase):
    """대화 워커."""

    def __init__(
        self,
        job_queue: ChatJobQueue,
        event_queue: ChatStreamEventQueue,
        checkpointer: Any,
        poll_interval: float = 0.1,
    ) -> None:
        """워커를 초기화한다.

        Args:
            job_queue: 대화 작업 큐.
            event_queue: 스트리밍 이벤트 큐.
            checkpointer: LangGraph 체크포인터.
            poll_interval: 큐 폴링 간격(초).
        """
        super().__init__(poll_interval=poll_interval)
        self._job_queue = job_queue
        self._event_queue = event_queue
        self._checkpointer = checkpointer

    def _dequeue_job(self) -> dict | None:
        """큐에서 작업을 꺼낸다."""
        return self._job_queue.dequeue()

    def _process_job(self, job: dict) -> None:
        """단일 작업을 처리한다.

        TODO:
            - 그래프를 빌드하고 invoke/stream을 실행한다.
            - config에 thread_id를 넣어 체크포인터 복구를 활성화한다.
            - 실행 중 token/metadata/error 이벤트를 event_queue에 적재한다.
            - 메타데이터 content는 JSON 문자열(예: event, message, route, timestamp)을 사용한다.
            - error 발생 시 error → done 순서로 적재한다.
            - done 이벤트를 반드시 적재하고 종료한다.
        """
        _ = ChatGraph(self._checkpointer)
        _ = job
        raise NotImplementedError("워커 실행 로직을 구현해야 합니다.")
