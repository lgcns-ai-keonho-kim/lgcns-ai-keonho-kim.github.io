# 목적: API 상수 모듈을 외부에 노출한다.
# 설명: 스트리밍 이벤트 타입을 집계한다.
# 디자인 패턴: 파사드
# 참조: secondsession/api/chat/const/stream_event_type.py

"""대화 API 상수 패키지."""

from secondsession.api.chat.const.stream_event_type import StreamEventType

__all__ = ["StreamEventType"]
