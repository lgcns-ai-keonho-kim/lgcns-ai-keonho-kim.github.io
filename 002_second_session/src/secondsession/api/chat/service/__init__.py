# 목적: 채팅 서비스 모듈을 외부에 노출한다.
# 설명: 서비스 클래스의 진입점을 제공한다.
# 디자인 패턴: 파사드
# 참조: secondsession/api/chat/router/chat_router.py

"""채팅 서비스 패키지."""

from secondsession.api.chat.service.chat_service import ChatService

__all__ = ["ChatService"]
