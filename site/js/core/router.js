/*
목적: 해시 기반 라우팅 상태를 읽고 쓴다.
설명: 세션/뷰/파일 경로를 URL 해시에 반영한다.
디자인 패턴: URL 상태 동기화.
참조: site/js/app/main.js
*/
export const Router = {
  read(defaultSession) {
    const rawHash = window.location.hash.replace("#", "");
    const params = new URLSearchParams(rawHash);
    return {
      sessionId: params.get("s") || defaultSession,
      view: params.get("v"),
      path: params.get("p"),
    };
  },

  write({ sessionId, view, path }) {
    const params = new URLSearchParams();
    params.set("s", sessionId);
    params.set("v", view);
    if (path) {
      params.set("p", path);
    }
    history.replaceState(null, "", `#${params.toString()}`);
  },
};
