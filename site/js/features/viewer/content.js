/*
목적: 파일 콘텐츠를 렌더링한다.
설명: Markdown/코드 분기와 Mermaid/하이라이트 처리를 수행한다.
디자인 패턴: 전략 패턴.
참조: site/js/features/viewer/markdown.js
*/
import { PathUtils } from "../../shared/path-utils.js";
import { renderMarkdown } from "./markdown.js";
import { Highlighter } from "./highlight.js";
import { MermaidRenderer } from "./mermaid.js";
import { animateViewer, setBreadcrumb } from "./utils.js";

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

async function renderMarkdownContent(container, markdownText) {
  container.innerHTML = renderMarkdown(markdownText);
  await MermaidRenderer.render(container);
  Highlighter.highlightContainer(container);
}

export async function renderContent(viewer, breadcrumb, path) {
  if (!path) {
    viewer.innerHTML = "<div class=\"empty-state\">표시할 문서를 선택하세요.</div>";
    setBreadcrumb(breadcrumb, "");
    return;
  }

  try {
    const response = await fetch(path);
    if (!response.ok) {
      throw new Error("파일을 불러오지 못했습니다.");
    }
    const text = await response.text();
    if (PathUtils.isMarkdown(path)) {
      await renderMarkdownContent(viewer, text);
    } else {
      renderCode(viewer, text, PathUtils.getLanguage(path));
    }
    animateViewer(viewer);
    setBreadcrumb(breadcrumb, path);
  } catch (error) {
    viewer.innerHTML = "<div class=\"empty-state\">콘텐츠를 불러오는 중 오류가 발생했습니다.</div>";
    setBreadcrumb(breadcrumb, path);
  }
}
