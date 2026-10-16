---
title: 용어 사전 탐색기 / Glossary Explorer
---

# 📖 용어 사전 탐색기 / Glossary Explorer

> 엘든 링 무기·방어구·탈리스만·소비 아이템·주문 이름의 영어-한국어 대응표입니다. 한국어나 영어로 검색할 수 있어요.
> 번역이 불확실한 항목은 상태 칸에 따로 표시됩니다.
>
> English-Korean name table for weapons, armor, talismans, consumables, spells and basic terms.
> Search in either language. Uncertain entries are flagged in the status column.
> Data is generated from `glossary/outputs/*.csv` via `glossary/tools/export_names.py`.

<style>
  .gl-controls { display: flex; flex-wrap: wrap; gap: 1rem; margin-bottom: 1rem; align-items: flex-start; }
  .gl-search-wrap { flex: 1; min-width: 240px; }
  .gl-search { width: 100%; padding: 0.55rem 0.85rem; border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px; background: var(--md-default-bg-color); color: var(--md-default-fg-color); font-size: 0.9em; }
  .gl-search:focus { outline: 2px solid var(--md-primary-fg-color); outline-offset: -1px; }
  .gl-chip-group { display: flex; gap: 0.4rem; flex-wrap: wrap; align-items: center; }
  .gl-chip-label { font-size: 0.8em; color: var(--md-default-fg-color--light); margin-right: 0.25rem; }
  .gl-chip { display: inline-flex; align-items: center; padding: 0.3rem 0.75rem; border: 1px solid var(--md-default-fg-color--lightest); border-radius: 16px; cursor: pointer; user-select: none; font-size: 0.8em; transition: all 0.15s; }
  .gl-chip:hover { border-color: var(--md-primary-fg-color); }
  .gl-chip.active { background: var(--md-primary-fg-color); color: white; border-color: var(--md-primary-fg-color); }
  .gl-table { width: 100%; border-collapse: collapse; font-size: 0.9em; margin: 0; }
  .gl-table th, .gl-table td { padding: 0.5rem 0.65rem; text-align: left; border-bottom: 1px solid var(--md-default-fg-color--lightest); }
  .gl-table th { cursor: pointer; user-select: none; background: var(--md-default-fg-color--lightest); font-weight: 600; position: sticky; top: 0; }
  .gl-table th:hover { color: var(--md-primary-fg-color); }
  .gl-table th.sort-asc::after { content: " ▲"; opacity: 0.7; }
  .gl-table th.sort-desc::after { content: " ▼"; opacity: 0.7; }
  .gl-table tr:hover td { background: var(--md-default-fg-color--lightest); }
  .gl-ko { font-weight: 600; }
  .gl-tag { display: inline-block; padding: 1px 7px; border-radius: 4px; font-size: 0.78em; border: 1px solid var(--md-default-fg-color--lightest); color: var(--md-default-fg-color--light); }
  .gl-tag-unsure { border-color: #f57c00; color: #f57c00; }
  .gl-tag-dlc { border-color: #5e35b1; color: #5e35b1; }
  .gl-empty { padding: 2rem; text-align: center; color: var(--md-default-fg-color--light); }
  .gl-meta { font-size: 0.82em; color: var(--md-default-fg-color--light); margin: 0.25rem 0 0.75rem; }
  .gl-more { margin: 0.75rem 0; }
  .gl-btn { padding: 0.35rem 0.9rem; border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px; background: var(--md-default-bg-color); color: var(--md-default-fg-color); cursor: pointer; }
  .gl-btn:hover { border-color: var(--md-primary-fg-color); }
</style>

<div id="glossary-explorer">
  <div class="gl-controls">
    <div class="gl-search-wrap">
      <input type="text" id="gl-search" class="gl-search" placeholder="🔍 한국어·영어 이름 검색 / Search Korean or English names…">
    </div>
    <div class="gl-chip-group" id="gl-category-filter">
      <span class="gl-chip-label">분류 / Category:</span>
    </div>
    <div class="gl-chip-group" id="gl-flag-filter">
      <span class="gl-chip-label">보기 / Show:</span>
    </div>
  </div>
  <div class="gl-meta" id="gl-meta">로딩 중… / Loading…</div>
  <table class="gl-table">
    <thead>
      <tr>
        <th data-sort="ko">한국어 / Korean</th>
        <th data-sort="en">English</th>
        <th data-sort="category">분류 / Category</th>
        <th data-sort="group">세부 / Group</th>
        <th data-sort="status">상태 / Status</th>
      </tr>
    </thead>
    <tbody id="gl-tbody"></tbody>
  </table>
  <div class="gl-more" id="gl-more"></div>
</div>

<script>
(function () {
  const DATA_URL = "../../assets/data/glossary_names.json";
  const PAGE_SIZE = 200;
  const filters = { search: "", category: "all", onlyUnsure: false, onlyDlc: false, sortKey: "category", sortDir: "asc", shown: PAGE_SIZE };
  let items = [];
  let categoryLabel = {};

  const $ = (id) => document.getElementById(id);

  async function init() {
    try {
      const res = await fetch(DATA_URL);
      if (!res.ok) throw new Error("HTTP " + res.status);
      const data = await res.json();
      items = data.items;
      data.categories.forEach((c) => { categoryLabel[c.key] = c.ko + " / " + c.en; });
      buildCategoryChips(data.categories);
      buildFlagChips();
      attachEvents();
      render();
    } catch (err) {
      $("gl-meta").textContent = "데이터를 불러오지 못했습니다 / Failed to load data: " + err.message;
    }
  }

  function makeChip(container, label, active, onClick) {
    const chip = document.createElement("span");
    chip.className = "gl-chip" + (active ? " active" : "");
    chip.textContent = label;
    chip.addEventListener("click", () => onClick(chip));
    container.appendChild(chip);
    return chip;
  }

  function buildCategoryChips(categories) {
    const container = $("gl-category-filter");
    const chips = [];
    const select = (key) => {
      filters.category = key;
      filters.shown = PAGE_SIZE;
      chips.forEach((c) => c.chip.classList.toggle("active", c.key === key));
      render();
    };
    chips.push({ key: "all", chip: makeChip(container, "전체 / All", true, () => select("all")) });
    categories.forEach((c) => {
      chips.push({ key: c.key, chip: makeChip(container, c.ko, false, () => select(c.key)) });
    });
  }

  function buildFlagChips() {
    const container = $("gl-flag-filter");
    makeChip(container, "확인 필요만 / Unsure only", false, (chip) => {
      filters.onlyUnsure = !filters.onlyUnsure;
      chip.classList.toggle("active", filters.onlyUnsure);
      filters.shown = PAGE_SIZE;
      render();
    });
    makeChip(container, "DLC만 / DLC only", false, (chip) => {
      filters.onlyDlc = !filters.onlyDlc;
      chip.classList.toggle("active", filters.onlyDlc);
      filters.shown = PAGE_SIZE;
      render();
    });
  }

  function attachEvents() {
    $("gl-search").addEventListener("input", (e) => {
      filters.search = e.target.value;
      filters.shown = PAGE_SIZE;
      render();
    });
    document.querySelectorAll(".gl-table th[data-sort]").forEach((th) => {
      th.addEventListener("click", () => {
        const key = th.dataset.sort;
        if (filters.sortKey === key) {
          filters.sortDir = filters.sortDir === "asc" ? "desc" : "asc";
        } else {
          filters.sortKey = key;
          filters.sortDir = "asc";
        }
        render();
      });
    });
  }

  function render() {
    const q = filters.search.trim().toLowerCase();
    let rows = items.filter((r) => {
      if (filters.category !== "all" && r.category !== filters.category) return false;
      if (filters.onlyUnsure && r.status === "ok") return false;
      if (filters.onlyDlc && !r.dlc) return false;
      if (q) {
        const hay = (r.ko + " " + r.en + " " + r.group).toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });

    const dir = filters.sortDir === "asc" ? 1 : -1;
    const key = filters.sortKey;
    const collator = new Intl.Collator(key === "ko" ? "ko" : "en");
    rows = rows.slice().sort((a, b) => dir * collator.compare(String(a[key]), String(b[key])));

    const visible = rows.slice(0, filters.shown);
    const tbody = $("gl-tbody");
    if (rows.length === 0) {
      tbody.innerHTML = '<tr><td colspan="5" class="gl-empty">조건에 맞는 항목이 없습니다 / No matching entries</td></tr>';
    } else {
      tbody.innerHTML = visible.map(rowHtml).join("");
    }

    document.querySelectorAll(".gl-table th[data-sort]").forEach((th) => {
      th.classList.remove("sort-asc", "sort-desc");
      if (th.dataset.sort === key) th.classList.add(filters.sortDir === "asc" ? "sort-asc" : "sort-desc");
    });

    $("gl-meta").textContent = rows.length + " / " + items.length + " 항목 / entries";
    const more = $("gl-more");
    if (rows.length > visible.length) {
      more.innerHTML = '<button class="gl-btn" id="gl-more-btn">더 보기 / Show more (' + (rows.length - visible.length) + ")</button>";
      $("gl-more-btn").addEventListener("click", () => { filters.shown += PAGE_SIZE; render(); });
    } else {
      more.innerHTML = "";
    }
  }

  function rowHtml(r) {
    const tags = [];
    if (r.dlc) tags.push('<span class="gl-tag gl-tag-dlc">DLC</span>');
    if (r.status !== "ok") tags.push('<span class="gl-tag gl-tag-unsure">확인 필요 / Unsure</span>');
    return (
      "<tr>" +
      '<td class="gl-ko">' + escapeHtml(r.ko || "—") + "</td>" +
      "<td>" + escapeHtml(r.en) + "</td>" +
      "<td>" + escapeHtml(categoryLabel[r.category] || r.category) + "</td>" +
      "<td>" + escapeHtml(r.group) + "</td>" +
      "<td>" + tags.join(" ") + "</td>" +
      "</tr>"
    );
  }

  const ESC_MAP = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ESC_MAP[c]);
  }

  init();
})();
</script>
