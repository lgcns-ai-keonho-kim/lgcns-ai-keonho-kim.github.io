# 목적: 최종 응답을 구성하는 노드를 정의한다.
# 설명: 상태를 API 응답으로 변환하기 전 정리한다.
# 디자인 패턴: 파이프라인 노드
# 참조: firstsession/api/translate/model/translation_response.py

"""응답 구성 노드 모듈."""

from firstsession.core.translate.state.translation_state import TranslationState


class ResponseNode:
    """응답 구성을 담당하는 노드."""

    def run(self, state: TranslationState) -> TranslationState:
        """최종 응답을 위한 상태를 정리한다.

        Args:
            state: 현재 번역 상태.

        Returns:
            TranslationState: 응답 구성이 완료된 상태.
        """
        # TODO: 최종 응답에 필요한 필드만 추려 상태를 정리한다.
        # TODO: 에러 메시지와 성공 응답의 우선순위를 정의한다.
        raise NotImplementedError("응답 구성 로직을 구현해야 합니다.")
