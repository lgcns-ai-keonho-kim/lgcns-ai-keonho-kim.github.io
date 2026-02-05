# 목적: 번역 모델 호출 노드를 정의한다.
# 설명: 실제 LLM/외부 번역 API 호출을 이 위치에서 수행한다.
# 디자인 패턴: 파이프라인 노드
# 참조: firstsession/core/translate/graphs/translate_graph.py

"""모델 호출 노드 모듈."""

from firstsession.core.translate.state.translation_state import TranslationState


class CallModelNode:
    """모델 호출을 담당하는 노드."""

    def run(self, state: TranslationState) -> TranslationState:
        """프롬프트를 기반으로 번역 결과를 생성한다.

        Args:
            state: 현재 번역 상태.

        Returns:
            TranslationState: 번역 결과가 포함된 상태.
        """
        # TODO: 모델 호출 인터페이스와 에러 처리 규칙을 구현한다.
        # TODO: 응답 텍스트 파싱 및 정규화 규칙을 정의한다.
        raise NotImplementedError("모델 호출 로직을 구현해야 합니다.")
