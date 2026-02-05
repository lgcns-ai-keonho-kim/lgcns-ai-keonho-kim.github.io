/*
목적: 상단 세션 탭을 렌더링한다.
설명: 세션 목록을 버튼으로 만들고 활성 상태를 표시한다.
디자인 패턴: 프리젠터.
참조: site/index.html
*/
export const TopNav = {
  render(container, sessions, currentSessionId) {
    container.innerHTML = "";
    sessions.filter((session) => session.id !== "MAIN").forEach((session) => {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = session.label;
      button.dataset.session = session.id;
      if (session.id === currentSessionId) {
        button.classList.add("is-active");
      }
      container.appendChild(button);
    });
  },
};
