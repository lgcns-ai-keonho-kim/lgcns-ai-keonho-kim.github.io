# 목적: CLI 엔트리포인트를 제공한다.
# 설명: secondsession 명령으로 FastAPI 서버를 실행한다.
# 디자인 패턴: 파사드
# 참조: secondsession/main.py

"""secondsession 패키지 엔트리포인트 모듈."""


def main() -> None:
    """FastAPI 서버를 실행한다."""
    import uvicorn

    uvicorn.run("secondsession.main:app", host="0.0.0.0", port=8000, reload=True)
