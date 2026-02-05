# 첫번째 세션

이 프로젝트는 LangChain/LangGraph 입문자를 대상으로 한 **실전형 교육 코스**입니다.
"LLM은 텍스트를 반환하는 도구"라는 관점을 중심으로, 프롬프트 설계부터 그래프 기반 처리까지 단계적으로 학습합니다.

## 교육 방향성

- **한 작업-한 프롬프트** 원칙을 기반으로 설계를 분리한다.
- LLM 출력은 **파싱 → 검증 → 정규화**로 안정화한다.
- LangGraph를 사용해 **태스크 분리와 흐름 제어**를 구현한다.
- 실패 응답은 **재시도 전략**으로 복구한다.

## 학습 콘텐츠

- 교재 문서: `docs/`
- 코드 템플릿: `src/firstsession/`
- 번역 API 엔드포인트: `/api/v1/translate`

## 구현해야 하는 과제

아래 항목은 코드의 `TODO`/`NotImplementedError`를 기준으로 정리했습니다.
학습자는 각 항목을 직접 구현해 전체 번역 파이프라인을 완성합니다.

### 1) API/서비스 레이어 구현

- `src/firstsession/api/translate/router/translate_router.py`
  - 라우터 초기화(경로/태그/의존성 연결)
  - `/api/v1/translate` 처리 로직에서 서비스 호출 및 응답 반환
- `src/firstsession/api/translate/service/translation_service.py`
  - `TranslateGraph` 의존성 주입 및 보관
  - 요청 → 상태 변환, 그래프 실행, 상태 → 응답 변환

### 2) 그래프 구성/실행 로직

- `src/firstsession/core/translate/graphs/translate_graph.py`
  - 그래프 초기화 및 실행(`run`)
  - START부터 각 노드 등록 및 엣지 연결
  - 조건부 엣지 설계(PASS/차단, QC 통과/실패, 재시도 루프)

### 3) LangGraph 노드 구현

- `src/firstsession/core/translate/nodes/normalize_input_node.py`
  - 언어 코드 표준화, 공백/길이 규칙, 민감 정보 처리
- `src/firstsession/core/translate/nodes/safeguard_classify_node.py`
  - 안전 분류(PASS/PII/HARMFUL/PROMPT_INJECTION) 산출 및 정규화
- `src/firstsession/core/translate/nodes/safeguard_decision_node.py`
  - PASS 여부 판단 및 오류 메시지 매핑
- `src/firstsession/core/translate/nodes/safeguard_fail_response_node.py`
  - 차단 응답 필드 구성 및 로깅 규칙
- `src/firstsession/core/translate/nodes/translate_node.py`
  - 번역 프롬프트 구성 및 번역 결과 기록
- `src/firstsession/core/translate/nodes/call_model_node.py`
  - 모델 호출 인터페이스와 에러 처리, 응답 파싱/정규화
- `src/firstsession/core/translate/nodes/quality_check_node.py`
  - QC 프롬프트로 YES/NO 판정 및 기록
- `src/firstsession/core/translate/nodes/retry_gate_node.py`
  - 재시도 가능 여부 판단 및 분기 규칙
- `src/firstsession/core/translate/nodes/retry_translate_node.py`
  - 재번역 수행 및 재시도 횟수 갱신
- `src/firstsession/core/translate/nodes/postprocess_node.py`
  - 번역 결과 검증/정규화 및 표준 에러 처리
- `src/firstsession/core/translate/nodes/response_node.py`
  - 최종 응답 필드 구성 및 성공/실패 우선순위 결정

### 4) 선택 과제: 테스트 코드 작성

- `pytest` 기반으로 핵심 흐름 테스트 작성
- **모킹 없이** 실제 로직을 검증하는 테스트 설계

---

## 목표 플로우

1) 입력 정규화  
2) 안전 분류 및 차단 여부 결정  
3) 번역 수행  
4) 품질 검사(QC)  
5) 재시도 루프(필요 시)  
6) 최종 응답 구성

## 실행 방법

```bash
uv run uvicorn firstsession.main:app --host 0.0.0.0 --port 8000 --reload
```

또는 

```bash
uv run python -m firstsession.main
```

## 기본 엔드포인트

- 헬스 체크: `GET /health`
- 번역 요청: `POST /api/v1/translate`

## 주요 위치

- 애플리케이션 진입점: `src/firstsession/api/main.py`
- API 영역: `src/firstsession/api`
- Core 영역: `src/firstsession/core`

## 환경 설정

프로젝트 루트에서 아래 순서로 실행하세요.

```txt
uv venv .venv
uv sync
```
