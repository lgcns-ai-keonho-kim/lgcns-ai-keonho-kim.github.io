/*
목적: Mermaid 다이어그램을 렌더링한다.
설명: Markdown 내 mermaid 코드 블록을 Mermaid 노드로 변환 후 렌더링한다.
디자인 패턴: 어댑터.
참조: site/js/features/viewer/viewer.js
*/
let configured = false;

function getMermaid() {
  return window.mermaid;
}

function setupMermaid() {
  const mermaid = getMermaid();
  if (!mermaid || configured) {
    return;
  }
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "loose",
  });
  configured = true;
}

function transformBlocks(container) {
  const blocks = container.querySelectorAll("pre > code.language-mermaid");
  blocks.forEach((code) => {
    const pre = code.parentElement;
    if (!pre) {
      return;
    }
    const node = document.createElement("pre");
    node.className = "mermaid";
    node.textContent = code.textContent;
    pre.replaceWith(node);
  });
}

export const MermaidRenderer = {
  async render(container) {
    const mermaid = getMermaid();
    if (!mermaid || !container) {
      return;
    }
    setupMermaid();
    transformBlocks(container);
    const nodes = container.querySelectorAll(".mermaid");
    if (!nodes.length || typeof mermaid.run !== "function") {
      return;
    }
    try {
      await mermaid.run({ nodes });
    } catch (error) {
      console.warn("Mermaid 렌더링 실패:", error);
    }
  },
};
