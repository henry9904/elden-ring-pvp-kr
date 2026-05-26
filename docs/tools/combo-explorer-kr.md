---
title: 트루콤보 탐색기 / True Combo Explorer (KR)
---

# ⚔️ 트루콤보 탐색기 / True Combo Explorer (KR)

> Mugen님의 트루콤보 데이터베이스를 한 눈에 검색하고 필터링하세요!
> 
> 데이터 작성: **Halvard** (Mugen)

<style>
  .we-controls { display: flex; flex-wrap: wrap; gap: 1rem; margin-bottom: 1rem; align-items: flex-start; }
  .we-search-wrap { flex: 1; min-width: 240px; }
  .we-search { width: 100%; padding: 0.55rem 0.85rem; border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px; background: var(--md-default-bg-color); color: var(--md-default-fg-color); font-size: 0.9em; }
  .we-search:focus { outline: 2px solid var(--md-primary-fg-color); outline-offset: -1px; }
  .we-select { padding: 0.5rem; border-radius: 8px; border: 1px solid var(--md-default-fg-color--lightest); background: var(--md-default-bg-color); color: var(--md-default-fg-color); max-width: 250px; }
  .we-table { width: 100%; border-collapse: collapse; font-size: 0.88em; margin: 0; }
  .we-table th, .we-table td { padding: 0.5rem 0.65rem; text-align: left; border-bottom: 1px solid var(--md-default-fg-color--lightest); }
  .we-table th { cursor: pointer; user-select: none; background: var(--md-default-fg-color--lightest); font-weight: 600; position: sticky; top: 0; }
  .we-table th:hover { color: var(--md-primary-fg-color); }
  .we-table tr:hover td { background: var(--md-default-fg-color--lightest); }
  .we-empty { padding: 2rem; text-align: center; color: var(--md-default-fg-color--light); }
  .we-meta { font-size: 0.82em; color: var(--md-default-fg-color--light); margin: 0.25rem 0 0.75rem; }
  .setup-badge { display: inline-block; background: var(--md-primary-fg-color); color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 0.8em; }
  .combo-code { font-family: 'JetBrains Mono', monospace; background: var(--md-code-bg-color); padding: 0.2em 0.4em; border-radius: 3px; font-size: 0.9em; color: var(--md-code-fg-color); }
</style>

<div id="combo-explorer">
  <div class="we-controls">
    <div class="we-search-wrap">
      <input type="text" id="we-search" class="we-search" placeholder="🔍 무기명 또는 콤보(예: L1) 검색...">
    </div>
    <select id="we-mh-select" class="we-select">
      <option value="">-- 우수 (Main Hand) 전체 --</option>
    </select>
    <select id="we-oh-select" class="we-select">
      <option value="">-- 좌수 (Off Hand) 전체 --</option>
    </select>
  </div>
  <div class="we-meta" id="we-meta">데이터 로딩 중...</div>
  <table class="we-table">
    <thead>
      <tr>
        <th>Setup</th>
        <th>우수 (Main Hand)</th>
        <th>좌수 (Off Hand)</th>
        <th>콤보 (Combo)</th>
        <th>타이트니스 (Tightness)</th>
      </tr>
    </thead>
    <tbody id="we-tbody"></tbody>
  </table>
  <div class="we-empty" id="we-empty" hidden>조건에 맞는 콤보가 없습니다.</div>
</div>

<script>
(() => {
  const DATA_URL = "../../assets/data/combos_kr.json";

  let combos = [];
  let mainHands = [];
  let offHands = [];
  
  const filters = {
    search: "",
    mainHand: "",
    offHand: ""
  };

  const $ = (id) => document.getElementById(id);

  async function init() {
    try {
      const res = await fetch(DATA_URL);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      
      // Flatten the setups into individual combo rows
      data.setups.forEach(setup => {
        setup.combos.forEach(c => {
          combos.push({
            setup_id: setup.id,
            main_hand: setup.main_hand,
            off_hand: setup.off_hand,
            combo: c.combo,
            tightness: c.tightness
          });
        });
      });
      
      mainHands = data.main_hands;
      offHands = data.off_hands;
      
      buildSelect("we-mh-select", mainHands);
      buildSelect("we-oh-select", offHands);
      
      attachEvents();
      render();
    } catch (err) {
      $("we-meta").textContent = "데이터 로드 실패: " + err.message;
    }
  }

  function buildSelect(id, items) {
    const sel = $(id);
    items.forEach(item => {
      const opt = document.createElement("option");
      opt.value = item;
      opt.textContent = item;
      sel.appendChild(opt);
    });
  }

  function attachEvents() {
    $("we-search").addEventListener("input", (e) => {
      filters.search = e.target.value.toLowerCase();
      render();
    });
    $("we-mh-select").addEventListener("change", (e) => {
      filters.mainHand = e.target.value;
      render();
    });
    $("we-oh-select").addEventListener("change", (e) => {
      filters.offHand = e.target.value;
      render();
    });
  }

  function render() {
    const q = filters.search.trim();
    let result = combos.filter((c) => {
      if (filters.mainHand && !c.main_hand.includes(filters.mainHand)) return false;
      if (filters.offHand && !c.off_hand.includes(filters.offHand)) return false;
      if (q) {
        const hay = `${c.main_hand} ${c.off_hand} ${c.combo} ${c.tightness}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });

    const tbody = $("we-tbody");
    tbody.innerHTML = result.map((c) => `
      <tr>
        <td><span class="setup-badge">${escapeHtml(c.setup_id)}</span></td>
        <td>${escapeHtml(c.main_hand)}</td>
        <td>${escapeHtml(c.off_hand)}</td>
        <td><span class="combo-code">${escapeHtml(c.combo)}</span></td>
        <td>${escapeHtml(c.tightness)}</td>
      </tr>
    `).join("");

    $("we-empty").hidden = result.length > 0;
    $("we-meta").textContent = `${result.length} / ${combos.length} 콤보 표시 중`;
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
