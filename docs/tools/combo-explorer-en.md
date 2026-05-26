---
title: True Combo Explorer (EN)
---

# ⚔️ True Combo Explorer (EN)

> Search, filter, and discover all true combos from Mugen's database!
>
> Data by: **Halvard** (Mugen)

<style>
  /* ── Layout ── */
  .ce-controls {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
    align-items: center;
  }
  .ce-search-wrap { flex: 1; min-width: 220px; }
  .ce-search {
    width: 100%;
    padding: 0.55rem 0.85rem;
    border: 1px solid var(--md-default-fg-color--lightest);
    border-radius: 8px;
    background: var(--md-default-bg-color);
    color: var(--md-default-fg-color);
    font-size: 0.9em;
  }
  .ce-search:focus { outline: 2px solid var(--md-primary-fg-color); outline-offset: -1px; }

  .ce-select {
    padding: 0.5rem 0.7rem;
    border-radius: 8px;
    border: 1px solid var(--md-default-fg-color--lightest);
    background: var(--md-default-bg-color);
    color: var(--md-default-fg-color);
    font-size: 0.85em;
    max-width: 240px;
    min-width: 170px;
  }
  .ce-select:focus { outline: 2px solid var(--md-primary-fg-color); outline-offset: -1px; }
  .ce-btn {
    padding: 0.5rem 0.85rem;
    border-radius: 8px;
    border: 1px solid var(--md-default-fg-color--lightest);
    background: var(--md-default-bg-color);
    color: var(--md-default-fg-color--light);
    font-size: 0.85em;
    cursor: pointer;
    white-space: nowrap;
  }
  .ce-btn:hover { border-color: var(--md-primary-fg-color); color: var(--md-primary-fg-color); }
  .ce-pair-hint {
    font-size: 0.78em;
    color: var(--md-primary-fg-color);
    margin: -0.25rem 0 0.5rem;
  }

  /* ── Chip bar ── */
  .ce-chip-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-bottom: 0.75rem;
  }
  .ce-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.3rem 0.7rem;
    border: 1px solid var(--md-default-fg-color--lighter);
    border-radius: 999px;
    background: var(--md-default-bg-color);
    color: var(--md-default-fg-color);
    font-size: 0.82em;
    cursor: pointer;
    user-select: none;
    transition: background 0.15s, color 0.15s, border-color 0.15s;
    white-space: nowrap;
  }
  .ce-chip:hover { border-color: var(--md-primary-fg-color); color: var(--md-primary-fg-color); }
  .ce-chip.active {
    background: var(--md-primary-fg-color);
    border-color: var(--md-primary-fg-color);
    color: #fff;
    font-weight: 600;
  }

  /* ── Meta ── */
  .ce-meta { font-size: 0.82em; color: var(--md-default-fg-color--light); margin: 0.25rem 0 0.6rem; }

  /* ── Table ── */
  .ce-table { width: 100%; border-collapse: collapse; font-size: 0.86em; margin: 0; }
  .ce-table th, .ce-table td { padding: 0.45rem 0.65rem; text-align: left; border-bottom: 1px solid var(--md-default-fg-color--lightest); }
  .ce-table th {
    background: var(--md-default-fg-color--lightest);
    font-weight: 600;
    position: sticky;
    top: 0;
    z-index: 2;
  }
  .ce-table tr:hover td { background: var(--md-default-fg-color--lightest); }

  /* Group header rows */
  .ce-group-row td {
    background: var(--md-primary-fg-color--light, #e8f0fe);
    font-weight: 700;
    font-size: 0.88em;
    padding: 0.5rem 0.65rem;
    letter-spacing: 0.02em;
    position: sticky;
    top: 2.3rem;
    z-index: 1;
    border-bottom: 2px solid var(--md-primary-fg-color);
  }
  [data-md-color-scheme="slate"] .ce-group-row td {
    background: rgba(var(--md-primary-fg-color--rgb, 99,108,158), 0.18);
  }

  /* Weapon cells: truncate + full text on hover */
  .weapon-cell {
    max-width: 180px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .setup-badge {
    display: inline-block;
    background: var(--md-primary-fg-color);
    color: #fff;
    padding: 1px 6px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 0.78em;
  }
  .combo-code {
    font-family: 'JetBrains Mono', monospace;
    background: var(--md-code-bg-color);
    padding: 0.15em 0.4em;
    border-radius: 3px;
    font-size: 0.88em;
    color: var(--md-code-fg-color);
  }
  .ce-empty { padding: 2rem; text-align: center; color: var(--md-default-fg-color--light); }
</style>

<div id="combo-explorer">
  <div class="ce-chip-bar" id="ce-chips">
    <button class="ce-chip active" data-class="">All Classes</button>
  </div>
  <div class="ce-controls">
    <div class="ce-search-wrap">
      <input type="text" id="ce-search" class="ce-search" placeholder="🔍 Search weapons or combo inputs (e.g. R1, L1, Dagger)...">
    </div>
    <select id="ce-mh-select" class="ce-select" aria-label="Main hand filter">
      <option value="">-- All Main Hand --</option>
    </select>
    <select id="ce-oh-select" class="ce-select" aria-label="Off hand filter">
      <option value="">-- All Off Hand --</option>
    </select>
    <button id="ce-reset" class="ce-btn" type="button">Reset</button>
  </div>
  <div class="ce-pair-hint" id="ce-pair-hint" hidden></div>
  <div class="ce-meta" id="ce-meta">Loading data...</div>
  <div style="overflow-x:auto;">
    <table class="ce-table">
      <thead>
        <tr>
          <th style="min-width:54px">Setup</th>
          <th style="min-width:140px">Main Hand</th>
          <th style="min-width:140px">Off Hand</th>
          <th style="min-width:200px">Combo</th>
          <th style="min-width:110px">Tightness</th>
        </tr>
      </thead>
      <tbody id="ce-tbody"></tbody>
    </table>
  </div>
  <div class="ce-empty" id="ce-empty" hidden>No combos match your filters.</div>
</div>

<script>
(() => {
  const DATA_URL = "../../assets/data/combos_en.json";

  let allCombos = [];
  let weaponClasses = [];
  const filters = { search: "", weaponClasses: new Set(), mainHand: "", offHand: "" };
  const $ = id => document.getElementById(id);
  const parseList = s => String(s || "").split(",").map(w => w.trim()).filter(Boolean);

  async function init() {
    try {
      const res = await fetch(DATA_URL);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      weaponClasses = data.weapon_classes || [];

      data.setups.forEach(setup => {
        setup.combos.forEach(c => {
          allCombos.push({
            setup_id: setup.id,
            weapon_class: setup.weapon_class || "",
            main_hand: setup.main_hand,
            off_hand: setup.off_hand,
            combo: c.combo,
            tightness: c.tightness
          });
        });
      });

      buildChips();
      attachEvents();
      rebuildSelects();
      render();
    } catch (err) {
      $("ce-meta").textContent = "Failed to load data: " + err.message;
    }
  }

  // Repopulate the two weapon dropdowns based on current class chip(s) + the OTHER select.
  // Picking a Main Hand narrows the Off Hand list to only pair-able weapons, and vice versa.
  function rebuildSelects() {
    const classCombos = filters.weaponClasses.size > 0
      ? allCombos.filter(c => filters.weaponClasses.has(c.weapon_class))
      : allCombos;

    // Off-hand options: pairings allowed with current Main-Hand selection
    const ohCombos = filters.mainHand
      ? classCombos.filter(c => parseList(c.main_hand).includes(filters.mainHand))
      : classCombos;
    const ohSet = new Set();
    ohCombos.forEach(c => parseList(c.off_hand).forEach(w => ohSet.add(w)));

    // Main-hand options: pairings allowed with current Off-Hand selection
    const mhCombos = filters.offHand
      ? classCombos.filter(c => parseList(c.off_hand).includes(filters.offHand))
      : classCombos;
    const mhSet = new Set();
    mhCombos.forEach(c => parseList(c.main_hand).forEach(w => mhSet.add(w)));

    populateSelect("ce-mh-select", [...mhSet].sort(), filters.mainHand, "-- All Main Hand --", "mainHand");
    populateSelect("ce-oh-select", [...ohSet].sort(), filters.offHand, "-- All Off Hand --", "offHand");

    updatePairHint();
  }

  function populateSelect(id, items, current, placeholder, key) {
    const sel = $(id);
    const stillValid = current && items.includes(current);
    sel.innerHTML = `<option value="">${placeholder}</option>` +
      items.map(w => `<option value="${esc(w)}"${w === current ? " selected" : ""}>${esc(w)}</option>`).join("");
    if (!stillValid && current) {
      filters[key] = "";
    }
  }

  function updatePairHint() {
    const hint = $("ce-pair-hint");
    if (filters.mainHand && !filters.offHand) {
      const n = $("ce-oh-select").options.length - 1;
      hint.textContent = `Off-Hand list narrowed to ${n} weapon${n !== 1 ? "s" : ""} that pair with "${filters.mainHand}".`;
      hint.hidden = false;
    } else if (filters.offHand && !filters.mainHand) {
      const n = $("ce-mh-select").options.length - 1;
      hint.textContent = `Main-Hand list narrowed to ${n} weapon${n !== 1 ? "s" : ""} that pair with "${filters.offHand}".`;
      hint.hidden = false;
    } else {
      hint.hidden = true;
    }
  }

  function buildChips() {
    const bar = $("ce-chips");
    weaponClasses.forEach(cls => {
      const btn = document.createElement("button");
      btn.className = "ce-chip";
      btn.dataset.class = cls;
      btn.textContent = cls;
      btn.addEventListener("click", () => toggleChip(btn));
      bar.appendChild(btn);
    });
    bar.querySelector('[data-class=""]').addEventListener("click", resetChips);
  }

  function toggleChip(el) {
    const cls = el.dataset.class;
    if (filters.weaponClasses.has(cls)) {
      filters.weaponClasses.delete(cls);
      el.classList.remove("active");
    } else {
      filters.weaponClasses.add(cls);
      el.classList.add("active");
      $("ce-chips").querySelector('[data-class=""]').classList.remove("active");
    }
    if (filters.weaponClasses.size === 0) {
      $("ce-chips").querySelector('[data-class=""]').classList.add("active");
    }
    rebuildSelects();
    render();
  }

  function resetChips() {
    filters.weaponClasses.clear();
    $("ce-chips").querySelectorAll(".ce-chip").forEach(c => c.classList.remove("active"));
    $("ce-chips").querySelector('[data-class=""]').classList.add("active");
    rebuildSelects();
    render();
  }

  function attachEvents() {
    $("ce-search").addEventListener("input", e => {
      filters.search = e.target.value.toLowerCase();
      render();
    });
    $("ce-mh-select").addEventListener("change", e => {
      filters.mainHand = e.target.value;
      rebuildSelects();
      render();
    });
    $("ce-oh-select").addEventListener("change", e => {
      filters.offHand = e.target.value;
      rebuildSelects();
      render();
    });
    $("ce-reset").addEventListener("click", () => {
      filters.search = "";
      filters.weaponClasses.clear();
      filters.mainHand = "";
      filters.offHand = "";
      $("ce-search").value = "";
      $("ce-chips").querySelectorAll(".ce-chip").forEach(c => c.classList.remove("active"));
      $("ce-chips").querySelector('[data-class=""]').classList.add("active");
      rebuildSelects();
      render();
    });
  }

  function render() {
    const q = filters.search.trim();

    let filtered = allCombos.filter(c => {
      if (filters.weaponClasses.size > 0 && !filters.weaponClasses.has(c.weapon_class)) return false;
      if (filters.mainHand && !parseList(c.main_hand).includes(filters.mainHand)) return false;
      if (filters.offHand && !parseList(c.off_hand).includes(filters.offHand)) return false;
      if (q) {
        const hay = `${c.weapon_class} ${c.main_hand} ${c.off_hand} ${c.combo} ${c.tightness}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });

    // Group by weapon class (preserve archive order)
    const groups = [];
    const groupMap = new Map();
    filtered.forEach(c => {
      if (!groupMap.has(c.weapon_class)) {
        const g = { name: c.weapon_class, rows: [] };
        groups.push(g);
        groupMap.set(c.weapon_class, g);
      }
      groupMap.get(c.weapon_class).rows.push(c);
    });

    // Show group headers when more than one class is visible
    const showGroupHeaders = groups.length > 1;
    const tbody = $("ce-tbody");
    const parts = [];

    groups.forEach(g => {
      if (showGroupHeaders) {
        parts.push(
          `<tr class="ce-group-row"><td colspan="5">${esc(g.name)}</td></tr>`
        );
      }
      g.rows.forEach(r => {
        parts.push(`<tr>
          <td><span class="setup-badge">${esc(r.setup_id)}</span></td>
          <td class="weapon-cell" title="${esc(r.main_hand)}">${esc(r.main_hand)}</td>
          <td class="weapon-cell" title="${esc(r.off_hand)}">${esc(r.off_hand)}</td>
          <td><span class="combo-code">${esc(r.combo)}</span></td>
          <td>${esc(r.tightness)}</td>
        </tr>`);
      });
    });

    tbody.innerHTML = parts.join("");
    $("ce-empty").hidden = filtered.length > 0;

    const setupCount = new Set(filtered.map(c => `${c.weapon_class}|${c.setup_id}`)).size;
    const clsLabel = filters.weaponClasses.size > 0
      ? `${groups.length} selected class${groups.length !== 1 ? "es" : ""}`
      : `${groups.length} weapon class${groups.length !== 1 ? "es" : ""}`;
    $("ce-meta").textContent = filtered.length
      ? `Showing ${filtered.length} combo${filtered.length !== 1 ? "s" : ""} from ${setupCount} setup${setupCount !== 1 ? "s" : ""} across ${clsLabel}`
      : "";
  }

  const ESC_MAP = {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"};
  function esc(s) {
    return String(s).replace(/[&<>"']/g, c => ESC_MAP[c]);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
</script>
