/*
목적: 파일 콘텐츠를 빠르게 렌더링한다.
설명: Markdown/코드 분기와 Mermaid/하이라이트 처리에 캐시/요청 취소를 결합한다.
디자인 패턴: 전략 패턴 + 캐시.
참조: site/js/features/viewer/markdown.js
*/
import { PathUtils } from "../../shared/path-utils.js";
import { renderMarkdown } from "./markdown.js";
import { Highlighter } from "./highlight.js";
import { MermaidRenderer } from "./mermaid.js";
import { animateViewer, setBreadcrumb } from "./utils.js";

const contentCache = new Map();

let activeController = null;
let latestRequestId = 0;

function cancelActiveRequest() {
  if (activeController) {
    activeController.abort();
    activeController = null;
  }
}

async function loadContentText(path) {
  const cached = contentCache.get(path);
  if (typeof cached === "string") {
    return cached;
  }

  const controller = new AbortController();
  activeController = controller;
  try {
    const response = await fetch(path, {
      signal: controller.signal,
      cache: "force-cache",
    });
    if (!response.ok) {
      throw new Error("파일을 불러오지 못했습니다.");
    }
    const text = await response.text();
    contentCache.set(path, text);
    return text;
  } finally {
    if (activeController === controller) {
      activeController = null;
    }
  }
}

function renderCode(container, codeText, language) {
  container.innerHTML = "";
  const pre = document.createElement("pre");
  const code = document.createElement("code");
  code.className = language ? `language-${language}` : "";
  code.textContent = codeText;
  pre.appendChild(code);
  container.appendChild(pre);
  Highlighter.highlightContainer(container);
}

async function renderMarkdownContent(container, markdownText, shouldContinue) {
  if (!shouldContinue()) {
    return;
  }
  container.innerHTML = renderMarkdown(markdownText);
  if (!shouldContinue()) {
    return;
  }
  await MermaidRenderer.render(container);
  if (!shouldContinue()) {
    return;
  }
  Highlighter.highlightContainer(container);
}

export async function renderContent(viewer, breadcrumb, path) {
  const requestId = ++latestRequestId;
  const isLatestRequest = () => requestId === latestRequestId;
  cancelActiveRequest();

  if (!path) {
    viewer.innerHTML = "<div class=\"empty-state\">표시할 문서를 선택하세요.</div>";
    setBreadcrumb(breadcrumb, "");
    return;
  }

  try {
    const text = await loadContentText(path);
    if (!isLatestRequest()) {
      return;
    }
    if (PathUtils.isMarkdown(path)) {
      await renderMarkdownContent(viewer, text, isLatestRequest);
    } else {
      renderCode(viewer, text, PathUtils.getLanguage(path));
    }
    if (!isLatestRequest()) {
      return;
    }
    animateViewer(viewer);
    setBreadcrumb(breadcrumb, path);
  } catch (error) {
    if (!isLatestRequest() || error?.name === "AbortError") {
      return;
    }
    viewer.innerHTML = "<div class=\"empty-state\">콘텐츠를 불러오는 중 오류가 발생했습니다.</div>";
    setBreadcrumb(breadcrumb, path);
  }
}
