/*
목적: 뷰어 공통 유틸리티를 제공한다.
설명: 브레드크럼 설정과 전환 애니메이션을 담당한다.
디자인 패턴: 유틸리티 모듈.
참조: site/js/features/viewer/content.js, site/js/features/viewer/home.js
*/
export function setBreadcrumb(element, path) {
  element.textContent = path || "";
}

export function animateViewer(container) {
  container.classList.remove("is-animate");
  void container.offsetWidth;
  container.classList.add("is-animate");
}
