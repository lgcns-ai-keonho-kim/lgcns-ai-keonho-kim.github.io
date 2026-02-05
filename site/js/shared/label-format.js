/*
목적: 트리 뷰 라벨 표시 규칙을 제공한다.
설명: Docs 트리에서 언더스코어를 공백으로, 영문은 대문자로 변환한다.
디자인 패턴: 유틸리티 모듈.
참조: site/js/features/sidebar/tree-renderer.js
*/
export function formatDocsLabel(name, type) {
  const hasExt = type === "file" && name.includes(".");
  const dotIndex = hasExt ? name.lastIndexOf(".") : -1;
  const base = hasExt ? name.slice(0, dotIndex) : name;
  const ext = hasExt ? name.slice(dotIndex) : "";
  const normalized = base.replace(/_+/g, " ");
  return `${normalized.toUpperCase()}${ext}`;
}
