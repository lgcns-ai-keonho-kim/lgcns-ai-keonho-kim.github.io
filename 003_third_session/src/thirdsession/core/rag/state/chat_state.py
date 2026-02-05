# 목적: RAG 파이프라인에서 사용하는 상태 구조를 정의한다.
# 설명: 노드 간 전달할 필드를 명확히 관리하고 reducer 규칙을 제공한다.
# 디자인 패턴: 상태 패턴(State) 데이터 구조
# 참조: thirdsession/core/rag/graphs/rag_pipeline_graph.py

"""RAG 파이프라인 상태 모듈."""

from __future__ import annotations

from typing import Annotated, Any, TypedDict


def add_history(existing: list[dict[str, Any]], incoming: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    """대화 내역을 누적한다."""
    if incoming is None:
        return existing
    return existing + incoming


def set_summary(existing: str | None, incoming: str | None) -> str | None:
    """요약 값을 갱신한다."""
    if incoming is None:
        return existing
    return incoming


def add_turn(existing: int, incoming: int | None) -> int:
    """턴 수를 누적한다."""
    if incoming is None:
        return existing
    return existing + incoming


def add_contexts(existing: list[Any], incoming: list[Any] | None) -> list[Any]:
    """문서 컨텍스트를 누적한다."""
    if incoming is None:
        return existing
    return existing + incoming


def add_sources(existing: list[dict[str, Any]], incoming: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    """근거 소스 목록을 누적한다."""
    if incoming is None:
        return existing
    return existing + incoming


class ChatState(TypedDict):
    """RAG 파이프라인 상태 스키마."""

    question: str
    history: Annotated[list[dict[str, Any]], add_history]
    summary: Annotated[str | None, set_summary]
    turn_count: Annotated[int, add_turn]
    contexts: Annotated[list[Any], add_contexts]
    answer: str | None
    last_user_message: str | None
    last_assistant_message: str | None
    route: str | None
    error_code: str | None
    safeguard_label: str | None
    trace_id: str | None
    thread_id: str | None
    session_id: str | None
    user_id: str | None
    metadata: dict[str, Any] | None
    sources: Annotated[list[dict[str, Any]], add_sources]
    retrieval_stats: dict[str, Any] | None
