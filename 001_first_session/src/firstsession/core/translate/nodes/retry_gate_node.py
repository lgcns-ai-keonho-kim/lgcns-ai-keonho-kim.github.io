# 목적: 재번역 가능 여부를 판단한다.
# 설명: retry_count와 qc_passed를 기준으로 다음 경로를 결정한다.
# 디자인 패턴: 파이프라인 노드
# 참조: docs/04_string_tricks/05_retry_logic.md

"""재번역 게이트 노드 모듈."""

from firstsession.core.translate.state.translation_state import TranslationState


class RetryGateNode:
    """재번역 가능 여부를 판단하는 노드."""

    def run(self, state: TranslationState) -> TranslationState:
        """재번역 가능 여부를 판단한다.

        Args:
            state: 현재 번역 상태.

        Returns:
            TranslationState: 게이트 판단 결과가 포함된 상태.
        """
        # TODO: retry_count와 max_retry_count 기준으로 재번역 여부를 판단한다.
        # TODO: qc_passed 결과에 따른 분기 규칙을 정의한다.
        raise NotImplementedError("재번역 게이트 로직을 구현해야 합니다.")
