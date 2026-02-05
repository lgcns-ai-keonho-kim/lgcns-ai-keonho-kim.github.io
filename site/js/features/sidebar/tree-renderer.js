/*
목적: 문서/코드 트리를 생성하고 DOM에 렌더링한다.
설명: 경로 목록을 트리로 변환하고 버튼/디테일을 구성한다.
디자인 패턴: 재귀적 트리 렌더링.
참조: site/index.html, site/js/shared/label-format.js
*/
import { formatDocsLabel } from "../../shared/label-format.js";
function createNode(name, type, path) {
  return { name, type, path, children: [] };
}

function sortChildren(children) {
  return children.sort((a, b) => {
    if (a.type !== b.type) {
      return a.type === "dir" ? -1 : 1;
    }
    return a.name.localeCompare(b.name, "ko");
  });
}

export function buildTree(paths, root) {
  const rootPath = root.replace(/\/$/, "");
  const rootNode = createNode(rootPath.split("/").pop(), "dir", rootPath);
  const index = new Map();
  index.set(rootNode.path, rootNode);

  paths.forEach((path) => {
    if (!path.startsWith(`${rootPath}/`)) {
      return;
    }
    const relPath = path.slice(rootPath.length + 1);
    const parts = relPath.split("/");
    let currentPath = rootPath;
    let currentNode = rootNode;

    parts.forEach((part, idx) => {
      const isLast = idx === parts.length - 1;
      const nodePath = `${currentPath}/${part}`;
      if (index.has(nodePath)) {
        currentNode = index.get(nodePath);
        currentPath = nodePath;
        return;
      }

      const nextNode = createNode(part, isLast ? "file" : "dir", nodePath);
      currentNode.children.push(nextNode);
      index.set(nodePath, nextNode);
      currentNode = nextNode;
      currentPath = nodePath;
    });
  });

  function finalize(node) {
    if (node.type === "dir") {
      node.children = sortChildren(node.children).map(finalize);
    }
    return node;
  }

  return finalize(rootNode);
}

function formatDisplayName(name, type, options = {}) {
  if (options.labelStyle !== "docs") {
    return name;
  }
  return formatDocsLabel(name, type);
}

function createFileButton(node, currentPath, options) {
  const item = document.createElement("div");
  item.className = "tree-item";

  const button = document.createElement("button");
  button.type = "button";
  button.textContent = formatDisplayName(node.name, node.type, options);
  button.dataset.path = node.path;
  if (node.path === currentPath) {
    button.classList.add("is-active");
  }
  item.appendChild(button);
  return item;
}

function renderNode(node, currentPath, options) {
  if (node.type === "file") {
    return createFileButton(node, currentPath, options);
  }

  const details = document.createElement("details");
  details.open = true;

  const summary = document.createElement("summary");
  summary.textContent = formatDisplayName(node.name, node.type, options);
  details.appendChild(summary);

  const list = document.createElement("div");
  node.children.forEach((child) => {
    list.appendChild(renderNode(child, currentPath, options));
  });
  details.appendChild(list);
  return details;
}

export function renderTree(container, tree, currentPath, options = {}) {
  container.innerHTML = "";
  if (!tree || !tree.children.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "표시할 항목이 없습니다.";
    container.appendChild(empty);
    return;
  }

  const list = document.createElement("div");
  list.className = "tree-list";
  tree.children.forEach((child) => {
    list.appendChild(renderNode(child, currentPath, options));
  });
  container.appendChild(list);
}
