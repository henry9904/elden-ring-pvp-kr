---
title: 애니메이션 / 프레임 데이터 탐색기 / Animations & Frame Data Explorer
---

# 🎯 애니메이션 / 프레임 데이터 탐색기 / Animations Explorer

> 모든 무기 + Ash of War 애니메이션의 **동작 속성** (하이퍼아머·패리 가능·멀티히트·웨폰 스킬 등)을
> 검색·필터할 수 있어요. **7,874개 애니메이션 × 19개 flag × 334개 클래스**.
>
> Every weapon + Ash of War animation tagged with behavioral flags
> (HyperArmour, Parriable, Multihit, WeaponSkill, …). Look up exactly which
> attacks can be parried, which have hyperarmor, or which AoWs share an
> animation across weapon classes.
>
> **Data source: [emilia](https://er-frame-data.nyasu.business/) (Elden Ring Frame Data Explorer)**

<style>
  .an-controls { display: flex; flex-direction: column; gap: 0.6rem; margin-bottom: 1rem; }
  .an-row { display: flex; flex-wrap: wrap; gap: 0.6rem; align-items: center; }
  .an-search { flex: 1; min-width: 220px; padding: 0.55rem 0.85rem; border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px; background: var(--md-default-bg-color); color: var(--md-default-fg-color); font-size: 0.9em; }
  .an-search:focus { outline: 2px solid var(--md-primary-fg-color); outline-offset: -1px; }
  .an-chip-group { display: flex; gap: 0.35rem; flex-wrap: wrap; align-items: center; }
  .an-chip-label { font-size: 0.78em; color: var(--md-default-fg-color--light); margin-right: 0.2rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
  .an-chip { display: inline-flex; align-items: center; padding: 0.25rem 0.65rem; border: 1px solid var(--md-default-fg-color--lightest); border-radius: 14px; cursor: pointer; user-select: none; font-size: 0.78em; transition: all 0.12s; white-space: nowrap; }
  .an-chip:hover { border-color: var(--md-primary-fg-color); }
  .an-chip.active { background: var(--md-primary-fg-color); color: white; border-color: var(--md-primary-fg-color); }
  .an-class-wrap { display: flex; flex-direction: column; gap: 0.4rem; flex: 1; min-width: 220px; }
  .an-class-search { padding: 0.4rem 0.7rem; border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px; background: var(--md-default-bg-color); color: var(--md-default-fg-color); font-size: 0.82em; }
  .an-class-chips { max-height: 7rem; overflow-y: auto; display: flex; gap: 0.3rem; flex-wrap: wrap; padding: 0.25rem 0; }
  .an-table-wrap { overflow-x: auto; max-height: 70vh; border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px; }
  .an-table { width: 100%; border-collapse: collapse; font-size: 0.82em; margin: 0; }
  .an-table th, .an-table td { padding: 0.4rem 0.6rem; text-align: left; border-bottom: 1px solid var(--md-default-fg-color--lightest); vertical-align: top; }
  .an-table th { cursor: pointer; user-select: none; background: var(--md-default-bg-color); font-weight: 600; position: sticky; top: 0; z-index: 1; box-shadow: 0 1px 0 var(--md-default-fg-color--lightest); white-space: nowrap; }
  .an-table th:hover { color: var(--md-primary-fg-color); }
  .an-table th.sort-asc::after { content: " ▲"; opacity: 0.7; }
  .an-table th.sort-desc::after { content: " ▼"; opacity: 0.7; }
  .an-table tr:hover td { background: var(--md-default-fg-color--lightest); }
  .an-name { font-weight: 500; white-space: nowrap; }
  .an-class { color: var(--md-default-fg-color--light); white-space: nowrap; }
  .an-flags { display: flex; flex-wrap: wrap; gap: 0.25rem; }
  .an-flag { display: inline-block; padding: 1px 7px; border-radius: 10px; font-size: 0.74em; font-weight: 500; border: 1px solid; white-space: nowrap; }
  .an-flag-Attack { background: rgba(96, 125, 139, 0.15); color: #b0bec5; border-color: rgba(96, 125, 139, 0.4); }
  .an-flag-Parriable { background: rgba(33, 150, 243, 0.18); color: #64b5f6; border-color: rgba(33, 150, 243, 0.45); }
  .an-flag-HyperArmour { background: rgba(244, 67, 54, 0.18); color: #ef9a9a; border-color: rgba(244, 67, 54, 0.5); font-weight: 600; }
  .an-flag-Multihit { background: rgba(156, 39, 176, 0.18); color: #ce93d8; border-color: rgba(156, 39, 176, 0.4); }
  .an-flag-WeaponSkill { background: rgba(255, 193, 7, 0.18); color: #ffd54f; border-color: rgba(255, 193, 7, 0.45); }
  .an-flag-Special { background: rgba(63, 81, 181, 0.18); color: #9fa8da; border-color: rgba(63, 81, 181, 0.4); }
  .an-flag-HasSpeedGradient { background: rgba(255, 152, 0, 0.18); color: #ffb74d; border-color: rgba(255, 152, 0, 0.4); }
  .an-flag-Casting { background: rgba(0, 188, 212, 0.18); color: #80deea; border-color: rgba(0, 188, 212, 0.4); }
  .an-flag-Cloned { background: rgba(121, 85, 72, 0.18); color: #bcaaa4; border-color: rgba(121, 85, 72, 0.4); }
  .an-flag-HasBullet { background: rgba(76, 175, 80, 0.18); color: #a5d6a7; border-color: rgba(76, 175, 80, 0.4); }
  .an-flag-Guard { background: rgba(76, 175, 80, 0.18); color: #81c784; border-color: rgba(76, 175, 80, 0.5); }
  .an-flag-Dodge { background: rgba(0, 150, 136, 0.18); color: #80cbc4; border-color: rgba(0, 150, 136, 0.4); }
  .an-weapons { font-size: 0.92em; }
  .an-weapons-more { color: var(--md-primary-fg-color); cursor: pointer; text-decoration: underline; font-size: 0.92em; }
  .an-empty { padding: 2rem; text-align: center; color: var(--md-default-fg-color--light); }
  .an-meta { font-size: 0.82em; color: var(--md-default-fg-color--light); margin: 0.25rem 0 0.5rem; }
  .an-mode { display: inline-flex; align-items: center; gap: 0.4rem; font-size: 0.78em; color: var(--md-default-fg-color--light); }
  .an-mode input { margin: 0; }
  [data-md-color-scheme="default"] .an-flag-Attack { color: #455a64; }
  [data-md-color-scheme="default"] .an-flag-Parriable { color: #1565c0; }
  [data-md-color-scheme="default"] .an-flag-HyperArmour { color: #c62828; }
  [data-md-color-scheme="default"] .an-flag-Multihit { color: #6a1b9a; }
  [data-md-color-scheme="default"] .an-flag-WeaponSkill { color: #ef6c00; }
  [data-md-color-scheme="default"] .an-flag-Special { color: #283593; }
  [data-md-color-scheme="default"] .an-flag-HasSpeedGradient { color: #e65100; }
  [data-md-color-scheme="default"] .an-flag-Casting { color: #00838f; }
  [data-md-color-scheme="default"] .an-flag-Cloned { color: #5d4037; }
  [data-md-color-scheme="default"] .an-flag-HasBullet { color: #2e7d32; }
  [data-md-color-scheme="default"] .an-flag-Guard { color: #2e7d32; }
  [data-md-color-scheme="default"] .an-flag-Dodge { color: #00695c; }
</style>

<div id="animations-explorer">
  <div class="an-controls">
    <div class="an-row">
      <input type="text" id="an-search" class="an-search" placeholder="🔍 애니메이션·무기 검색 / Search animation name or weapon…">
    </div>
    <div class="an-row">
      <div class="an-chip-group" id="an-flag-filter">
        <span class="an-chip-label">Flags</span>
      </div>
      <label class="an-mode">
        <input type="radio" name="an-flag-mode" value="and" checked> 모두 포함 / AND
      </label>
      <label class="an-mode">
        <input type="radio" name="an-flag-mode" value="or"> 하나라도 / OR
      </label>
    </div>
    <div class="an-row">
      <div class="an-class-wrap">
        <input type="text" id="an-class-search" class="an-class-search" placeholder="무기 클래스 / AoW 필터 (예: dagger, lion's claw) — 클릭으로 선택">
        <div class="an-class-chips" id="an-class-filter"></div>
      </div>
    </div>
  </div>
  <div class="an-meta" id="an-meta">로딩 중… / Loading…</div>
  <div class="an-table-wrap">
    <table class="an-table">
      <thead>
        <tr>
          <th data-sort="name">Animation</th>
          <th data-sort="class">Class / AoW</th>
          <th data-sort="flag_count">Flags</th>
          <th data-sort="weapon_count">Weapons</th>
        </tr>
      </thead>
      <tbody id="an-tbody"></tbody>
    </table>
  </div>
  <div class="an-empty" id="an-empty" hidden>No animations match your filters.</div>
</div>

<script>
(() => {
  const DATA_URL = "../../assets/data/animations.json";
  const NUMERIC_KEYS = new Set(["flag_count", "weapon_count"]);
  const DEFAULT_DESC = new Set(["flag_count", "weapon_count"]);
  const MAX_ROWS = 250;
  const WEAPON_PREVIEW = 3;

  let animations = [];
  let allClasses = [];
  const expanded = new Set();
  const filters = {
    search: "",
    classes: new Set(),
    flags: new Set(),
    flagMode: "and",
    classFilter: "",
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
        flag_count: a.flags.length,
        weapon_count: a.weapons.length,
        searchKey: `${a.name} ${a.id} ${a.class} ${a.weapons.join(" ")}`.toLowerCase(),
      }));
      allClasses = data.weapon_classes;
      buildFlagChips(data.flags);
      renderClassChips();
      attachEvents();
      render();
    } catch (err) {
      $("an-meta").textContent = "데이터 로드 실패 / Failed to load data: " + err.message;
    }
  }

  function buildFlagChips(flags) {
    const c = $("an-flag-filter");
    flags.forEach((f) => {
      const chip = document.createElement("span");
      chip.className = "an-chip";
      chip.textContent = f;
      chip.addEventListener("click", () => {
        if (filters.flags.has(f)) {
          filters.flags.delete(f);
          chip.classList.remove("active");
        } else {
          filters.flags.add(f);
          chip.classList.add("active");
        }
        render();
      });
      c.appendChild(chip);
    });
  }

  function renderClassChips() {
    const c = $("an-class-filter");
    const q = filters.classFilter.trim().toLowerCase();
    let list = allClasses;
    if (q) list = list.filter((cls) => cls.toLowerCase().includes(q));
    else list = list.slice(0, 40);
    c.innerHTML = "";
    list.forEach((cls) => {
      const chip = document.createElement("span");
      chip.className = "an-chip" + (filters.classes.has(cls) ? " active" : "");
      chip.textContent = cls;
      chip.addEventListener("click", () => {
        if (filters.classes.has(cls)) {
          filters.classes.delete(cls);
          chip.classList.remove("active");
        } else {
          filters.classes.add(cls);
          chip.classList.add("active");
        }
        render();
      });
      c.appendChild(chip);
    });
    if (!q && allClasses.length > 40) {
      const hint = document.createElement("span");
      hint.className = "an-chip";
      hint.style.cursor = "default";
      hint.style.fontStyle = "italic";
      hint.style.opacity = "0.6";
      hint.textContent = `+${allClasses.length - 40} more — type to search`;
      c.appendChild(hint);
    }
  }

  function attachEvents() {
    $("an-search").addEventListener("input", (e) => {
      filters.search = e.target.value.toLowerCase();
      render();
    });
    $("an-class-search").addEventListener("input", (e) => {
      filters.classFilter = e.target.value;
      renderClassChips();
    });
    document.querySelectorAll('input[name="an-flag-mode"]').forEach((r) => {
      r.addEventListener("change", (e) => {
        filters.flagMode = e.target.value;
        render();
      });
    });
    document.querySelectorAll(".an-table th").forEach((th) => {
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

  function matchFlags(a) {
    if (filters.flags.size === 0) return true;
    if (filters.flagMode === "and") {
      for (const f of filters.flags) if (!a.flags.includes(f)) return false;
      return true;
    }
    for (const f of filters.flags) if (a.flags.includes(f)) return true;
    return false;
  }

  function render() {
    const q = filters.search.trim();
    let result = animations.filter((a) => {
      if (filters.classes.size && !filters.classes.has(a.class)) return false;
      if (!matchFlags(a)) return false;
      if (q && !a.searchKey.includes(q)) return false;
      return true;
    });

    const dir = filters.sortDir === "asc" ? 1 : -1;
    const key = filters.sortKey;
    const isNum = NUMERIC_KEYS.has(key);
    result.sort((a, b) => {
      const va = a[key], vb = b[key];
      if (isNum) return (va - vb) * dir;
      return String(va).localeCompare(String(vb)) * dir;
    });

    const total = result.length;
    const sliced = result.slice(0, MAX_ROWS);
    const tbody = $("an-tbody");
    tbody.innerHTML = sliced.map((a) => {
      const isOpen = expanded.has(a.idx);
      const weaponsHtml = renderWeapons(a, isOpen);
      const flagsHtml = a.flags.map((f) =>
        `<span class="an-flag an-flag-${cssClass(f)}">${esc(f)}</span>`
      ).join("");
      return `
        <tr>
          <td class="an-name">${esc(a.name)}</td>
          <td class="an-class">${esc(a.class)}</td>
          <td><div class="an-flags">${flagsHtml}</div></td>
          <td class="an-weapons">${weaponsHtml}</td>
        </tr>`;
    }).join("");

    tbody.querySelectorAll(".an-weapons-more").forEach((el) => {
      el.addEventListener("click", () => {
        const idx = Number(el.dataset.idx);
        if (expanded.has(idx)) expanded.delete(idx); else expanded.add(idx);
        render();
      });
    });

    document.querySelectorAll(".an-table th").forEach((th) => {
      th.classList.remove("sort-asc", "sort-desc");
      if (th.dataset.sort === key) th.classList.add(filters.sortDir === "asc" ? "sort-asc" : "sort-desc");
    });

    $("an-empty").hidden = total > 0;
    const truncated = total > MAX_ROWS ? ` (상위 ${MAX_ROWS}개 표시 / showing top ${MAX_ROWS})` : "";
    $("an-meta").textContent = `${sliced.length.toLocaleString()} / ${total.toLocaleString()} of ${animations.length.toLocaleString()} 애니메이션${truncated} — 컬럼 헤더 클릭으로 정렬`;
  }

  function renderWeapons(a, isOpen) {
    if (a.weapons.length === 0) return '<span style="opacity:0.5">—</span>';
    if (isOpen || a.weapons.length <= WEAPON_PREVIEW) {
      return esc(a.weapons.join(", "));
    }
    const preview = a.weapons.slice(0, WEAPON_PREVIEW).join(", ");
    const more = a.weapons.length - WEAPON_PREVIEW;
    return `${esc(preview)} <span class="an-weapons-more" data-idx="${a.idx}">+${more} more</span>`;
  }

  function cssClass(flag) {
    return flag.replace(/[^A-Za-z0-9]/g, "");
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
원본 사이트에는 여기에 없는 모션값(MV), 스태미나 코스트, 상태이상 빌드업 같은
더 자세한 수치 데이터가 있어요.

This dataset comes from **emilia**'s *Elden Ring Frame Data Explorer*. The
original site has additional numeric data (damage motion values, stamina
costs, status buildup) that isn't included in this export.

- 🌐 원본 / Original site: [er-frame-data.nyasu.business](https://er-frame-data.nyasu.business/)

### Flag 의미 / Flag Meanings

| Flag | 의미 |
|------|------|
| **Attack** | 적에게 피해를 주는 일반 공격 / Damaging attack |
| **Parriable** | 패리 가능 / Can be parried |
| **HyperArmour** | 하이퍼아머가 발동되는 모션 / Has poise / hyperarmor |
| **Multihit** | 한 모션에서 여러 번 히트 / Multiple hit instances |
| **WeaponSkill** | Ash of War 사용 모션 / Ash of War skill |
| **HasSpeedGradient** | 속도가 가변적 (러닝 어택 등) / Variable speed (running attacks, etc.) |
| **Casting** | 마법·기도 시전 모션 / Spell/prayer casting |
| **HasBullet** | 발사체 생성 / Spawns a projectile |
| **Guard** | 가드 동작 / Guard / block |
| **Dodge** | 회피·구르기 / Dodge / roll |
| **Cloned** | 다른 클래스 모션 차용 / Cloned animation |
| **Special** | 특수 상태 / Special / unique state |

CSV 갱신 시 `python tools/extract_animations.py`로 JSON을 재생성하고, CI가 무결성을 검증합니다.
