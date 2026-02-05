/*
목적: UI에서 사용하는 DOM 참조를 한 번에 수집한다.
설명: 뷰 영역/사이드바/탭 등을 DOM 캐시로 제공한다.
디자인 패턴: DOM 레지스트리.
참조: site/index.html
*/
export const Dom = {
  getUI() {
    return {
      topNav: document.getElementById("topNav"),
      brandHome: document.getElementById("brandHome"),
      docsTree: document.getElementById("docsTree"),
      codeTree: document.getElementById("codeTree"),
      sections: document.querySelectorAll(".sidebar-section"),
      viewer: document.getElementById("viewer"),
      breadcrumb: document.getElementById("breadcrumb"),
      toggleSidebar: document.getElementById("toggleSidebar"),
      app: document.querySelector(".app"),
    };
  },
};
