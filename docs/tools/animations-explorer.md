---
title: 애니메이션 / 프레임 데이터 탐색기 / Animations Explorer
---

# 🎯 애니메이션 / 프레임 데이터 탐색기 / Animations Explorer

> 모든 무기 + Ash of War 애니메이션의 동작 속성 — 하이퍼아머·패리·멀티히트 등 — 을 한눈에.
> **7,874개 애니메이션 × 334개 클래스**.
>
> Behavioral flags for every weapon and AoW animation in Elden Ring 1.12.
> Find out exactly which attacks have hyperarmor, can be parried, or share
> an animation across weapons.
>
> **Data source: [emilia](https://er-frame-data.nyasu.business/) — Elden Ring Frame Data Explorer**

<style>
  /* === Layout === */
  #anim-explorer { --an-border: var(--md-default-fg-color--lightest); --an-muted: var(--md-default-fg-color--light); }
  .an-bar { display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; margin-bottom: 0.4rem; }
  .an-input { flex: 1; min-width: 220px; padding: 0.5rem 0.8rem; border: 1px solid var(--an-border); border-radius: 8px; background: var(--md-default-bg-color); color: var(--md-default-fg-color); font-size: 0.9em; }
  .an-input:focus { outline: 2px solid var(--md-primary-fg-color); outline-offset: -1px; }
  .an-cls-wrap { position: relative; flex: 1; min-width: 220px; }
  .an-cls-list { position: absolute; top: calc(100% + 2px); left: 0; right: 0; background: var(--md-default-bg-color); border: 1px solid var(--an-border); border-radius: 8px; max-height: 220px; overflow-y: auto; z-index: 10; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
  .an-cls-item { padding: 0.4rem 0.75rem; cursor: pointer; font-size: 0.85em; }
  .an-cls-item:hover, .an-cls-item.focused { background: var(--md-default-fg-color--lightest); }
  .an-cls-tags { display: flex; flex-wrap: wrap; gap: 0.3rem; margin-bottom: 0.4rem; }
  .an-cls-tag { display: inline-flex; align-items: center; gap: 0.3rem; padding: 0.2rem 0.5rem 0.2rem 0.6rem; background: var(--md-primary-fg-color); color: white; border-radius: 12px; font-size: 0.78em; }
  .an-cls-tag button { background: rgba(255,255,255,0.25); color: white; border: 0; border-radius: 50%; width: 16px; height: 16px; cursor: pointer; font-size: 0.9em; line-height: 1; display: inline-flex; align-items: center; justify-content: center; padding: 0; }

  /* === Flag chips === */
  .an-flags-bar { display: flex; flex-wrap: wrap; gap: 0.3rem; align-items: center; padding: 0.4rem 0; }
  .an-fchip { display: inline-flex; align-items: center; padding: 0.22rem 0.6rem; border: 1px solid var(--an-border); border-radius: 12px; cursor: pointer; user-select: none; font-size: 0.78em; transition: all 0.12s; white-space: nowrap; color: var(--an-muted); }
  .an-fchip:hover { border-color: var(--md-primary-fg-color); color: var(--md-default-fg-color); }
  .an-fchip.active { background: var(--md-primary-fg-color); color: white; border-color: var(--md-primary-fg-color); }
  .an-more { font-size: 0.78em; color: var(--md-primary-fg-color); cursor: pointer; padding: 0.22rem 0.4rem; }
  .an-more:hover { text-decoration: underline; }

  /* === Meta === */
  .an-meta { font-size: 0.78em; color: var(--an-muted); margin: 0.5rem 0; }

  /* === Table === */
  .an-table-wrap { border: 1px solid var(--an-border); border-radius: 8px; overflow: hidden; }
  .an-table-scroll { max-height: 70vh; overflow-y: auto; overflow-x: auto; }
  .an-table { width: 100%; border-collapse: collapse; font-size: 0.86em; }
  .an-table th, .an-table td { padding: 0.55rem 0.9rem; text-align: left; border-bottom: 1px solid var(--an-border); vertical-align: top; }
  .an-table th { cursor: pointer; user-select: none; background: var(--md-default-bg-color); font-weight: 600; position: sticky; top: 0; z-index: 1; box-shadow: 0 1px 0 var(--an-border); white-space: nowrap; font-size: 0.8em; text-transform: uppercase; letter-spacing: 0.04em; color: var(--an-muted); }
  .an-table th:hover { color: var(--md-primary-fg-color); }
  .an-table th.sort-asc::after { content: " ↑"; }
  .an-table th.sort-desc::after { content: " ↓"; }
  .an-table tbody tr { transition: background 0.1s; }
  .an-table tbody tr:hover td { background: var(--md-default-fg-color--lightest); }
  .an-table tbody tr:last-child td { border-bottom: 0; }

  /* === Animation cell === */
  .an-name { font-weight: 500; color: var(--md-default-fg-color); line-height: 1.3; }
  .an-class { font-size: 0.84em; color: var(--an-muted); margin-top: 2px; }

  /* === Property pills — minimal, only colored for the few that matter === */
  .an-props { display: flex; flex-wrap: wrap; gap: 0.3rem; }
  .an-prop { display: inline-block; padding: 1px 6px; border-radius: 8px; font-size: 0.72em; font-weight: 500; border: 1px solid var(--an-border); color: var(--an-muted); white-space: nowrap; }
  .an-prop.hyper { background: rgba(229, 57, 53, 0.14); color: #ef9a9a; border-color: rgba(229, 57, 53, 0.45); font-weight: 600; }
  .an-prop.parriable { background: rgba(33, 150, 243, 0.1); color: #64b5f6; border-color: rgba(33, 150, 243, 0.35); }
  .an-prop.multi { background: rgba(156, 39, 176, 0.1); color: #ce93d8; border-color: rgba(156, 39, 176, 0.35); }
  .an-prop.skill { background: rgba(255, 193, 7, 0.1); color: #ffd54f; border-color: rgba(255, 193, 7, 0.4); }
  [data-md-color-scheme="default"] .an-prop.hyper { color: #c62828; }
  [data-md-color-scheme="default"] .an-prop.parriable { color: #1565c0; }
  [data-md-color-scheme="default"] .an-prop.multi { color: #6a1b9a; }
  [data-md-color-scheme="default"] .an-prop.skill { color: #b26a00; }

  /* === Weapon count === */
  .an-wcount { font-variant-numeric: tabular-nums; color: var(--an-muted); cursor: pointer; user-select: none; }
  .an-wcount:hover { color: var(--md-primary-fg-color); }
  .an-wlist { margin-top: 0.4rem; font-size: 0.84em; color: var(--md-default-fg-color); line-height: 1.5; }

  /* === States === */
  .an-empty { padding: 2.5rem 1rem; text-align: center; color: var(--an-muted); }
  .an-dim { opacity: 0.5; font-style: italic; }
</style>

<div id="anim-explorer">
  <div class="an-bar">
    <input type="text" id="an-q" class="an-input" placeholder="🔍 애니메이션·무기명 검색 / Search by name or weapon…">
    <div class="an-cls-wrap">
      <input type="text" id="an-cls-q" class="an-input" placeholder="무기 클래스 / AoW 필터 (예: dagger)" autocomplete="off">
      <div class="an-cls-list" id="an-cls-list" hidden></div>
    </div>
  </div>
  <div class="an-cls-tags" id="an-cls-tags"></div>
  <div class="an-flags-bar" id="an-flags"></div>
  <div class="an-meta" id="an-meta">로딩 중… / Loading…</div>
  <div class="an-table-wrap">
    <div class="an-table-scroll">
      <table class="an-table">
        <thead>
          <tr>
            <th data-sort="name">Animation</th>
            <th data-sort="propcount">Properties</th>
            <th data-sort="weapon_count">Weapons</th>
          </tr>
        </thead>
        <tbody id="an-rows"></tbody>
      </table>
    </div>
  </div>
  <div class="an-empty" id="an-empty" hidden>일치하는 애니메이션이 없어요. / No animations match your filters.</div>
</div>

<script>
(() => {
  const DATA_URL = "../../assets/data/animations.json";
  // The flags worth surfacing by default. "Attack" is on 60% of rows
  // (it just means "this is an attack") so showing it is pure noise.
  const PRIMARY_FLAGS = [
    "HyperArmour", "Parriable", "Multihit", "WeaponSkill",
    "HasSpeedGradient", "Casting", "Guard", "Dodge",
  ];
  // Flags that should never appear as a row pill (too common / too noisy).
  const HIDDEN_AS_PILL = new Set(["Attack"]);
  // Visual emphasis classes for the few flags that truly matter at a glance.
  const PROP_CLASS = {
    HyperArmour: "hyper",
    Parriable: "parriable",
    Multihit: "multi",
    WeaponSkill: "skill",
  };
  const MAX_ROWS = 200;
  const NUMERIC_KEYS = new Set(["propcount", "weapon_count"]);
  const DEFAULT_DESC = new Set(["propcount", "weapon_count"]);

  let animations = [];
  let allClasses = [];
  let allFlags = [];
  let moreOpen = false;
  const expanded = new Set();
  const state = {
    q: "",
    classes: new Set(),
    flags: new Set(),
    classQuery: "",
    classFocus: -1,
    sortKey: "name",
    sortDir: "asc",
  };

  const $ = (id) => document.getElementById(id);

  async function init() {
    try {
      const res = await fetch(DATA_URL);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      animations = data.animations.map((a, i) => ({
        ...a,
        idx: i,
        propcount: a.flags.filter((f) => !HIDDEN_AS_PILL.has(f)).length,
        weapon_count: a.weapons.length,
        searchKey: `${a.name} ${a.id} ${a.class} ${a.weapons.join(" ")}`.toLowerCase(),
      }));
      allClasses = data.weapon_classes;
      allFlags = data.flags;
      renderFlagBar();
      attachEvents();
      render();
    } catch (err) {
      $("an-meta").textContent = "데이터 로드 실패 / Failed to load: " + err.message;
    }
  }

  function renderFlagBar() {
    const bar = $("an-flags");
    const visible = moreOpen ? allFlags : allFlags.filter((f) => PRIMARY_FLAGS.includes(f));
    bar.innerHTML = "";
    visible.forEach((f) => {
      const chip = document.createElement("span");
      chip.className = "an-fchip" + (state.flags.has(f) ? " active" : "");
      chip.textContent = f;
      chip.addEventListener("click", () => toggleFlag(f));
      bar.appendChild(chip);
    });
    const more = document.createElement("span");
    more.className = "an-more";
    more.textContent = moreOpen ? "− 기본만 / less" : `+ 전체 ${allFlags.length}개 / all flags`;
    more.addEventListener("click", () => { moreOpen = !moreOpen; renderFlagBar(); });
    bar.appendChild(more);
  }

  function toggleFlag(f) {
    if (state.flags.has(f)) state.flags.delete(f); else state.flags.add(f);
    renderFlagBar();
    render();
  }

  function renderClassTags() {
    const c = $("an-cls-tags");
    c.innerHTML = "";
    state.classes.forEach((cls) => {
      const tag = document.createElement("span");
      tag.className = "an-cls-tag";
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
    const list = $("an-cls-list");
    const q = state.classQuery.trim().toLowerCase();
    if (!q) { list.hidden = true; return; }
    const matches = allClasses
      .filter((cls) => cls.toLowerCase().includes(q) && !state.classes.has(cls))
      .slice(0, 12);
    if (matches.length === 0) { list.hidden = true; return; }
    list.innerHTML = matches.map((cls, i) =>
      `<div class="an-cls-item${i === state.classFocus ? " focused" : ""}" data-cls="${esc(cls)}">${esc(cls)}</div>`
    ).join("");
    list.hidden = false;
    list.querySelectorAll(".an-cls-item").forEach((el) => {
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
    $("an-cls-q").value = "";
    $("an-cls-list").hidden = true;
    renderClassTags();
    render();
  }

  function attachEvents() {
    $("an-q").addEventListener("input", (e) => {
      state.q = e.target.value.toLowerCase();
      render();
    });
    const cq = $("an-cls-q");
    cq.addEventListener("input", (e) => {
      state.classQuery = e.target.value;
      state.classFocus = -1;
      renderClassSuggestions();
    });
    cq.addEventListener("keydown", (e) => {
      const list = $("an-cls-list");
      const items = list.querySelectorAll(".an-cls-item");
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
      setTimeout(() => $("an-cls-list").hidden = true, 150);
    });
    document.querySelectorAll(".an-table th").forEach((th) => {
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

  function matchFlags(a) {
    if (state.flags.size === 0) return true;
    for (const f of state.flags) if (!a.flags.includes(f)) return false;
    return true;
  }

  function render() {
    const q = state.q.trim();
    let result = animations.filter((a) => {
      if (state.classes.size && !state.classes.has(a.class)) return false;
      if (!matchFlags(a)) return false;
      if (q && !a.searchKey.includes(q)) return false;
      return true;
    });

    const dir = state.sortDir === "asc" ? 1 : -1;
    const key = state.sortKey;
    const isNum = NUMERIC_KEYS.has(key);
    result.sort((a, b) => {
      const va = a[key], vb = b[key];
      if (isNum) return (va - vb) * dir;
      return String(va).localeCompare(String(vb)) * dir;
    });

    const total = result.length;
    const sliced = result.slice(0, MAX_ROWS);
    const rows = $("an-rows");
    rows.innerHTML = sliced.map((a) => {
      const isOpen = expanded.has(a.idx);
      const props = a.flags
        .filter((f) => !HIDDEN_AS_PILL.has(f))
        .map((f) => `<span class="an-prop ${PROP_CLASS[f] || ""}">${esc(f)}</span>`)
        .join("");
      const wcount = a.weapons.length;
      const wcountHtml = wcount === 0
        ? '<span class="an-dim">—</span>'
        : `<span class="an-wcount" data-idx="${a.idx}">${wcount} ${isOpen ? "▾" : "▸"}</span>${
            isOpen ? `<div class="an-wlist">${esc(a.weapons.join(", "))}</div>` : ""
          }`;
      return `
        <tr>
          <td>
            <div class="an-name">${esc(a.name)}</div>
            <div class="an-class">${esc(a.class)}</div>
          </td>
          <td><div class="an-props">${props || '<span class="an-dim">—</span>'}</div></td>
          <td>${wcountHtml}</td>
        </tr>`;
    }).join("");

    rows.querySelectorAll(".an-wcount").forEach((el) => {
      el.addEventListener("click", () => {
        const idx = Number(el.dataset.idx);
        if (expanded.has(idx)) expanded.delete(idx); else expanded.add(idx);
        render();
      });
    });

    document.querySelectorAll(".an-table th").forEach((th) => {
      th.classList.remove("sort-asc", "sort-desc");
      if (th.dataset.sort === key) th.classList.add(state.sortDir === "asc" ? "sort-asc" : "sort-desc");
    });

    $("an-empty").hidden = total > 0;
    const truncated = total > MAX_ROWS ? ` · 상위 ${MAX_ROWS}개 표시` : "";
    $("an-meta").textContent = `${total.toLocaleString()} / ${animations.length.toLocaleString()} matches${truncated}`;
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

이 데이터는 **emilia**의 *Elden Ring Frame Data Explorer*에서 가져왔어요.
원본 사이트에는 여기에 없는 모션값(MV)·스태미나 코스트·상태이상 빌드업
같은 더 자세한 수치 데이터가 있어요.

This dataset comes from **emilia**'s *Elden Ring Frame Data Explorer*. The
original site has additional numeric data (damage motion values, stamina
costs, status buildup) not included in this export.

- 🌐 [er-frame-data.nyasu.business](https://er-frame-data.nyasu.business/)

### Flag 의미 / Flag Meanings

| Flag | 의미 |
|------|------|
| **HyperArmour** 🔴 | 하이퍼아머 (포이즈로 끊기지 않음) / Has poise — uninterruptible |
| **Parriable** 🔵 | 패리 가능 / Can be parried |
| **Multihit** 🟣 | 한 모션에 여러 번 히트 / Multiple hits per swing |
| **WeaponSkill** 🟡 | Ash of War 사용 모션 / Ash of War skill |
| **HasSpeedGradient** | 속도 가변 (러닝 등) / Variable speed |
| **Casting** | 마법·기도 시전 / Spell/prayer casting |
| **HasBullet** | 발사체 생성 / Spawns a projectile |
| **Guard / Dodge** | 가드 / 회피 / Block / dodge |
| **Cloned / Special** | 차용·특수 / Cloned or special-cased animation |

CSV 갱신 시 `python tools/extract_animations.py`로 JSON을 재생성하고, CI가 무결성을 검증합니다.
