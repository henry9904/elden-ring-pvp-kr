---
title: 무기 탐색기 / Weapon Explorer
---

# ⚔️ 무기 탐색기 / Weapon Explorer

> 각 가이드(직검·할버드·카타나)에 흩어져 있는 티어 표를 한 곳에서 검색·필터·정렬할 수 있어요.
> 무기명을 클릭하면 해당 가이드의 원본 섹션으로 이동합니다.
>
> Cross-guide weapon table — search, filter, and sort tier data parsed from
> the Straight Sword, Halberd, and Katana guides. Data is auto-generated from
> the markdown sources via `tools/extract_weapons.py`.

<style>
  .we-controls { display: flex; flex-wrap: wrap; gap: 1rem; margin-bottom: 1rem; align-items: flex-start; }
  .we-search-wrap { flex: 1; min-width: 240px; }
  .we-search { width: 100%; padding: 0.55rem 0.85rem; border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px; background: var(--md-default-bg-color); color: var(--md-default-fg-color); font-size: 0.9em; }
  .we-search:focus { outline: 2px solid var(--md-primary-fg-color); outline-offset: -1px; }
  .we-chip-group { display: flex; gap: 0.4rem; flex-wrap: wrap; align-items: center; }
  .we-chip-label { font-size: 0.8em; color: var(--md-default-fg-color--light); margin-right: 0.25rem; }
  .we-chip { display: inline-flex; align-items: center; padding: 0.3rem 0.75rem; border: 1px solid var(--md-default-fg-color--lightest); border-radius: 16px; cursor: pointer; user-select: none; font-size: 0.8em; transition: all 0.15s; }
  .we-chip:hover { border-color: var(--md-primary-fg-color); }
  .we-chip.active { background: var(--md-primary-fg-color); color: white; border-color: var(--md-primary-fg-color); }
  .we-table { width: 100%; border-collapse: collapse; font-size: 0.88em; margin: 0; }
  .we-table th, .we-table td { padding: 0.5rem 0.65rem; text-align: left; border-bottom: 1px solid var(--md-default-fg-color--lightest); }
  .we-table th { cursor: pointer; user-select: none; background: var(--md-default-fg-color--lightest); font-weight: 600; position: sticky; top: 0; }
  .we-table th:hover { color: var(--md-primary-fg-color); }
  .we-table th.sort-asc::after { content: " ▲"; opacity: 0.7; }
  .we-table th.sort-desc::after { content: " ▼"; opacity: 0.7; }
  .we-table tr:hover td { background: var(--md-default-fg-color--lightest); }
  .we-tier { display: inline-block; min-width: 26px; text-align: center; padding: 2px 6px; border-radius: 4px; font-weight: 700; color: white; font-size: 0.85em; }
  .we-tier-S { background: #d32f2f; }
  .we-tier-A { background: #f57c00; }
  .we-tier-B { background: #fbc02d; color: #222; }
  .we-tier-C { background: #689f38; }
  .we-tier-D { background: #5e35b1; }
  .we-tier-E { background: #455a64; }
  .we-tier-F { background: #424242; }
  .we-link { color: var(--md-primary-fg-color); text-decoration: none; font-weight: 500; }
  .we-link:hover { text-decoration: underline; }
  .we-empty { padding: 2rem; text-align: center; color: var(--md-default-fg-color--light); }
  .we-meta { font-size: 0.82em; color: var(--md-default-fg-color--light); margin: 0.25rem 0 0.75rem; }
  .we-num { font-variant-numeric: tabular-nums; }
</style>

<div id="weapon-explorer">
  <div class="we-controls">
    <div class="we-search-wrap">
      <input type="text" id="we-search" class="we-search" placeholder="🔍 무기명·스탯 검색 / Search weapons or stats…">
    </div>
    <div class="we-chip-group" id="we-class-filter">
      <span class="we-chip-label">Class:</span>
    </div>
    <div class="we-chip-group" id="we-tier-filter">
      <span class="we-chip-label">Tier:</span>
    </div>
  </div>
  <div class="we-meta" id="we-meta">로딩 중… / Loading…</div>
  <table class="we-table">
    <thead>
      <tr>
        <th data-sort="tier_order">Tier</th>
        <th data-sort="name">Weapon</th>
        <th data-sort="weapon_class">Class</th>
        <th data-sort="ar_peak" class="sort-desc">AR</th>
        <th data-sort="damage_peak">Damage</th>
        <th data-sort="weight">Weight</th>
        <th data-sort="optimal_stats">Optimal Stats</th>
      </tr>
    </thead>
    <tbody id="we-tbody"></tbody>
  </table>
  <div class="we-empty" id="we-empty" hidden>No weapons match your filters.</div>
</div>

<script>
(() => {
  const DATA_URL = "../../assets/data/weapons.json";
  const TIER_ORDER = { S: 0, A: 1, B: 2, C: 3, D: 4, E: 5, F: 6 };
  const NUMERIC_KEYS = new Set(["ar_peak", "damage_peak", "weight", "tier_order"]);
  const DEFAULT_DESC = new Set(["ar_peak", "damage_peak"]);

  let weapons = [];
  const filters = {
    search: "",
    classes: new Set(),
    tiers: new Set(),
    sortKey: "ar_peak",
    sortDir: "desc",
  };

  const $ = (id) => document.getElementById(id);

  async function init() {
    try {
      const res = await fetch(DATA_URL);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      weapons = data.weapons.map((w) => ({
        ...w,
        tier_order: TIER_ORDER[w.tier] ?? 99,
      }));
      buildChips("we-class-filter", data.weapon_classes, "classes");
      buildChips("we-tier-filter", data.tiers, "tiers");
      attachEvents();
      render();
    } catch (err) {
      $("we-meta").textContent = "데이터 로드 실패 / Failed to load data: " + err.message;
    }
  }

  function buildChips(containerId, items, key) {
    const container = $(containerId);
    items.forEach((item) => {
      const chip = document.createElement("span");
      chip.className = "we-chip";
      chip.textContent = item;
      chip.addEventListener("click", () => {
        if (filters[key].has(item)) {
          filters[key].delete(item);
          chip.classList.remove("active");
        } else {
          filters[key].add(item);
          chip.classList.add("active");
        }
        render();
      });
      container.appendChild(chip);
    });
  }

  function attachEvents() {
    $("we-search").addEventListener("input", (e) => {
      filters.search = e.target.value.toLowerCase();
      render();
    });
    document.querySelectorAll(".we-table th").forEach((th) => {
      th.addEventListener("click", () => {
        const key = th.dataset.sort;
        if (filters.sortKey === key) {
          filters.sortDir = filters.sortDir === "asc" ? "desc" : "asc";
        } else {
          filters.sortKey = key;
          filters.sortDir = DEFAULT_DESC.has(key) ? "desc" : "asc";
        }
        render();
      });
    });
  }

  function render() {
    const q = filters.search.trim();
    let result = weapons.filter((w) => {
      if (filters.classes.size && !filters.classes.has(w.weapon_class)) return false;
      if (filters.tiers.size && !filters.tiers.has(w.tier)) return false;
      if (q) {
        const hay = `${w.name} ${w.optimal_stats} ${w.extra} ${w.ar}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });

    const dir = filters.sortDir === "asc" ? 1 : -1;
    result.sort((a, b) => {
      const va = a[filters.sortKey];
      const vb = b[filters.sortKey];
      if (NUMERIC_KEYS.has(filters.sortKey)) return (va - vb) * dir;
      return String(va).localeCompare(String(vb)) * dir;
    });

    const tbody = $("we-tbody");
    tbody.innerHTML = result.map((w) => `
      <tr>
        <td><span class="we-tier we-tier-${w.tier}">${w.tier}</span></td>
        <td><a class="we-link" href="${escapeHtml(w.source_url)}">${escapeHtml(w.name)}</a></td>
        <td>${escapeHtml(w.weapon_class)}</td>
        <td>${escapeHtml(w.ar)}</td>
        <td class="we-num">${escapeHtml(w.damage_1h)}</td>
        <td class="we-num">${w.weight}</td>
        <td>${escapeHtml(w.optimal_stats)}</td>
      </tr>
    `).join("");

    document.querySelectorAll(".we-table th").forEach((th) => {
      th.classList.remove("sort-asc", "sort-desc");
      if (th.dataset.sort === filters.sortKey) {
        th.classList.add(filters.sortDir === "asc" ? "sort-asc" : "sort-desc");
      }
    });

    $("we-empty").hidden = result.length > 0;
    $("we-meta").textContent = `${result.length} / ${weapons.length} 무기 표시 중 — 컬럼 헤더 클릭으로 정렬, 칩 클릭으로 필터`;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[c]));
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
</script>

---

## 데이터 출처 / Data Sources

이 도구는 다음 가이드의 티어 표를 자동으로 추출합니다.

| Source | Original Author |
|--------|-----------------|
| [Straight Sword Guide](../guides/Straight_Sword_Guide_EN.md) | eisenwave |
| [Halberd Guide](../guides/Halberd_Guide_EN.md) | eisenwave |
| [Katana Guide](../guides/Katana_Guide_EN.md) | eisenwave |

가이드 표가 수정되면 `python tools/extract_weapons.py`를 실행해 `docs/assets/data/weapons.json`을 재생성하고, CI가 마크다운 원본과 JSON이 일치하는지 자동으로 검증합니다.
