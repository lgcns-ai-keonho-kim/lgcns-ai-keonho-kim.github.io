/*
목적: Markdown을 HTML로 변환한다.
설명: marked 라이브러리를 사용해 HTML 문자열을 반환한다.
디자인 패턴: 어댑터.
참조: site/js/features/viewer/viewer.js
*/
let configured = false;

export function renderMarkdown(markdownText) {
  if (!window.marked) {
    return "<div class=\"empty-state\">Markdown 라이브러리가 없습니다.</div>";
  }
  if (!configured) {
    window.marked.setOptions({
      langPrefix: "language-",
    });
    configured = true;
  }
  return window.marked.parse(markdownText);
}
