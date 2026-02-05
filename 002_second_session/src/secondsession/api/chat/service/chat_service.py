# 목적: 대화 서비스 인터페이스를 정의한다.
# 설명: 라우터가 호출할 서비스 메서드 시그니처를 제공한다.
# 디자인 패턴: 서비스 레이어 패턴
# 참조: secondsession/api/chat/router/chat_router.py

"""대화 서비스 인터페이스 모듈."""

from collections.abc import Iterable

from secondsession.api.chat.model import (
    ChatJobRequest,
    ChatJobResponse,
    ChatJobStatusResponse,
    ChatJobCancelResponse,
)
from secondsession.core.chat.graphs.chat_graph import ChatGraph


class ChatService:
    """대화 서비스 인터페이스."""

    def __init__(self, graph: ChatGraph) -> None:
        """서비스 의존성을 초기화한다.

        Args:
            graph: 대화 그래프 실행기.
        """
        self._graph = graph

    def create_job(self, request: ChatJobRequest) -> ChatJobResponse:
        """대화 작업을 생성한다.

        TODO:
            - job_id/trace_id 생성
            - 워커 큐에 작업 적재
            - 대화 요청 → 스트리밍 응답 → 5턴 초과 시 요약 플로우를 설계
            - thread_id 기반 복구 로직을 연결
            - 체크포인터에 thread_id를 전달해 대화 내역을 복구
            - safeguard 분기 결과를 error_code/metadata에 기록
            - 폴백 케이스에서도 스트리밍 이벤트를 정상 종료
        """
        raise NotImplementedError("대화 작업 생성 로직을 구현해야 합니다.")

    def stream_events(self, job_id: str) -> Iterable[str]:
        """스트리밍 이벤트를 SSE 라인으로 반환한다.

        TODO:
            - Redis에서 이벤트를 소비
            - done 이벤트까지 전송
            - 대화 응답 토큰과 메타데이터를 순서대로 전달
            - seq는 job_id 기준으로 단조 증가하도록 구성
            - type/token/metadata/error/done 포맷을 유지
            - 종료 시 done 이벤트를 반드시 적재
            - 폴백 에러 코드가 있는 경우 error 이벤트를 먼저 전송
        """
        raise NotImplementedError("스트리밍 이벤트 소비 로직을 구현해야 합니다.")

    def get_status(self, job_id: str) -> ChatJobStatusResponse:
        """작업 상태를 조회한다.

        TODO:
            - 상태 저장소 조회
            - 진행률/상태 반환
        """
        raise NotImplementedError("작업 상태 조회 로직을 구현해야 합니다.")

    def cancel(self, job_id: str) -> ChatJobCancelResponse:
        """작업을 취소한다.

        TODO:
            - 취소 플래그 기록
            - 워커가 취소를 확인하도록 구성
        """
        raise NotImplementedError("작업 취소 로직을 구현해야 합니다.")
