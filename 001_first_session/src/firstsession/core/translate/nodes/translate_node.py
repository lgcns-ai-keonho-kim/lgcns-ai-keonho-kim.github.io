# 목적: 번역을 수행하는 노드를 정의한다.
# 설명: 프롬프트 생성과 모델 호출을 포함할 수 있다.
# 디자인 패턴: 전략 패턴 + 파이프라인 노드
# 참조: docs/04_string_tricks/05_retry_logic.md

"""번역 수행 노드 모듈."""

from firstsession.core.translate.state.translation_state import TranslationState


class TranslateNode:
    """번역 수행을 담당하는 노드."""

    def run(self, state: TranslationState) -> TranslationState:
        """번역 결과를 생성한다.

        Args:
            state: 현재 번역 상태.

        Returns:
            TranslationState: 번역 결과가 포함된 상태.
        """
        # TODO: 번역 프롬프트를 구성하고 모델/외부 API를 호출한다.
        # TODO: 번역 결과를 상태에 기록하는 규칙을 정의한다.
        raise NotImplementedError("번역 수행 로직을 구현해야 합니다.")
