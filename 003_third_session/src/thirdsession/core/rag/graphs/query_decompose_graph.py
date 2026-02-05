# 목적: 쿼리 분해 기반 그래프를 정의한다.
# 설명: 질문 분해 → 병렬 검색 → 병합 흐름을 캡슐화한다.
# 디자인 패턴: State Machine
# 참조: thirdsession/core/rag/nodes/query_decompose_node.py

"""쿼리 분해 그래프 모듈."""

from __future__ import annotations


class QueryDecomposeGraph:
    """쿼리 분해 그래프."""

    def build(self) -> None:
        """그래프를 구성한다."""
        # TODO: LangGraph 그래프와 노드 연결을 구현한다.
        raise NotImplementedError
