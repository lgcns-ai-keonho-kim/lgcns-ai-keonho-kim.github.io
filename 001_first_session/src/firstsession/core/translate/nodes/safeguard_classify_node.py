# 목적: 입력 문장을 안전 분류로 라우팅한다.
# 설명: PASS/PII/HARMFUL/PROMPT_INJECTION 라벨로 안전 여부를 판정한다.
# 디자인 패턴: 전략 패턴 + 파이프라인 노드
# 참조: docs/04_string_tricks/02_single_choice_파서.md

"""안전 분류 노드 모듈."""

from firstsession.core.translate.state.translation_state import TranslationState


class SafeguardClassifyNode:
    """안전 분류를 담당하는 노드."""

    def run(self, state: TranslationState) -> TranslationState:
        """입력에 대한 안전 라벨을 판정한다.

        Args:
            state: 현재 번역 상태.

        Returns:
            TranslationState: 안전 라벨이 포함된 상태.
        """
        # TODO: 안전 분류 프롬프트를 호출하고 PASS/PII/HARMFUL/PROMPT_INJECTION을 산출한다.
        # TODO: 출력 검증 및 정규화 규칙을 정의한다.
        raise NotImplementedError("안전 분류 로직을 구현해야 합니다.")
