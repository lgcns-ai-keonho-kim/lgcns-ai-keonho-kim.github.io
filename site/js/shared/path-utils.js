/*
목적: 경로 문자열을 정규화하고 파일 타입을 판별한다.
설명: Markdown 여부, 코드 언어 등의 정보를 제공한다.
디자인 패턴: 유틸리티 모듈.
참조: site/js/services/data-service.js, site/js/features/viewer/viewer.js
*/
export const PathUtils = {
  normalizePath(line) {
    return line.replace(/^\.\//, "").trim();
  },

  isMarkdown(path) {
    return path.toLowerCase().endsWith(".md");
  },

  getLanguage(path) {
    const lower = path.toLowerCase();
    if (lower.endsWith(".py")) {
      return "python";
    }
    if (lower.endsWith(".js")) {
      return "javascript";
    }
    if (lower.endsWith(".ts")) {
      return "typescript";
    }
    return "";
  },
};
