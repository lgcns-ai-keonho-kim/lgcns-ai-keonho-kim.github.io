/*
목적: 하이라이트 적용 로직을 제공한다.
설명: 외부 라이브러리가 없을 때 간단한 Python 하이라이트를 수행한다.
디자인 패턴: 전략 패턴(외부 라이브러리/폴백).
참조: site/js/features/viewer/viewer.js
*/
function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function highlightPython(code) {
  const pattern = new RegExp(
    "(#.*$)|(\"[^\"]*\"|'[^']*')|(\\b\\d+(?:\\.\\d+)?\\b)|(\\b(?:def|class|return|if|elif|else|for|while|break|continue|try|except|finally|with|as|import|from|pass|raise|yield|lambda|True|False|None|and|or|not|in|is)\\b)",
    "gm"
  );

  let result = "";
  let lastIndex = 0;
  let match = pattern.exec(code);
  while (match) {
    result += escapeHtml(code.slice(lastIndex, match.index));
    if (match[1]) {
      result += `<span class=\"tok-com\">${escapeHtml(match[1])}</span>`;
    } else if (match[2]) {
      result += `<span class=\"tok-str\">${escapeHtml(match[2])}</span>`;
    } else if (match[3]) {
      result += `<span class=\"tok-num\">${escapeHtml(match[3])}</span>`;
    } else if (match[4]) {
      result += `<span class=\"tok-kw\">${escapeHtml(match[4])}</span>`;
    } else {
      result += escapeHtml(match[0]);
    }
    lastIndex = pattern.lastIndex;
    match = pattern.exec(code);
  }
  result += escapeHtml(code.slice(lastIndex));
  return result;
}

function highlightBash(code) {
  const pattern = new RegExp(
    "(#.*$)|(\"[^\"]*\"|'[^']*')|(\\$\\{[^}]+\\}|\\$[A-Za-z_][A-Za-z0-9_]*)|(\\b\\d+\\b)|(\\b(?:if|then|fi|for|in|do|done|while|case|esac|function|return|exit|export|local|set|unset|alias|source|readonly|shift|break|continue)\\b)",
    "gm"
  );

  let result = "";
  let lastIndex = 0;
  let match = pattern.exec(code);
  while (match) {
    result += escapeHtml(code.slice(lastIndex, match.index));
    if (match[1]) {
      result += `<span class=\"tok-com\">${escapeHtml(match[1])}</span>`;
    } else if (match[2]) {
      result += `<span class=\"tok-str\">${escapeHtml(match[2])}</span>`;
    } else if (match[3]) {
      result += `<span class=\"tok-var\">${escapeHtml(match[3])}</span>`;
    } else if (match[4]) {
      result += `<span class=\"tok-num\">${escapeHtml(match[4])}</span>`;
    } else if (match[5]) {
      result += `<span class=\"tok-kw\">${escapeHtml(match[5])}</span>`;
    } else {
      result += escapeHtml(match[0]);
    }
    lastIndex = pattern.lastIndex;
    match = pattern.exec(code);
  }
  result += escapeHtml(code.slice(lastIndex));
  return result;
}

function simpleHighlight(code, language) {
  const lang = (language || "").toLowerCase();
  if (!lang) {
    return escapeHtml(code);
  }
  if (lang === "py" || lang === "python") {
    return highlightPython(code);
  }
  if (lang === "bash" || lang === "sh" || lang === "shell" || lang === "zsh") {
    return highlightBash(code);
  }
  return escapeHtml(code);
}

export const Highlighter = {
  highlightBlock(block, language) {
    const canUseHljs =
      window.hljs && typeof window.hljs.highlightElement === "function";
    const hasLanguage =
      canUseHljs && typeof window.hljs.getLanguage === "function"
        ? Boolean(window.hljs.getLanguage(language))
        : true;
    if (canUseHljs) {
      if (language && !hasLanguage) {
        const highlighted = simpleHighlight(block.textContent, language);
        block.innerHTML = highlighted;
        return;
      }
      window.hljs.highlightElement(block);
      return;
    }
    const highlighted = simpleHighlight(block.textContent, language);
    block.innerHTML = highlighted;
  },

  highlightContainer(container) {
    const blocks = container.querySelectorAll("pre code");
    blocks.forEach((block) => {
      const language = block.className.match(/language-([a-z0-9]+)/i);
      const lang = language ? language[1].toLowerCase() : "";
      Highlighter.highlightBlock(block, lang);
    });
  },

  highlightText(code, language) {
    const canUseHljs =
      window.hljs && typeof window.hljs.highlightElement === "function";
    if (!canUseHljs) {
      return simpleHighlight(code, language);
    }
    return escapeHtml(code);
  },
};
