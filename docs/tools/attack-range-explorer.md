---
title: 공격 거리 탐색기 / Attack Range Explorer
---

# 📏 공격 거리 탐색기 / Attack Range Explorer

> Elden Ring 1.12 기준 모든 무기 클래스의 공격별 도달 거리와 startup 데이터.
> **5,995개 측정값 × 41개 클래스**.
>
> Every weapon class' attack measured in-game — reach, startup, speed.
> 5,995 attacks across 41 weapon classes.
>
> **Data source: [emilia](https://docs.google.com/spreadsheets/) — Elden Ring 1.12 Attack Ranges**

<style>
  #ar-explorer { --ar-border: var(--md-default-fg-color--lightest); --ar-muted: var(--md-default-fg-color--light); }
  .ar-bar { display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; margin-bottom: 0.4rem; }
  .ar-input { flex: 1; min-width: 220px; padding: 0.5rem 0.8rem; border: 1px solid var(--ar-border); border-radius: 8px; background: var(--md-default-bg-color); color: var(--md-default-fg-color); font-size: 0.9em; }
  .ar-input:focus { outline: 2px solid var(--md-primary-fg-color); outline-offset: -1px; }
  .ar-cls-wrap { position: relative; flex: 1; min-width: 220px; }
  .ar-cls-list { position: absolute; top: calc(100% + 2px); left: 0; right: 0; background: var(--md-default-bg-color); border: 1px solid var(--ar-border); border-radius: 8px; max-height: 220px; overflow-y: auto; z-index: 10; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
  .ar-cls-item { padding: 0.4rem 0.75rem; cursor: pointer; font-size: 0.85em; }
  .ar-cls-item:hover, .ar-cls-item.focused { background: var(--md-default-fg-color--lightest); }
  .ar-cls-tags { display: flex; flex-wrap: wrap; gap: 0.3rem; margin-bottom: 0.4rem; }
  .ar-cls-tag { display: inline-flex; align-items: center; gap: 0.3rem; padding: 0.2rem 0.5rem 0.2rem 0.6rem; background: var(--md-primary-fg-color); color: white; border-radius: 12px; font-size: 0.78em; }
  .ar-cls-tag button { background: rgba(255,255,255,0.25); color: white; border: 0; border-radius: 50%; width: 16px; height: 16px; cursor: pointer; font-size: 0.9em; line-height: 1; display: inline-flex; align-items: center; justify-content: center; padding: 0; }

  .ar-chips { display: flex; flex-wrap: wrap; gap: 0.3rem; align-items: center; padding: 0.3rem 0; }
  .ar-chip-sep { display: inline-block; width: 1px; height: 1.1em; background: var(--ar-border); margin: 0 0.3rem; }
  .ar-chip { display: inline-flex; align-items: center; padding: 0.22rem 0.6rem; border: 1px solid var(--ar-border); border-radius: 12px; cursor: pointer; user-select: none; font-size: 0.78em; transition: all 0.12s; white-space: nowrap; color: var(--ar-muted); }
  .ar-chip:hover { border-color: var(--md-primary-fg-color); color: var(--md-default-fg-color); }
  .ar-chip.active { background: var(--md-primary-fg-color); color: white; border-color: var(--md-primary-fg-color); }

  .ar-meta { font-size: 0.78em; color: var(--ar-muted); margin: 0.5rem 0; }

  .ar-table-wrap { border: 1px solid var(--ar-border); border-radius: 8px; overflow: hidden; }
  .ar-table-scroll { max-height: 72vh; overflow-y: auto; overflow-x: auto; }
  .ar-table { width: 100%; border-collapse: collapse; font-size: 0.86em; }
  .ar-table th, .ar-table td { padding: 0.55rem 0.9rem; text-align: left; border-bottom: 1px solid var(--ar-border); vertical-align: top; }
  .ar-table th { cursor: pointer; user-select: none; background: var(--md-default-bg-color); font-weight: 600; position: sticky; top: 0; z-index: 1; box-shadow: 0 1px 0 var(--ar-border); white-space: nowrap; font-size: 0.78em; text-transform: uppercase; letter-spacing: 0.04em; color: var(--ar-muted); }
  .ar-table th:hover { color: var(--md-primary-fg-color); }
  .ar-table th.sort-asc::after { content: " ↑"; }
  .ar-table th.sort-desc::after { content: " ↓"; }
  .ar-table tbody tr { transition: background 0.1s; }
  .ar-table tbody tr:hover td { background: var(--md-default-fg-color--lightest); }
  .ar-table tbody tr.low-sample td { opacity: 0.55; }
  .ar-table tbody tr:last-child td { border-bottom: 0; }

  /* Attack cell — three-tier hierarchy */
  .ar-setup { font-weight: 500; color: var(--md-default-fg-color); line-height: 1.3; }
  .ar-attack { font-size: 0.85em; color: var(--md-default-fg-color); margin-top: 1px; }
  .ar-class { font-size: 0.78em; color: var(--ar-muted); margin-top: 2px; display: flex; align-items: center; gap: 0.4rem; }
  .ar-hand { display: inline-block; padding: 0 5px; border: 1px solid var(--ar-border); border-radius: 4px; font-size: 0.92em; color: var(--ar-muted); font-variant-numeric: tabular-nums; }

  /* Numeric cells — main value + secondary stacked */
  .ar-primary { font-variant-numeric: tabular-nums; font-weight: 500; color: var(--md-default-fg-color); }
  .ar-secondary { font-size: 0.78em; font-variant-numeric: tabular-nums; color: var(--ar-muted); margin-top: 1px; }
  .ar-num-th { text-align: right !important; }
  .ar-num-td { text-align: right; }

  .ar-null { color: var(--ar-muted); font-style: italic; opacity: 0.6; }
  .ar-empty { padding: 2.5rem 1rem; text-align: center; color: var(--ar-muted); }
</style>

<div id="ar-explorer">
  <div class="ar-bar">
    <input type="text" id="ar-q" class="ar-input" placeholder="🔍 무기명·공격명 검색 / Search setup or attack…">
    <div class="ar-cls-wrap">
      <input type="text" id="ar-cls-q" class="ar-input" placeholder="무기 클래스 필터 (예: halberd, katana)" autocomplete="off">
      <div class="ar-cls-list" id="ar-cls-list" hidden></div>
    </div>
  </div>
  <div class="ar-cls-tags" id="ar-cls-tags"></div>
  <div class="ar-chips" id="ar-filters"></div>
  <div class="ar-meta" id="ar-meta">로딩 중… / Loading…</div>
  <div class="ar-table-wrap">
    <div class="ar-table-scroll">
      <table class="ar-table">
        <thead>
          <tr>
            <th data-sort="setup">Attack</th>
            <th data-sort="avg_m" class="ar-num-th sort-desc">Reach (m)</th>
            <th data-sort="startup_ms" class="ar-num-th">Startup</th>
            <th data-sort="speed_mps" class="ar-num-th">Speed (m/s)</th>
            <th data-sort="sample_size" class="ar-num-th">Samples</th>
          </tr>
        </thead>
        <tbody id="ar-rows"></tbody>
      </table>
    </div>
  </div>
  <div class="ar-empty" id="ar-empty" hidden>일치하는 공격이 없어요. / No attacks match your filters.</div>
</div>

<script>
(() => {
  const DATA_URL = "../../assets/data/attack_ranges.json";
  const NUMERIC_KEYS = new Set(["avg_m", "min_m", "max_m", "startup_ms", "startup_frames", "speed_mps", "sample_size"]);
  const DEFAULT_DESC = new Set(["avg_m", "min_m", "max_m", "speed_mps", "sample_size"]);
  const MAX_ROWS = 250;
  const LOW_SAMPLE = 10;

  let attacks = [];
  let allClasses = [];
  let allCategories = [];
  let allHands = [];
  const state = {
    q: "",
    classes: new Set(),
    categories: new Set(),
    hands: new Set(),
    classQuery: "",
    classFocus: -1,
    sortKey: "avg_m",
    sortDir: "desc",
  };

  const $ = (id) => document.getElementById(id);

  async function init() {
    try {
      const res = await fetch(DATA_URL);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      attacks = data.attacks.map((a) => ({
        ...a,
        searchKey: `${a.setup} ${a.attack} ${a.weapon_class}`.toLowerCase(),
      }));
      allClasses = data.weapon_classes;
      allCategories = data.categories;
      allHands = data.hands.filter((h) => h !== "other");
      renderFilterChips();
      attachEvents();
      render();
    } catch (err) {
      $("ar-meta").textContent = "데이터 로드 실패 / Failed to load: " + err.message;
    }
  }

  function renderFilterChips() {
    const bar = $("ar-filters");
    bar.innerHTML = "";
    // Hand chips
    allHands.forEach((h) => {
      const chip = makeChip(h, () => toggleSet(state.hands, h));
      if (state.hands.has(h)) chip.classList.add("active");
      bar.appendChild(chip);
    });
    bar.appendChild(sep());
    // Category chips
    allCategories.forEach((c) => {
      const chip = makeChip(c, () => toggleSet(state.categories, c));
      if (state.categories.has(c)) chip.classList.add("active");
      bar.appendChild(chip);
    });
  }

  function makeChip(label, onclick) {
    const el = document.createElement("span");
    el.className = "ar-chip";
    el.textContent = label;
    el.addEventListener("click", () => { onclick(); renderFilterChips(); render(); });
    return el;
  }
  function sep() {
    const s = document.createElement("span");
    s.className = "ar-chip-sep";
    return s;
  }
  function toggleSet(set, v) { if (set.has(v)) set.delete(v); else set.add(v); }

  function renderClassTags() {
    const c = $("ar-cls-tags");
    c.innerHTML = "";
    state.classes.forEach((cls) => {
      const tag = document.createElement("span");
      tag.className = "ar-cls-tag";
      tag.innerHTML = `${esc(cls)} <button type="button" aria-label="remove">×</button>`;
      tag.querySelector("button").addEventListener("click", () => {
        state.classes.delete(cls);
        renderClassTags();
        render();
      });
      c.appendChild(tag);
    });
  }

  function renderClassSuggestions() {
    const list = $("ar-cls-list");
    const q = state.classQuery.trim().toLowerCase();
    if (!q) { list.hidden = true; return; }
    const matches = allClasses
      .filter((cls) => cls.toLowerCase().includes(q) && !state.classes.has(cls))
      .slice(0, 12);
    if (matches.length === 0) { list.hidden = true; return; }
    list.innerHTML = matches.map((cls, i) =>
      `<div class="ar-cls-item${i === state.classFocus ? " focused" : ""}" data-cls="${esc(cls)}">${esc(cls)}</div>`
    ).join("");
    list.hidden = false;
    list.querySelectorAll(".ar-cls-item").forEach((el) => {
      el.addEventListener("mousedown", (e) => {
        e.preventDefault();
        selectClass(el.dataset.cls);
      });
    });
  }

  function selectClass(cls) {
    state.classes.add(cls);
    state.classQuery = "";
    state.classFocus = -1;
    $("ar-cls-q").value = "";
    $("ar-cls-list").hidden = true;
    renderClassTags();
    render();
  }

  function attachEvents() {
    $("ar-q").addEventListener("input", (e) => {
      state.q = e.target.value.toLowerCase();
      render();
    });
    const cq = $("ar-cls-q");
    cq.addEventListener("input", (e) => {
      state.classQuery = e.target.value;
      state.classFocus = -1;
      renderClassSuggestions();
    });
    cq.addEventListener("keydown", (e) => {
      const list = $("ar-cls-list");
      const items = list.querySelectorAll(".ar-cls-item");
      if (e.key === "ArrowDown") {
        e.preventDefault();
        state.classFocus = Math.min(items.length - 1, state.classFocus + 1);
        renderClassSuggestions();
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        state.classFocus = Math.max(0, state.classFocus - 1);
        renderClassSuggestions();
      } else if (e.key === "Enter") {
        e.preventDefault();
        const pick = items[state.classFocus] || items[0];
        if (pick) selectClass(pick.dataset.cls);
      } else if (e.key === "Escape") {
        list.hidden = true;
      }
    });
    cq.addEventListener("blur", () => {
      setTimeout(() => $("ar-cls-list").hidden = true, 150);
    });
    document.querySelectorAll(".ar-table th").forEach((th) => {
      th.addEventListener("click", () => {
        const key = th.dataset.sort;
        if (state.sortKey === key) {
          state.sortDir = state.sortDir === "asc" ? "desc" : "asc";
        } else {
          state.sortKey = key;
          state.sortDir = DEFAULT_DESC.has(key) ? "desc" : "asc";
        }
        render();
      });
    });
  }

  function render() {
    const q = state.q.trim();
    let result = attacks.filter((a) => {
      if (state.classes.size && !state.classes.has(a.weapon_class)) return false;
      if (state.categories.size && !state.categories.has(a.category)) return false;
      if (state.hands.size && !state.hands.has(a.hand)) return false;
      if (q && !a.searchKey.includes(q)) return false;
      return true;
    });

    const dir = state.sortDir === "asc" ? 1 : -1;
    const key = state.sortKey;
    const isNum = NUMERIC_KEYS.has(key);
    result.sort((a, b) => {
      const va = a[key], vb = b[key];
      if (va == null && vb == null) return 0;
      if (va == null) return 1;
      if (vb == null) return -1;
      if (isNum) return (va - vb) * dir;
      return String(va).localeCompare(String(vb)) * dir;
    });

    const total = result.length;
    const sliced = result.slice(0, MAX_ROWS);
    const rows = $("ar-rows");
    rows.innerHTML = sliced.map((a) => {
      const isLow = a.sample_size != null && a.sample_size < LOW_SAMPLE;
      const range = a.min_m != null && a.max_m != null && (a.max_m - a.min_m) > 0.01
        ? `${a.min_m.toFixed(2)}–${a.max_m.toFixed(2)}` : "";
      const startupMs = a.startup_ms != null ? `${a.startup_ms} ms` : '<span class="ar-null">—</span>';
      const startupFrames = a.startup_frames != null ? `${a.startup_frames}f @ 30fps` : "";
      const speed = a.speed_mps != null ? a.speed_mps.toFixed(2) : '<span class="ar-null">—</span>';
      const handBadge = a.hand !== "other" ? `<span class="ar-hand">${esc(a.hand)}</span>` : "";

      return `
        <tr${isLow ? ' class="low-sample"' : ""}>
          <td>
            <div class="ar-setup">${esc(a.setup)}</div>
            <div class="ar-attack">${esc(a.attack)}</div>
            <div class="ar-class">${handBadge}<span>${esc(a.weapon_class)}</span></div>
          </td>
          <td class="ar-num-td">
            <div class="ar-primary">${a.avg_m.toFixed(2)}</div>
            ${range ? `<div class="ar-secondary">${range}</div>` : ""}
          </td>
          <td class="ar-num-td">
            <div class="ar-primary">${startupMs}</div>
            ${startupFrames ? `<div class="ar-secondary">${startupFrames}</div>` : ""}
          </td>
          <td class="ar-num-td"><div class="ar-primary">${speed}</div></td>
          <td class="ar-num-td"><div class="ar-secondary">n=${a.sample_size}</div></td>
        </tr>`;
    }).join("");

    document.querySelectorAll(".ar-table th").forEach((th) => {
      th.classList.remove("sort-asc", "sort-desc");
      if (th.dataset.sort === key) th.classList.add(state.sortDir === "asc" ? "sort-asc" : "sort-desc");
    });

    $("ar-empty").hidden = total > 0;
    const truncated = total > MAX_ROWS ? ` · 상위 ${MAX_ROWS}개 표시` : "";
    $("ar-meta").textContent = `${total.toLocaleString()} / ${attacks.length.toLocaleString()} matches${truncated}`;
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

모든 측정값은 **emilia**의 *Elden Ring 1.12 Attack Ranges* 데이터셋에서 가져왔어요.
게임 내에서 직접 캡처한 root motion + attack extension 측정값입니다.

All measurements come from **emilia**'s *Elden Ring 1.12 Attack Ranges* dataset —
in-game captures of root motion + attack extension distance for every weapon class.

| Field | Meaning |
|-------|---------|
| **Reach (m)** | 평균 공격 도달 거리 / Avg reach distance. 작게 표시된 값은 측정 샘플의 min–max 범위. |
| **Startup** | 시작 모션 길이 / Animation startup. ms와 30fps 프레임 환산값. |
| **Speed (m/s)** | active hit까지의 평균 속도 / Average speed to active. |
| **Samples** | 측정 샘플 수. **n<10인 행은 반투명으로 표시** — 신뢰도가 낮을 수 있음. |

데이터가 갱신되면 `python tools/extract_attack_ranges.py`를 실행해 JSON을 재생성하고, CI가 CSV와 일치하는지 검증합니다.
