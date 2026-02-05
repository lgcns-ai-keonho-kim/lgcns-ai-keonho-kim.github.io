# 사이트 구조 안내

`site/` 아래는 정적 튜토리얼 웹을 구성하는 프론트엔드 리소스입니다.
각 디렉터리의 책임을 간단히 정리했습니다.

```text
site/
├─ assets/
├─ css/
│  └─ styles.css
├─ data/
│  ├─ home.json
│  ├─ manifest.json
│  ├─ docs_paths.txt
│  └─ code_paths.txt
├─ js/
│  ├─ app/
│  │  └─ main.js
│  ├─ core/
│  │  ├─ dom.js
│  │  ├─ router.js
│  │  └─ state.js
│  ├─ features/
│  │  ├─ navigation/
│  │  │  └─ top-nav.js
│  │  ├─ sidebar/
│  │  │  ├─ section.js
│  │  │  └─ tree-renderer.js
│  │  └─ viewer/
│  │     ├─ content.js
│  │     ├─ highlight.js
│  │     ├─ home-data.js
│  │     ├─ home.js
│  │     ├─ markdown.js
│  │     ├─ mermaid.js
│  │     ├─ utils.js
│  │     └─ viewer.js
│  ├─ services/
│  │  └─ data-service.js
│  └─ shared/
│     ├─ label-format.js
│     └─ path-utils.js
└─ libs/
   ├─ github.min.css
   ├─ highlight.min.js
   ├─ marked.min.js
   └─ mermaid.min.js
```

## 디렉터리 책임

- `assets/`
  이미지, 아이콘 등 정적 리소스.
- `css/`
  전체 UI 스타일 정의.
- `data/`
  세션 메타데이터와 경로, 홈 화면 콘텐츠 데이터.
- `js/`
  앱 로직. 아래 역할 분리 기준으로 구성됨.
- `libs/`
  외부 라이브러리 로컬 배치(오프라인 대응).

## JS 하위 구조

- `app/`
  앱 부트스트랩과 이벤트 바인딩.
- `core/`
  라우팅, DOM, 전역 상태 등 핵심 인프라.
- `services/`
  데이터 로딩 등 외부 데이터 접근 계층.
- `features/`
  화면 기능 단위(UI 컴포넌트/뷰) 모듈.
- `shared/`
  공통 유틸리티(경로/라벨 규칙 등).
