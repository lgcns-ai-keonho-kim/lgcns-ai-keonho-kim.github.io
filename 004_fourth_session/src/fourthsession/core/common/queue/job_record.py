# 목적: 작업 레코드 모델을 정의한다.
# 설명: 작업 상태와 페이로드를 저장하는 구조를 제공한다.
# 디자인 패턴: 데이터 전송 객체(DTO)
# 참조: fourthsession/core/common/queue/inmemory_job_store.py

"""작업 레코드 모델 모듈."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class JobRecord:
    """작업 레코드."""

    job_id: str
    status: str
    payload: dict[str, Any]
    created_at: str
    updated_at: str
