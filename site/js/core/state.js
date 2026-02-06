/*
목적: 애플리케이션 상태를 단일 객체로 보관한다.
설명: 세션/뷰/트리/경로 등 전역 상태를 한 곳에서 관리한다.
디자인 패턴: 상태 컨테이너.
참조: site/js/app/main.js
*/
export const AppState = {
  data: {
    manifest: null,
    docsPaths: [],
    codePaths: [],
    docsTrees: {},
    codeTrees: {},
    currentSessionId: null,
    currentView: "docs",
    currentPath: "",
  },
};
