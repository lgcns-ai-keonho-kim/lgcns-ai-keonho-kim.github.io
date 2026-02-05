# 목적: 대화 그래프의 상태 스키마를 정의한다.
# 설명: 대화 내역과 요약 정보를 포함한 상태를 관리한다.
# 디자인 패턴: 상태 객체
# 참조: secondsession/core/chat/graphs/chat_graph.py

"""대화 그래프 상태 스키마 모듈."""

from typing import Annotated, TypedDict

from secondsession.core.chat.const import ErrorCode, SafeguardLabel

def add_history(existing: list[dict], incoming: list[dict] | None) -> list[dict]:
    """대화 내역을 누적한다.

    TODO:
        - history 항목의 스키마를 정의한다.
        - 필요한 경우 최근 N턴만 유지하는 정책을 추가한다.
    """
    if incoming is None:
        return existing
    return existing + incoming


def add_turn(existing: int, incoming: int | None) -> int:
    """턴 수를 누적한다."""
    if incoming is None:
        return existing
    return existing + incoming


def add_candidates(existing: list[str], incoming: list[str] | None) -> list[str]:
    """병렬 후보 응답을 누적한다."""
    if incoming is None:
        return existing
    return existing + incoming


class ChatState(TypedDict):
    """대화 그래프 상태 스키마."""

    history: Annotated[list[dict], add_history]
    summary: str | None
    turn_count: Annotated[int, add_turn]
    last_user_message: str
    last_assistant_message: str | None
    candidates: Annotated[list[str], add_candidates]
    # TODO:
    # - error_code와 safeguard_label을 기준으로 폴백 메시지를 연결한다.
    safeguard_label: SafeguardLabel | None
    route: str | None
    error_code: ErrorCode | None
    trace_id: str | None
    thread_id: str | None
    session_id: str | None
    history_persisted: bool | None
