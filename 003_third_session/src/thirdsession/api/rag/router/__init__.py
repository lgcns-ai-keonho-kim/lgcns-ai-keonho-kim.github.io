# 목적: RAG 라우터 등록 함수를 제공한다.
# 설명: app.state에 있는 서비스를 이용해 라우터를 합성/등록한다.
# 디자인 패턴: 파사드
# 참조: thirdsession/api/rag/router/rag_router.py, rag_*_router.py

"""RAG 라우터 등록 모듈."""

from fastapi import APIRouter, FastAPI

from thirdsession.api.rag.const import API_V1_PREFIX, JOB_PREFIX, JOB_TAG, RAG_PREFIX, RAG_TAG
from thirdsession.api.rag.router.rag_cancel_router import RagCancelRouter
from thirdsession.api.rag.router.rag_job_router import RagJobRouter
from thirdsession.api.rag.router.rag_status_router import RagStatusRouter
from thirdsession.api.rag.router.rag_stream_router import RagStreamRouter
from thirdsession.api.rag.router.rag_router import RagRouter
from thirdsession.api.rag.service.rag_job_service import RagJobService
from thirdsession.api.rag.service.rag_service import RagService


def register_rag_routes(app: FastAPI) -> None:
    """RAG 라우터를 애플리케이션에 등록한다.

    Args:
        app: FastAPI 애플리케이션 인스턴스.
    """
    rag_service: RagService = app.state.rag_service
    job_service: RagJobService = app.state.job_service
    api_router = APIRouter(prefix=API_V1_PREFIX)
    rag_router = APIRouter(prefix=RAG_PREFIX, tags=[RAG_TAG])
    job_router = APIRouter(prefix=JOB_PREFIX, tags=[JOB_TAG])

    rag_router.include_router(RagRouter(rag_service).router)
    job_router.include_router(RagJobRouter(job_service).router)
    job_router.include_router(RagStreamRouter(job_service).router)
    job_router.include_router(RagStatusRouter(job_service).router)
    job_router.include_router(RagCancelRouter(job_service).router)
    api_router.include_router(rag_router)
    api_router.include_router(job_router)
    app.include_router(api_router)


__all__ = ["register_rag_routes"]
