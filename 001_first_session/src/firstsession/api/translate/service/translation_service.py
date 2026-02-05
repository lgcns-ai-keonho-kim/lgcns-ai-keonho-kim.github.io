# 목적: 번역 서비스 계층을 제공한다.
# 설명: 요청 모델을 번역하고 응답 모델로 변환한다.
# 디자인 패턴: 서비스 레이어 패턴
# 참조: firstsession/api/translate/router/translate_router.py

"""번역 서비스 모듈."""

from firstsession.api.translate.model.translation_request import TranslationRequest
from firstsession.api.translate.model.translation_response import TranslationResponse
from firstsession.core.translate.graphs.translate_graph import TranslateGraph


class TranslationService:
    """번역 요청을 처리하는 서비스."""

    def __init__(self, graph: TranslateGraph) -> None:
        """서비스 의존성을 초기화한다.

        Args:
            graph: 번역 그래프 실행기.
        """
        raise NotImplementedError("서비스 초기화 로직을 구현해야 합니다.")

    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """번역 요청을 처리한다.

        Args:
            request: 번역 요청 데이터.

        Returns:
            TranslationResponse: 번역 결과 응답.
        """
        raise NotImplementedError("번역 서비스 처리 로직을 구현해야 합니다.")
