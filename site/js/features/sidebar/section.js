/*
목적: Docs/Code 섹션 상태를 제어한다.
설명: 활성/비활성/표시 여부를 세션 기준으로 업데이트한다.
디자인 패턴: 상태 기반 뷰 업데이트.
참조: site/index.html
*/
export const SidebarSection = {
  update(sections, { hasDocs, hasCode, currentView }) {
    sections.forEach((section) => {
      const view = section.dataset.view;
      const enabled = view === "docs" ? hasDocs : hasCode;
      section.classList.toggle("is-disabled", !enabled);
      section.classList.toggle("is-active", view === currentView);
    });
  },

  toggleVisibility(shouldShow) {
    document.body.classList.toggle("sidebar-hidden", !shouldShow);
  },
};
