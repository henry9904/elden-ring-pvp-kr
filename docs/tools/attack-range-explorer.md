---
title: 공격 거리 탐색기 / Attack Range Explorer
---

# 📏 공격 거리 탐색기 / Attack Range Explorer

> Elden Ring 1.12 기준 모든 무기 클래스의 공격별 거리·startup·속도 데이터를
> 검색·필터·정렬할 수 있어요. **5,995개의 측정값**이 들어있어요.
>
> Cross-weapon attack-range database — every R1/R2/Charged/Running/Rolling
> animation measured in-game (avg/min/max distance, startup ms & frames,
> speed-to-active). 5,995 attacks across 41 weapon classes.
>
> **Data source: [emilia](https://docs.google.com/spreadsheets/) (Elden Ring 1.12 Attack Ranges)**

<style>
  .ar-controls { display: flex; flex-direction: column; gap: 0.6rem; margin-bottom: 1rem; }
  .ar-row { display: flex; flex-wrap: wrap; gap: 0.6rem; align-items: center; }
  .ar-search { flex: 1; min-width: 240px; padding: 0.55rem 0.85rem; border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px; background: var(--md-default-bg-color); color: var(--md-default-fg-color); font-size: 0.9em; }
  .ar-search:focus { outline: 2px solid var(--md-primary-fg-color); outline-offset: -1px; }
  .ar-chip-group { display: flex; gap: 0.35rem; flex-wrap: wrap; align-items: center; }
  .ar-chip-label { font-size: 0.78em; color: var(--md-default-fg-color--light); margin-right: 0.2rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
  .ar-chip { display: inline-flex; align-items: center; padding: 0.25rem 0.65rem; border: 1px solid var(--md-default-fg-color--lightest); border-radius: 14px; cursor: pointer; user-select: none; font-size: 0.78em; transition: all 0.12s; white-space: nowrap; }
  .ar-chip:hover { border-color: var(--md-primary-fg-color); }
  .ar-chip.active { background: var(--md-primary-fg-color); color: white; border-color: var(--md-primary-fg-color); }
  .ar-chip.clear { font-style: italic; color: var(--md-default-fg-color--light); }
  .ar-table-wrap { overflow-x: auto; max-height: 70vh; border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px; }
  .ar-table { width: 100%; border-collapse: collapse; font-size: 0.82em; margin: 0; }
  .ar-table th, .ar-table td { padding: 0.4rem 0.6rem; text-align: left; border-bottom: 1px solid var(--md-default-fg-color--lightest); white-space: nowrap; }
  .ar-table th { cursor: pointer; user-select: none; background: var(--md-default-bg-color); font-weight: 600; position: sticky; top: 0; z-index: 1; box-shadow: 0 1px 0 var(--md-default-fg-color--lightest); }
  .ar-table th:hover { color: var(--md-primary-fg-color); }
  .ar-table th.sort-asc::after { content: " ▲"; opacity: 0.7; }
  .ar-table th.sort-desc::after { content: " ▼"; opacity: 0.7; }
  .ar-table tr:hover td { background: var(--md-default-fg-color--lightest); }
  .ar-num { font-variant-numeric: tabular-nums; text-align: right; }
  .ar-null { color: var(--md-default-fg-color--lighter); font-style: italic; }
  .ar-empty { padding: 2rem; text-align: center; color: var(--md-default-fg-color--light); }
  .ar-meta { font-size: 0.82em; color: var(--md-default-fg-color--light); margin: 0.25rem 0 0.5rem; }
  .ar-pill { display: inline-block; padding: 1px 7px; border-radius: 10px; font-size: 0.78em; font-weight: 500; border: 1px solid var(--md-default-fg-color--lightest); }
  .ar-pill-1h { background: rgba(103, 58, 183, 0.12); color: #9c78d6; border-color: rgba(103, 58, 183, 0.3); }
  .ar-pill-2h { background: rgba(244, 67, 54, 0.12); color: #ef7066; border-color: rgba(244, 67, 54, 0.3); }
  .ar-pill-paired { background: rgba(255, 152, 0, 0.12); color: #ffa726; border-color: rgba(255, 152, 0, 0.3); }
  .ar-pill-other { background: rgba(96, 125, 139, 0.12); color: #90a4ae; border-color: rgba(96, 125, 139, 0.3); }
  [data-md-color-scheme="default"] .ar-pill-1h { color: #5e35b1; }
  [data-md-color-scheme="default"] .ar-pill-2h { color: #c62828; }
  [data-md-color-scheme="default"] .ar-pill-paired { color: #e65100; }
  [data-md-color-scheme="default"] .ar-pill-other { color: #455a64; }
</style>

<div id="attack-range-explorer">
  <div class="ar-controls">
    <div class="ar-row">
      <input type="text" id="ar-search" class="ar-search" placeholder="🔍 무기명·공격명 검색 / Search setup or attack…">
    </div>
    <div class="ar-row">
      <div class="ar-chip-group" id="ar-hand-filter">
        <span class="ar-chip-label">Hand</span>
      </div>
    </div>
    <div class="ar-row">
      <div class="ar-chip-group" id="ar-category-filter">
        <span class="ar-chip-label">Attack</span>
      </div>
    </div>
    <div class="ar-row">
      <div class="ar-chip-group" id="ar-class-filter">
        <span class="ar-chip-label">Class</span>
      </div>
    </div>
  </div>
  <div class="ar-meta" id="ar-meta">로딩 중… / Loading…</div>
  <div class="ar-table-wrap">
    <table class="ar-table">
      <thead>
        <tr>
          <th data-sort="setup">Setup</th>
          <th data-sort="weapon_class">Class</th>
          <th data-sort="attack">Attack</th>
          <th data-sort="hand">Hand</th>
          <th data-sort="avg_m" class="sort-desc">Avg (m)</th>
          <th data-sort="min_m">Min (m)</th>
          <th data-sort="max_m">Max (m)</th>
          <th data-sort="startup_ms">Startup (ms)</th>
          <th data-sort="startup_frames">Frames</th>
          <th data-sort="speed_mps">Speed (m/s)</th>
          <th data-sort="sample_size">N</th>
        </tr>
      </thead>
      <tbody id="ar-tbody"></tbody>
    </table>
  </div>
  <div class="ar-empty" id="ar-empty" hidden>No attacks match your filters.</div>
</div>

<script>
(() => {
  const DATA_URL = "../../assets/data/attack_ranges.json";
  const NUMERIC_KEYS = new Set(["avg_m", "min_m", "max_m", "startup_ms", "startup_frames", "speed_mps", "sample_size", "root_motion_m", "extension_m", "sd"]);
  const DEFAULT_DESC = new Set(["avg_m", "min_m", "max_m", "speed_mps", "sample_size"]);
  const MAX_ROWS = 300;

  let attacks = [];
  const filters = {
    search: "",
    classes: new Set(),
    categories: new Set(),
    hands: new Set(),
    sortKey: "avg_m",
    sortDir: "desc",
  };

  const $ = (id) => document.getElementById(id);

  async function init() {
    try {
      const res = await fetch(DATA_URL);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      attacks = data.attacks;
      buildChips("ar-hand-filter", data.hands, "hands");
      buildChips("ar-category-filter", data.categories, "categories");
      buildChips("ar-class-filter", data.weapon_classes, "classes");
      attachEvents();
      render();
    } catch (err) {
      $("ar-meta").textContent = "데이터 로드 실패 / Failed to load data: " + err.message;
    }
  }

  function buildChips(containerId, items, key) {
    const container = $(containerId);
    items.forEach((item) => {
      const chip = document.createElement("span");
      chip.className = "ar-chip";
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
    $("ar-search").addEventListener("input", (e) => {
      filters.search = e.target.value.toLowerCase();
      render();
    });
    document.querySelectorAll(".ar-table th").forEach((th) => {
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
    let result = attacks.filter((a) => {
      if (filters.classes.size && !filters.classes.has(a.weapon_class)) return false;
      if (filters.categories.size && !filters.categories.has(a.category)) return false;
      if (filters.hands.size && !filters.hands.has(a.hand)) return false;
      if (q) {
        const hay = `${a.setup} ${a.attack} ${a.weapon_class}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });

    const dir = filters.sortDir === "asc" ? 1 : -1;
    const key = filters.sortKey;
    const isNum = NUMERIC_KEYS.has(key);
    result.sort((a, b) => {
      const va = a[key];
      const vb = b[key];
      if (va == null && vb == null) return 0;
      if (va == null) return 1;
      if (vb == null) return -1;
      if (isNum) return (va - vb) * dir;
      return String(va).localeCompare(String(vb)) * dir;
    });

    const total = result.length;
    const sliced = result.slice(0, MAX_ROWS);
    const tbody = $("ar-tbody");
    tbody.innerHTML = sliced.map((a) => `
      <tr>
        <td>${esc(a.setup)}</td>
        <td>${esc(a.weapon_class)}</td>
        <td>${esc(a.attack)}</td>
        <td><span class="ar-pill ar-pill-${a.hand}">${esc(a.hand)}</span></td>
        <td class="ar-num">${num(a.avg_m, 3)}</td>
        <td class="ar-num">${num(a.min_m, 3)}</td>
        <td class="ar-num">${num(a.max_m, 3)}</td>
        <td class="ar-num">${num(a.startup_ms, 0)}</td>
        <td class="ar-num">${num(a.startup_frames, 0)}</td>
        <td class="ar-num">${num(a.speed_mps, 2)}</td>
        <td class="ar-num">${num(a.sample_size, 0)}</td>
      </tr>
    `).join("");

    document.querySelectorAll(".ar-table th").forEach((th) => {
      th.classList.remove("sort-asc", "sort-desc");
      if (th.dataset.sort === key) {
        th.classList.add(filters.sortDir === "asc" ? "sort-asc" : "sort-desc");
      }
    });

    $("ar-empty").hidden = total > 0;
    const shown = sliced.length;
    const truncated = total > MAX_ROWS ? ` (상위 ${MAX_ROWS}개 표시 / showing top ${MAX_ROWS})` : "";
    $("ar-meta").textContent = `${shown.toLocaleString()} / ${total.toLocaleString()} of ${attacks.length.toLocaleString()} 공격${truncated} — 컬럼 헤더 클릭으로 정렬`;
  }

  function num(v, digits) {
    if (v == null) return '<span class="ar-null">—</span>';
    return Number(v).toFixed(digits);
  }

  function esc(s) {
    return String(s ?? "").replace(/[&<>"']/g, (c) => ({
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

## 데이터 출처 / Data Source

이 도구의 모든 측정값은 **emilia**의 *Elden Ring 1.12 Attack Ranges* 데이터셋에서
가져왔어요. 게임 내에서 직접 캡처한 root motion + attack extension 측정값입니다.

All measurements come from **emilia**'s *Elden Ring 1.12 Attack Ranges* dataset —
in-game captures of root motion + attack extension distance for every weapon class.

| Field | Meaning |
|-------|---------|
| **Avg (m)** | 평균 공격 도달 거리 / Average reach distance |
| **Min / Max (m)** | 샘플 내 최소·최대값 / Sample min/max |
| **Startup (ms / frames)** | 시작 모션 길이 / Animation startup duration (30 fps) |
| **Speed (m/s)** | active hit까지의 평균 속도 / Average speed to active |
| **N** | 측정 샘플 수 / Sample size |

데이터가 갱신되면 `python tools/extract_attack_ranges.py`를 실행해 JSON을 재생성하고, CI가 CSV와 일치하는지 검증합니다.

When the source CSV is updated, run `python tools/extract_attack_ranges.py` to
regenerate the JSON. CI verifies the JSON is in sync with the CSV.
