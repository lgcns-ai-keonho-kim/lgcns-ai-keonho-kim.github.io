/*
목적: 메인 홈 화면을 렌더링한다.
설명: 데이터 기반으로 히어로/블루프린트/카드를 생성한다.
디자인 패턴: 템플릿 메서드(데이터 주입형).
참조: site/js/features/viewer/utils.js
*/
import { animateViewer, setBreadcrumb } from "./utils.js";
import { loadHomeData } from "./home-data.js";

const fallbackData = {
  hero: {
    kicker: "LG CNS · Solution Delivery",
    title: "프로젝트 수행을 위한",
    accent: "AI Engineer 교육",
    subtitle:
      "실제 업무 흐름에 맞춰 설계·구현·운영 역량을 강화하는 실전형 커리큘럼입니다. 문서와 코드 템플릿을 중심으로 세션별 핵심 패턴을 학습합니다.",
    pills: ["4 Sessions", "Docs + Code", "실전형 커리큘럼"],
  },
  blueprint: {
    label: "Blue Print",
    ascii: [
      "/---------\\   /---------\\   /---------\\",
      "| DESIGN  |-->|  BUILD  |-->| OPERATE |",
      "\\---------/   \\---------/   \\---------/",
    ],
    stats: [
      { label: "Sessions", value: "4" },
      { label: "Modules", value: "Docs/Code" },
      { label: "Focus", value: "Delivery" },
    ],
  },
  features: [],
};

function renderPills(pills = []) {
  return pills.map((pill) => `<span class="hero-pill">${pill}</span>`).join("");
}

function renderStats(stats = []) {
  return stats
    .map(
      (stat) => `
        <div>
          <span class="stat-title">${stat.label}</span>
          <strong>${stat.value}</strong>
        </div>
      `
    )
    .join("");
}

function renderFeatures(features = []) {
  return features
    .map(
      (feature) => `
        <article class="feature-card">
          <h3>${feature.title}</h3>
          <ul>
            ${feature.items.map((item) => `<li>${item}</li>`).join("")}
          </ul>
        </article>
      `
    )
    .join("");
}

export async function renderHome(viewer, breadcrumb) {
  const data = (await loadHomeData()) || fallbackData;
  const blueprintAscii = (data.blueprint?.ascii || fallbackData.blueprint.ascii).join("\n");
  viewer.innerHTML = `
    <section class="hero hero-main">
      <div class="hero-panel course-panel">
        <span class="hero-kicker">${data.hero?.kicker || fallbackData.hero.kicker}</span>
        <h1 class="hero-title">
          ${data.hero?.title || fallbackData.hero.title}
          <span class="hero-accent">${data.hero?.accent || fallbackData.hero.accent}</span>
        </h1>
        <p class="hero-sub">${data.hero?.subtitle || fallbackData.hero.subtitle}</p>
        <div class="hero-meta">${renderPills(data.hero?.pills || fallbackData.hero.pills)}</div>
      </div>
      <div class="hero-panel blueprint-panel">
        <div class="blueprint-label">${data.blueprint?.label || fallbackData.blueprint.label}</div>
        <pre class="blueprint-track ascii">${blueprintAscii}</pre>
        <div class="blueprint-grid">${renderStats(data.blueprint?.stats || fallbackData.blueprint.stats)}</div>
      </div>
      <div class="feature-grid">${renderFeatures(data.features || fallbackData.features)}</div>
    </section>
  `;
  setBreadcrumb(breadcrumb, "MAIN");
  animateViewer(viewer);
}
