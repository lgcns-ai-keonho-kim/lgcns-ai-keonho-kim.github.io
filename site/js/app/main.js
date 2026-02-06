/*
목적: 앱 부트스트랩과 이벤트 바인딩을 수행한다.
설명: 데이터 로딩 → 트리 생성 → UI 렌더 순서로 초기화한다.
디자인 패턴: 애플리케이션 서비스.
참조: site/js/features/*
*/
import { AppState } from "../core/state.js";
import { Dom } from "../core/dom.js";
import { Router } from "../core/router.js";
import { DataService } from "../services/data-service.js";
import { TopNav } from "../features/navigation/top-nav.js";
import { SidebarSection } from "../features/sidebar/section.js";
import { buildTree, renderTree, syncTreeSelection } from "../features/sidebar/tree-renderer.js";
import { renderContent, renderHome } from "../features/viewer/viewer.js";

const ui = Dom.getUI();

function getSessionById(sessionId) {
  return AppState.data.manifest.sessions.find(
    (session) => session.id === sessionId
  );
}

function updateTopNav() {
  TopNav.render(
    ui.topNav,
    AppState.data.manifest.sessions,
    AppState.data.currentSessionId
  );
}

function updateSections() {
  const session = getSessionById(AppState.data.currentSessionId);
  const hasDocs = Boolean(session?.docs_root);
  const hasCode = Boolean(session?.code_root);

  SidebarSection.update(ui.sections, {
    hasDocs,
    hasCode,
    currentView: AppState.data.currentView,
  });
  SidebarSection.toggleVisibility(hasDocs || hasCode);
}

function ensureSessionTrees(session) {
  if (!session) {
    return;
  }
  if (session.docs_root && !AppState.data.docsTrees[session.id]) {
    AppState.data.docsTrees[session.id] = buildTree(
      AppState.data.docsPaths,
      session.docs_root
    );
  }
  if (session.code_root && !AppState.data.codeTrees[session.id]) {
    AppState.data.codeTrees[session.id] = buildTree(
      AppState.data.codePaths,
      session.code_root
    );
  }
}

function renderSessionTrees(session) {
  if (!session || session.id === "MAIN") {
    renderTree(ui.docsTree, null, "", { labelStyle: "docs" });
    renderTree(ui.codeTree, null, "");
    return;
  }

  renderTree(
    ui.docsTree,
    AppState.data.docsTrees[session.id],
    AppState.data.currentPath,
    { labelStyle: "docs" }
  );
  renderTree(ui.codeTree, AppState.data.codeTrees[session.id], AppState.data.currentPath);
}

function syncActiveTrees() {
  syncTreeSelection(ui.docsTree, AppState.data.currentPath);
  syncTreeSelection(ui.codeTree, AppState.data.currentPath);
}

function syncHash() {
  Router.write({
    sessionId: AppState.data.currentSessionId,
    view: AppState.data.currentView,
    path: AppState.data.currentPath,
  });
}

async function selectPath(path, { updateUrl = true } = {}) {
  AppState.data.currentPath = path;
  syncActiveTrees();
  await renderContent(ui.viewer, ui.breadcrumb, path);
  syncActiveTrees();
  if (updateUrl) {
    syncHash();
  }
}

async function selectSession(sessionId, options = {}) {
  const session = getSessionById(sessionId);
  if (!session) {
    return;
  }
  AppState.data.currentSessionId = sessionId;
  AppState.data.currentView = session.docs_root ? "docs" : "code";
  AppState.data.currentPath = options.initialPath || "";
  document.body.classList.toggle("main-mode", sessionId === "MAIN");
  ensureSessionTrees(session);
  updateTopNav();
  updateSections();
  renderSessionTrees(session);
  syncActiveTrees();

  if (sessionId === "MAIN") {
    await renderHome(ui.viewer, ui.breadcrumb);
    syncHash();
    return;
  }

  if (!options.skipReadme) {
    await selectPath(session.readme, { updateUrl: false });
    syncHash();
  }
}

async function applyRouteState() {
  const route = Router.read(AppState.data.manifest.site.default_session);
  await selectSession(route.sessionId, {
    skipReadme: Boolean(route.path),
    initialPath: route.path || "",
  });
  if (
    route.view &&
    (route.view === "docs" || route.view === "code") &&
    route.sessionId !== "MAIN"
  ) {
    AppState.data.currentView = route.view;
    updateSections();
  }
  if (route.path && route.sessionId !== "MAIN") {
    await selectPath(route.path, { updateUrl: false });
    syncHash();
  }
}

function bindEvents() {
  ui.brandHome.addEventListener("click", () => {
    selectSession("MAIN");
  });

  ui.topNav.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-session]");
    if (!button) {
      return;
    }
    selectSession(button.dataset.session);
  });

  const handleTreeClick = (event) => {
    const button = event.target.closest("button[data-path]");
    if (!button) {
      return;
    }
    const section = event.currentTarget.closest(".sidebar-section");
    if (section?.dataset.view) {
      AppState.data.currentView = section.dataset.view;
      updateSections();
    }
    selectPath(button.dataset.path);
    document.body.classList.remove("sidebar-open");
  };
  ui.docsTree.addEventListener("click", handleTreeClick);
  ui.codeTree.addEventListener("click", handleTreeClick);

  ui.toggleSidebar.addEventListener("click", () => {
    document.body.classList.toggle("sidebar-open");
  });

  window.addEventListener("hashchange", () => {
    applyRouteState();
  });
}

async function init() {
  AppState.data.manifest = await DataService.loadManifest();
  AppState.data.docsPaths = await DataService.loadPaths("docs_paths.txt");
  AppState.data.codePaths = await DataService.loadPaths("code_paths.txt");

  bindEvents();
  await applyRouteState();
  ui.app.setAttribute("data-ready", "true");
}

init().catch((error) => {
  ui.viewer.innerHTML = "<div class=\"empty-state\">앱 초기화 중 오류가 발생했습니다.</div>";
  ui.breadcrumb.textContent = String(error);
  ui.app.setAttribute("data-ready", "true");
});
