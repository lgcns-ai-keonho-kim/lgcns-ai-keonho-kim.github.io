/*
목적: Mermaid 다이어그램을 지연 로딩으로 렌더링한다.
설명: Mermaid 코드 블록이 있을 때만 라이브러리를 로드해 렌더링 비용을 줄인다.
디자인 패턴: 지연 초기화 + 어댑터.
참조: site/js/features/viewer/content.js
*/
const MERMAID_SRC = "site/libs/mermaid.min.js";

let configured = false;
let loadPromise = null;

function getMermaid() {
  return window.mermaid || null;
}

function loadMermaidLibrary() {
  const existing = getMermaid();
  if (existing) {
    return Promise.resolve(existing);
  }
  if (loadPromise) {
    return loadPromise;
  }

  loadPromise = new Promise((resolve, reject) => {
    const existingScript = document.querySelector(`script[src="${MERMAID_SRC}"]`);
    if (existingScript) {
      const loaded = getMermaid();
      if (loaded) {
        resolve(loaded);
        return;
      }

      const handleLoad = () => {
        resolve(getMermaid());
      };
      const handleError = () => {
        reject(new Error("Mermaid 스크립트를 불러오지 못했습니다."));
      };

      existingScript.addEventListener("load", handleLoad, { once: true });
      existingScript.addEventListener("error", handleError, { once: true });

      // 이미 로드된 스크립트가 남아있는 경우를 대비해 즉시 한 번 더 확인한다.
      window.setTimeout(() => {
        const ready = getMermaid();
        if (!ready) {
          return;
        }
        existingScript.removeEventListener("load", handleLoad);
        existingScript.removeEventListener("error", handleError);
        resolve(ready);
      }, 0);
      return;
    }

    const script = document.createElement("script");
    script.src = MERMAID_SRC;
    script.async = true;
    script.addEventListener("load", () => {
      resolve(getMermaid());
    }, { once: true });
    script.addEventListener("error", () => {
      reject(new Error("Mermaid 스크립트를 불러오지 못했습니다."));
    }, { once: true });
    document.head.appendChild(script);
  }).catch((error) => {
    loadPromise = null;
    throw error;
  });

  return loadPromise;
}

function setupMermaid(mermaid) {
  if (!mermaid || configured) {
    return;
  }
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "loose",
  });
  configured = true;
}

function transformBlocks(blocks) {
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
    if (!container) {
      return;
    }

    const blocks = container.querySelectorAll("pre > code.language-mermaid");
    if (!blocks.length) {
      return;
    }

    let mermaid = null;
    try {
      mermaid = await loadMermaidLibrary();
    } catch (error) {
      console.warn("Mermaid 로드 실패:", error);
      return;
    }
    if (!mermaid) {
      return;
    }

    setupMermaid(mermaid);
    transformBlocks(blocks);

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
