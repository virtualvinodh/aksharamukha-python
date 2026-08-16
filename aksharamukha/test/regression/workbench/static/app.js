const state = { tables: {} };

const EDITABLE = new Set(['source_texts']);

async function api(path, opts) {
  const res = await fetch(path, opts);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

async function loadTable(name) {
  const data = await api('/api/table/' + name);
  state.tables[name] = data;
  if (name === 'source_texts') sourceTextsSelected.clear();
  if (name === 'options_catalog') renderCatalog();
  else renderTable(name);
}

function cellClass (name, col, value, row) {
  if (col === 'error' && value) return 'col-error';
  if (col === 'backend_status') return '';
  if ((col === 'meaningful' || col === 'matches_original' || col === 'in_frontend')) {
    return value === 'True' || value === true ? 'col-bool-true' : 'col-bool-false';
  }
  return '';
}

function renderCellContent (name, col, value, row) {
  if (col === 'backend_status') {
    const cls = { working: 'pill-working', broken: 'pill-broken', 'working-multi-arg': 'pill-multiarg' }[value] || 'pill-unknown';
    return `<span class="pill ${cls}">${escapeHtml(value)}</span>`;
  }
  if (col === 'approve') {
    const checked = (value === 'yes' || value === 'y' || value === 'true') ? 'checked' : '';
    return `<input type="checkbox" class="approve-box" ${checked}>`;
  }
  return escapeHtml(value == null ? '' : String(value));
}

function escapeHtml (s) {
  return String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

// ---------------------------------------------------------------------------
// Generic editable-table CRUD, used only for Source Texts now (the other
// CSV-backed tables from the old propose/review workflow - fanout_requests,
// option_test_requests, and their results - are superseded by the
// generation buttons + direct viewer/editor tabs below, and no longer
// surfaced in the UI; their backend routes/files are untouched, just unused).
// ---------------------------------------------------------------------------
// Selection is keyed by row.id (a string), not object reference or index -
// collectRowsFromDOM() rebuilds a brand new row object on every call (reads
// straight from the DOM), so neither survives across it, but id is stable.
let sourceTextsSelected = new Set();

function renderTable (name) {
  const { columns, rows } = state.tables[name];
  const el = document.getElementById('table-' + name);
  const editable = EDITABLE.has(name);
  const isSourceTexts = name === 'source_texts';

  let thead = '<thead><tr>';
  if (isSourceTexts) {
    const allChecked = rows.length > 0 && rows.every(r => sourceTextsSelected.has(r.id));
    thead += `<th><input type="checkbox" class="st-select-all" ${allChecked ? 'checked' : ''}></th>`;
  }
  for (const c of columns) thead += `<th>${c}</th>`;
  if (isSourceTexts) thead += '<th>generate</th>';
  if (editable) thead += '<th></th>';
  thead += '</tr></thead>';

  let tbody = '<tbody>';
  rows.forEach((row, i) => {
    tbody += `<tr data-idx="${i}">`;
    if (isSourceTexts) {
      tbody += `<td><input type="checkbox" class="row-select st-row-select" data-st-select-i="${i}" ${sourceTextsSelected.has(row.id) ? 'checked' : ''}></td>`;
    }
    for (const c of columns) {
      const val = row[c] !== undefined ? row[c] : '';
      const cls = cellClass(name, c, val, row);
      if (editable) {
        tbody += `<td class="${cls}" data-col="${c}" contenteditable="true">${escapeHtml(val)}</td>`;
      } else {
        tbody += `<td class="readonly ${cls}" data-col="${c}">${renderCellContent(name, c, val, row)}</td>`;
      }
    }
    if (isSourceTexts) tbody += sourceTextActionsHtml(row, i);
    if (editable) {
      tbody += `<td><button class="btn-remove-row" data-remove="${name}:${i}" title="Remove row">✕</button></td>`;
    }
    tbody += '</tr>';
  });
  tbody += '</tbody>';

  el.innerHTML = thead + tbody;
  if (isSourceTexts) updateSourceTextsSelectionUI();
}

function updateSourceTextsSelectionUI () {
  document.querySelectorAll('[data-st-delete-selected]').forEach(btn => {
    btn.textContent = `Delete selected (${sourceTextsSelected.size})`;
    btn.disabled = sourceTextsSelected.size === 0;
  });
}

function deleteSelectedSourceTexts () {
  if (sourceTextsSelected.size === 0) return;
  collectRowsFromDOM('source_texts');
  state.tables.source_texts.rows = state.tables.source_texts.rows.filter(r => !sourceTextsSelected.has(r.id));
  sourceTextsSelected.clear();
  renderTable('source_texts');
}

// Generation is triggered per-row from here, against that row's own
// script/text - not by a global button on each viewer tab (see the 5
// conversion tabs and Post-options/Pre-options, which only render whatever
// has already been generated).
function sourceTextActionsHtml (row, i) {
  let html = '<td class="row-actions">';
  html += `<button class="btn btn-small" data-src-gen="all_fanout" data-row-idx="${i}" title="Generate baseline conversions to every script, nativize true &amp; false">all-fanout</button> `;
  html += `<button class="btn btn-small" data-src-pair data-row-idx="${i}" title="Generate just one source → target pair">pair</button>`;
  if ((row.script || '').trim() === 'Devanagari') {
    html += ` <button class="btn btn-small" data-src-gen-opts="post" data-row-idx="${i}" title="Generate full post-option coverage from this text">post-opts</button>`;
    html += ` <button class="btn btn-small" data-src-gen-opts="pre" data-row-idx="${i}" title="Generate full pre-option coverage from this text">pre-opts</button>`;
  }
  html += '</td>';
  return html;
}

function collectRowsFromDOM (name) {
  const { columns } = state.tables[name];
  const el = document.getElementById('table-' + name);
  const rows = [];
  el.querySelectorAll('tbody tr').forEach(tr => {
    const row = {};
    columns.forEach(c => {
      const td = tr.querySelector(`td[data-col="${c}"]`);
      row[c] = td ? td.textContent : '';
    });
    rows.push(row);
  });
  state.tables[name].rows = rows;
  return rows;
}

async function saveTable (name) {
  const rows = collectRowsFromDOM(name);
  await api('/api/table/' + name, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ rows })
  });
  flash(`Saved ${name} (${rows.length} rows)`);
}

function addRow (name) {
  collectRowsFromDOM(name);
  const blank = {};
  state.tables[name].columns.forEach(c => { blank[c] = ''; });
  state.tables[name].rows.push(blank);
  renderTable(name);
}

function removeRow (name, idx) {
  collectRowsFromDOM(name);
  state.tables[name].rows.splice(idx, 1);
  renderTable(name);
}

// Source Texts uses a popup form (like Add Case) instead of an inline blank
// contenteditable row - and assigns id automatically, since it's just an
// internal join key nothing in the UI asks you to type anywhere else.
function toggleAddSourceTextForm (show) {
  const el = document.getElementById('add-sourcetext-form');
  el.classList.toggle('hidden', !show);
  if (show) document.getElementById('st-script').focus();
}

function clearAddSourceTextForm () {
  ['st-script', 'st-label', 'st-text'].forEach(id => { document.getElementById(id).value = ''; });
}

function nextSourceTextId () {
  const rows = (state.tables.source_texts && state.tables.source_texts.rows) || [];
  const maxId = rows.reduce((m, r) => {
    const n = parseInt(r.id, 10);
    return Number.isFinite(n) && n > m ? n : m;
  }, 0);
  return String(maxId + 1);
}

function submitAddSourceText () {
  const script = document.getElementById('st-script').value.trim();
  const label = document.getElementById('st-label').value.trim();
  const text = document.getElementById('st-text').value;
  if (!script || !text) {
    flash('Script and text are required.');
    return;
  }
  collectRowsFromDOM('source_texts'); // capture any in-progress edits in other rows first
  state.tables.source_texts.rows.push({ id: nextSourceTextId(), script, label, text });
  renderTable('source_texts');
  toggleAddSourceTextForm(false);
  clearAddSourceTextForm();
  flash(`Added "${label || script}" - click Save to persist.`);
}

function showLog (text) {
  const panel = document.getElementById('workbench-log');
  panel.textContent = text;
  panel.classList.remove('hidden');
}

function flash (msg) {
  showLog(msg);
}

function switchTab (tabName) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('active', b.dataset.tab === tabName));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.toggle('active', p.id === 'tab-' + tabName));
  if (tabName === 'postopts') renderOptionsGrouped('post');
  else if (tabName === 'preopts') renderOptionsGrouped('pre');
  else if (tabName === 'directopts') renderDirectOptions();
}

// ---------------------------------------------------------------------------
// Options Catalog: sortable / groupable / filterable.
// ---------------------------------------------------------------------------
const catalogState = { sortCol: 'name', sortDir: 'asc', groupByScript: false, missingOnly: false, frontendOnly: false, internalOnly: false, query: '' };

// backend_status is a static snapshot (only refreshed by "Regenerate from
// manifest") and even then only checks whether the option's name exists as
// a KEY in test_postoptions.json/test_preoptions.json - not whether it has
// any actual non-empty cases. So it never reflects cases added/removed
// through this workbench. Check the live data directly instead.
function hasTestData (row) {
  if (row.backend_status === 'working-multi-arg') {
    const key = row.kind + '::' + row.name;
    const entry = rawCases.direct && rawCases.direct[key];
    return !!(entry && (entry.cases || []).length > 0);
  }
  const blocks = (rawCases[row.kind] && rawCases[row.kind][row.name]) || [];
  return blocks.some(b => (b.cases || []).length > 0);
}

function catalogSortValue (row, col) {
  const v = row[col];
  if (col === 'in_frontend') return v === 'True' ? 1 : 0;
  return (v || '').toLowerCase();
}

function sortRows (rows) {
  const { sortCol, sortDir } = catalogState;
  const sorted = [...rows].sort((a, b) => {
    const av = catalogSortValue(a, sortCol), bv = catalogSortValue(b, sortCol);
    if (av < bv) return -1;
    if (av > bv) return 1;
    return 0;
  });
  if (sortDir === 'desc') sorted.reverse();
  return sorted;
}

function catalogRowHtml (row) {
  const cls = hasTestData(row) ? 'row-has-tests' : '';
  let tr = `<tr class="${cls}" data-kind="${escapeHtml(row.kind)}" data-name="${escapeHtml(row.name)}">`;
  for (const c of state.tables.options_catalog.columns) {
    const val = row[c] !== undefined ? row[c] : '';
    const cls2 = cellClass('options_catalog', c, val, row);
    tr += `<td class="readonly ${cls2}">${renderCellContent('options_catalog', c, val, row)}</td>`;
  }
  tr += `<td class="row-actions">
    <button class="btn btn-small btn-view-cases" data-kind="${escapeHtml(row.kind)}" data-name="${escapeHtml(row.name)}">cases</button>
    <button class="btn btn-small btn-add-test" data-kind="${escapeHtml(row.kind)}" data-name="${escapeHtml(row.name)}" data-scripts="${escapeHtml(row.applies_to_scripts)}">+ test</button>
  </td>`;
  tr += '</tr>';
  return tr;
}

async function toggleCaseDetail (tr, kind, name) {
  const next = tr.nextElementSibling;
  if (next && next.classList.contains('case-detail-row')) {
    next.remove();
    return;
  }
  const colCount = state.tables.options_catalog.columns.length + 1;
  const detailTr = document.createElement('tr');
  detailTr.className = 'case-detail-row';
  detailTr.innerHTML = `<td colspan="${colCount}">Loading...</td>`;
  tr.after(detailTr);

  try {
    const res = await api(`/api/option_cases?kind=${encodeURIComponent(kind)}&name=${encodeURIComponent(name)}`);
    detailTr.querySelector('td').innerHTML = renderCaseDetail(res);
  } catch (err) {
    detailTr.querySelector('td').innerHTML = `<span class="col-error">Failed to load: ${escapeHtml(err.message)}</span>`;
  }
}

function renderCaseDetail (res) {
  if (!res.found) {
    return '<span class="muted">No test data recorded for this option (matches backend_status = unknown-to-backend).</span>';
  }
  if (res.broken) {
    const b = res.broken;
    return `<div class="case-broken"><b>Broken</b> - tried as <code>${escapeHtml(b.source)} → ${escapeHtml(b.target)}</code>:
      <code>${escapeHtml(b.error_type)}: ${escapeHtml(b.error)}</code></div>`;
  }
  let html = `<div class="case-source muted">source: ${escapeHtml(res.source)}</div>`;
  for (const block of (res.blocks || [])) {
    const head = block.source
      ? `${escapeHtml(block.source)} → ${escapeHtml(block.target)}`
      : (block.args && block.args.length ? `direct call, extra args: ${escapeHtml(JSON.stringify(block.args))}` : 'direct call');
    html += `<div class="case-block"><div class="case-block-head">${head}</div>`;
    for (const pair of (block.cases || [])) {
      html += `<div class="case-pair"><span class="case-in">${escapeHtml(pair[0])}</span><span class="case-arrow">→</span><span class="case-out">${escapeHtml(pair[1])}</span></div>`;
    }
    html += '</div>';
  }
  return html;
}

function renderCatalog () {
  const { columns, rows } = state.tables.options_catalog;
  const el = document.getElementById('table-options_catalog');

  const q = catalogState.query.trim().toLowerCase();
  let filtered = rows.filter(r => {
    if (catalogState.missingOnly && hasTestData(r)) return false;
    if (catalogState.frontendOnly && r.in_frontend !== 'True') return false;
    if (catalogState.internalOnly && (r.in_frontend === 'True' || !internalOptionNeedsReview(r))) return false;
    if (!q) return true;
    return columns.some(c => String(r[c] || '').toLowerCase().includes(q));
  });

  let thead = '<thead><tr>';
  for (const c of columns) {
    const arrow = catalogState.sortCol === c ? (catalogState.sortDir === 'asc' ? '▲' : '▼') : '';
    thead += `<th class="sortable" data-sort-col="${c}">${c}${arrow ? ` <span class="sort-arrow">${arrow}</span>` : ''}</th>`;
  }
  thead += '<th></th></tr></thead>';

  let tbody = '<tbody>';
  if (catalogState.groupByScript) {
    const groups = {};
    for (const row of filtered) {
      const scripts = (row.applies_to_scripts || '').split(';').map(s => s.trim()).filter(Boolean);
      const keys = scripts.length ? scripts : ['(not in frontend / no script)'];
      for (const k of keys) {
        (groups[k] = groups[k] || []).push(row);
      }
    }
    const groupNames = Object.keys(groups).sort((a, b) => a.localeCompare(b));
    for (const g of groupNames) {
      tbody += `<tr class="group-header"><td colspan="${columns.length + 1}">${escapeHtml(g)} (${groups[g].length})</td></tr>`;
      for (const row of sortRows(groups[g])) tbody += catalogRowHtml(row);
    }
  } else {
    for (const row of sortRows(filtered)) tbody += catalogRowHtml(row);
  }
  tbody += '</tbody>';

  el.innerHTML = thead + tbody;
}

// An internal (in_frontend=False) option only belongs on the "needs review"
// filter if there's actually something to review: no real cases at all, or
// every case it does have still sits on the crude 'IAST' fallback the old
// generator used when it couldn't infer a real script from the option's
// name. An internal option that already has real, non-fallback cases (e.g.
// AhomClosed -> Ahom) is already correctly represented on the
// Post-options/Pre-options tab grouped under its real script - surfacing it
// here too would just be a duplicate listing.
function internalOptionNeedsReview (row) {
  const blocks = (rawCases[row.kind] && rawCases[row.kind][row.name]) || [];
  const scriptField = row.kind === 'post' ? 'target' : 'source';
  const hasConfirmedCase = blocks.some(b => (b.cases || []).length > 0 && b[scriptField] !== 'IAST');
  return !hasConfirmedCase;
}

// ---------------------------------------------------------------------------
// Option cases: direct browse/edit view over test_postoptions.json /
// test_preoptions.json / test_direct_options.json, split across three tabs
// (Post-options, Pre-options, Direct Options) instead of one flat table.
//
// Deliberately NOT flatten-then-reconstruct: rawCases holds exactly the
// object graph the server returned. View rows carry references (_casePair,
// _block/_entry) back into that same graph, so editing a cell or deleting a
// row mutates rawCases in place. "Save" posts rawCases back as-is - anything
// the UI never touched (a hand-written "comments" field, an empty-cases
// placeholder block, the "custom_call" marker) survives untouched. An
// earlier flatten/reconstruct version silently dropped exactly those three
// things; caught by diffing a no-op round-trip against git before saving
// anything for real.
// ---------------------------------------------------------------------------
let rawCases = { post: {}, pre: {}, direct: {} };
let currentCaseView = [];
const ALL_CASES_COLUMNS = ['kind', 'option_name', 'source_script', 'target_script', 'nativize', 'auto', 'args', 'input', 'output'];

let originalValues = new WeakMap();

// Note: script-family categorization (reversible/irreversible/roman/semitic)
// lives server-side now (app.py's _categorize_script) and only applies to
// conversion samples - option cases are grouped by individual script name
// instead, computed directly from source_script/target_script per row.

// Keyed by the live [input, output] _casePair array reference, not the
// wrapper row object - buildCaseViewRows() builds a FRESH wrapper object on
// every render call, but the underlying _casePair array is mutated in place
// (per the same "never reconstruct" principle as the rest of this section),
// so it's the only stable identity to track selection across re-renders.
let optionCasesSelected = new Set();

async function loadAllCases () {
  rawCases = await api('/api/all_cases');
  originalValues = new WeakMap();
  snapshotOriginals();
  optionCasesSelected.clear();
  renderOptionsGrouped('post');
  renderOptionsGrouped('pre');
  renderDirectOptions();
}

// Keyed by the live [input, output] array's object identity, which survives
// a move (attach/detach relocate the same array, never clone it) - so this
// doubles as "did the case's home change" tracking, not just its text: a
// kind/option_name/source/target/args edit is detected the same way an
// input/output edit is, by diffing current row fields against this snapshot.
// nativize is stored/edited as the STRING 'true'/'false' throughout the view
// layer (never a JS boolean) - cellPreviewHtml and friends do `val || ''`,
// which would silently render a real `false` as an empty cell.
function blockNativizeStr (block) {
  return String(block.nativize !== undefined ? block.nativize : true);
}

// Unlike nativize, missing 'auto' is genuinely unknown (predates this flag),
// not a safe default - so it's '' (blank), never the literal string 'false'.
function blockAutoStr (block) {
  return block.auto === true ? 'true' : '';
}

function snapshotOriginals () {
  for (const kind of ['post', 'pre']) {
    for (const name of Object.keys(rawCases[kind] || {})) {
      rawCases[kind][name].forEach(block => {
        (block.cases || []).forEach(pair => originalValues.set(pair, {
          input: pair[0], output: pair[1], kind, option_name: name,
          source_script: block.source || '', target_script: block.target || '',
          nativize: blockNativizeStr(block), auto: blockAutoStr(block), args: '',
        }));
      });
    }
  }
  for (const key of Object.keys(rawCases.direct || {})) {
    const entry = rawCases.direct[key];
    (entry.cases || []).forEach(pair => originalValues.set(pair, {
      input: pair[0], output: pair[1], kind: entry.kind, option_name: entry.name,
      source_script: '', target_script: '', nativize: '', auto: '', args: JSON.stringify(entry.args || []),
    }));
  }
}

function buildCaseViewRows () {
  const rows = [];
  for (const kind of ['post', 'pre']) {
    const working = rawCases[kind] || {};
    for (const name of Object.keys(working)) {
      working[name].forEach((block) => {
        (block.cases || []).forEach((casePair) => {
          rows.push(finishRow({
            shape: 'working', kind, option_name: name, source_script: block.source || '', target_script: block.target || '',
            nativize: blockNativizeStr(block), auto: blockAutoStr(block), args: '', input: casePair[0], output: casePair[1],
            _casePair: casePair, _container: block.cases, _block: block,
          }));
        });
      });
    }
  }
  const direct = rawCases.direct || {};
  for (const key of Object.keys(direct)) {
    const entry = direct[key];
    (entry.cases || []).forEach((casePair) => {
      rows.push(finishRow({
        shape: 'direct', kind: entry.kind, option_name: entry.name, source_script: '', target_script: '', nativize: '', auto: '',
        args: JSON.stringify(entry.args || []), input: casePair[0], output: casePair[1],
        _casePair: casePair, _container: entry.cases, _entry: entry,
      }));
    });
  }
  return rows;
}

const MOVE_FIELDS = new Set(['kind', 'option_name', 'source_script', 'target_script', 'nativize']);

function columnApplies (row, col) {
  if (col === 'args') return row.shape === 'direct';
  if (col === 'source_script' || col === 'target_script' || col === 'nativize' || col === 'auto') return row.shape === 'working';
  return true;
}

function detachCase (row) {
  const idx = row._container.indexOf(row._casePair);
  if (idx !== -1) row._container.splice(idx, 1);
  if (row.shape === 'working') {
    const blocks = rawCases[row.kind] && rawCases[row.kind][row.option_name];
    if (blocks) {
      if (row._block.cases.length === 0) {
        const bi = blocks.indexOf(row._block);
        if (bi !== -1) blocks.splice(bi, 1);
      }
      if (blocks.length === 0) delete rawCases[row.kind][row.option_name];
    }
  } else {
    const key = row.kind + '::' + row.option_name;
    if (row._entry.cases.length === 0) delete rawCases.direct[key];
  }
}

function attachWorkingCase (kind, name, source, target, nativizeBool, casePair) {
  const target_map = rawCases[kind] || (rawCases[kind] = {});
  const blocks = target_map[name] || (target_map[name] = []);
  // nativize is part of a block's identity: a block's cases are only
  // meaningful checked under the ONE nativize value that produced them.
  let block = blocks.find(b => (b.source || '') === source && (b.target || '') === target
    && (b.nativize !== undefined ? b.nativize : true) === nativizeBool);
  if (!block) { block = { source, target, nativize: nativizeBool, cases: [] }; blocks.push(block); }
  block.cases.push(casePair);
}

function attachDirectCase (kind, name, argsFromRow, casePair) {
  const key = kind + '::' + name;
  let entry = rawCases.direct[key];
  if (!entry) { entry = { kind, name, args: argsFromRow || [], cases: [] }; rawCases.direct[key] = entry; }
  entry.cases.push(casePair);
}

function updateCaseField (row, field, newValue) {
  if (field === 'input') { row._casePair[0] = newValue; return; }
  if (field === 'output') { row._casePair[1] = newValue; return; }

  if (field === 'args') {
    if (row.shape !== 'direct') return;
    try {
      row._entry.args = JSON.parse(newValue || '[]');
    } catch (e) {
      flash('Invalid JSON for args - not saved: ' + e.message);
    }
    return;
  }

  // 'auto' isn't part of a block's identity (unlike nativize), so editing it
  // - e.g. clearing it once you've reviewed a case - just mutates the block
  // directly, no detach/reattach needed.
  if (field === 'auto') {
    if (row.shape === 'working') row._block.auto = (newValue.trim() === 'true');
    return;
  }

  if (!MOVE_FIELDS.has(field)) return;
  const next = {
    kind: field === 'kind' ? newValue : row.kind,
    option_name: field === 'option_name' ? newValue : row.option_name,
    source_script: field === 'source_script' ? newValue : row.source_script,
    target_script: field === 'target_script' ? newValue : row.target_script,
    nativize: field === 'nativize' ? newValue : row.nativize,
  };
  if (!next.kind || !next.option_name) { flash('kind and option_name cannot be empty.'); return; }

  const casePair = row._casePair;
  detachCase(row);
  if (row.shape === 'working') attachWorkingCase(next.kind, next.option_name, next.source_script, next.target_script, next.nativize === 'true', casePair);
  else attachDirectCase(next.kind, next.option_name, row._entry ? row._entry.args : [], casePair);
}

function finishRow (row) {
  const orig = originalValues.get(row._casePair);
  row._isNew = !orig;
  row._original = orig || { input: '', output: '', kind: '', option_name: '', source_script: '', target_script: '', nativize: '', auto: '', args: '' };
  row._changed = row._isNew || ['input', 'output', 'kind', 'option_name', 'source_script', 'target_script', 'nativize', 'auto', 'args']
    .some(f => row._original[f] !== row[f]);
  return row;
}

// Re-renders whichever tab a given row belongs to, after an edit/delete
// that might have moved it (kind/option_name change) or changed its shape's
// home tab entirely (working <-> direct never happens via the UI, but
// working post <-> working pre does, via the kind field).
function rerenderOptionTab (row) {
  if (row.shape === 'direct') renderDirectOptions();
  else renderOptionsGrouped(row.kind);
}

const PREVIEW_LEN = 80;

// Only the first line, truncated, and NOT rendered as editable content by
// default - with hundreds of cases some of them full multi-paragraph texts,
// always rendering (and making editable) the full value in every cell was
// heavy on the page and made the tables hard to scan. Full text only loads
// into the DOM when you click a cell to edit it.
function cellPreviewHtml (val) {
  const str = String(val || '');
  const firstLine = str.split('\n')[0];
  const truncated = firstLine.length > PREVIEW_LEN ? firstLine.slice(0, PREVIEW_LEN) + '…' : firstLine;
  const hasMore = str.includes('\n') || str.length > PREVIEW_LEN;
  return `<div class="cell-preview" title="Click to edit">${escapeHtml(truncated) || '<span class="muted">(empty)</span>'}${hasMore ? ' <span class="more-indicator">⋯</span>' : ''}</div>`;
}

function textPreviewOnly (val) {
  const str = String(val || '');
  const firstLine = str.split('\n')[0];
  const truncated = firstLine.length > PREVIEW_LEN ? firstLine.slice(0, PREVIEW_LEN) + '…' : firstLine;
  const hasMore = str.includes('\n') || str.length > PREVIEW_LEN;
  return escapeHtml(truncated) + (hasMore ? ' <span class="more-indicator">⋯</span>' : '');
}

const MULTILINE_COLUMNS = new Set(['input', 'output']);

function expandCellForEdit (td) {
  const tr = td.closest('tr');
  const row = currentCaseView[parseInt(tr.dataset.vidx, 10)];
  if (!row) return;
  const col = td.dataset.col;
  const fullValue = row[col];
  if (MULTILINE_COLUMNS.has(col)) {
    td.innerHTML = `<textarea class="cell-edit-textarea" rows="6">${escapeHtml(fullValue)}</textarea>`;
  } else {
    td.innerHTML = `<input type="text" class="cell-edit-input" value="${escapeHtml(fullValue)}">`;
  }
  const field = td.querySelector('textarea, input');
  field.focus();
  if (field.setSelectionRange) field.setSelectionRange(field.value.length, field.value.length);
}

function collapseCellFromEdit (field) {
  const td = field.closest('td');
  const tr = td.closest('tr');
  const row = currentCaseView[parseInt(tr.dataset.vidx, 10)];
  if (row) {
    updateCaseField(row, td.dataset.col, field.value);
    rerenderOptionTab(row);
  }
}

// ---------------------------------------------------------------------------
// Word-level diff (LCS-based) for the "diff" button on a changed row.
// ---------------------------------------------------------------------------
function tokenizeForDiff (str) {
  return String(str).match(/\s+|[^\s]+/g) || [];
}

function computeWordDiff (oldStr, newStr) {
  const a = tokenizeForDiff(oldStr), b = tokenizeForDiff(newStr);
  const n = a.length, m = b.length;
  const dp = Array.from({ length: n + 1 }, () => new Uint32Array(m + 1));
  for (let i = n - 1; i >= 0; i--) {
    for (let j = m - 1; j >= 0; j--) {
      dp[i][j] = a[i] === b[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
    }
  }
  const ops = [];
  let i = 0, j = 0;
  while (i < n && j < m) {
    if (a[i] === b[j]) { ops.push(['same', a[i]]); i++; j++; }
    else if (dp[i + 1][j] >= dp[i][j + 1]) { ops.push(['del', a[i]]); i++; }
    else { ops.push(['ins', b[j]]); j++; }
  }
  while (i < n) { ops.push(['del', a[i]]); i++; }
  while (j < m) { ops.push(['ins', b[j]]); j++; }
  return ops;
}

function diffHtml (oldStr, newStr) {
  if (oldStr === newStr) return '<span class="muted">(unchanged)</span>';
  const ops = computeWordDiff(oldStr, newStr);
  let html = '';
  for (const [type, text] of ops) {
    const esc = escapeHtml(text);
    if (type === 'same') html += esc;
    else if (type === 'del') html += `<del>${esc}</del>`;
    else html += `<ins>${esc}</ins>`;
  }
  return html;
}

function toggleDiffRow (tr, row) {
  const next = tr.nextElementSibling;
  if (next && next.classList.contains('diff-row')) { next.remove(); return; }
  const colCount = ALL_CASES_COLUMNS.length + 3;
  const detailTr = document.createElement('tr');
  detailTr.className = 'diff-row';
  let body = row._isNew ? '<div class="diff-field-label" style="margin-bottom:8px">new case - nothing to diff against</div>' : '';
  for (const field of ['kind', 'option_name', 'source_script', 'target_script', 'nativize', 'auto', 'args', 'input', 'output']) {
    if (row._original[field] === row[field]) continue;
    body += `<div class="diff-field"><div class="diff-field-label">${field}</div><div class="diff-text">${diffHtml(row._original[field], row[field])}</div></div>`;
  }
  detailTr.innerHTML = `<td colspan="${colCount}">${body}</td>`;
  tr.after(detailTr);
}

// ---------------------------------------------------------------------------
// Row rendering shared by Post-options / Pre-options (grouped) and Direct
// Options (flat).
// ---------------------------------------------------------------------------
function optionRowHtml (row, i) {
  let tr = `<tr data-vidx="${i}" class="${row._changed ? 'row-changed' : ''}">`;
  tr += `<td><input type="checkbox" class="row-select option-row-select" data-option-vidx="${i}" ${optionCasesSelected.has(row._casePair) ? 'checked' : ''}></td>`;
  tr += optionStatusCellHtml(row, i);
  for (const c of ALL_CASES_COLUMNS) {
    const val = row[c] !== undefined ? row[c] : '';
    const badge = (c === 'option_name' && row._changed)
      ? `<span class="changed-badge" title="${row._isNew ? 'New, not yet saved' : 'Edited, not yet saved'}"></span>` : '';
    if (!columnApplies(row, c)) {
      tr += `<td class="readonly not-applicable" title="Not applicable to this option">${badge}—</td>`;
    } else {
      tr += `<td data-col="${c}">${badge}${cellPreviewHtml(val)}</td>`;
    }
  }
  tr += `<td>`;
  if (row._changed) tr += `<button class="btn btn-small btn-diff" data-testdata-diff="${i}">diff</button>`;
  tr += `<button class="btn-remove-row" data-testdata-remove="${i}" title="Delete this case">✕</button></td>`;
  tr += '</tr>';
  return tr;
}

function optionsTheadHtml (view) {
  const allChecked = view.length > 0 && view.every(row => optionCasesSelected.has(row._casePair));
  let thead = `<thead><tr><th><input type="checkbox" class="option-select-all" ${allChecked ? 'checked' : ''}></th><th></th>`;
  for (const c of ALL_CASES_COLUMNS) thead += `<th>${c}</th>`;
  thead += `<th>${view.length} case${view.length === 1 ? '' : 's'}</th></tr></thead>`;
  return thead;
}

function updateOptionSelectionUI () {
  document.querySelectorAll('[data-option-delete-selected]').forEach(btn => {
    btn.textContent = `Delete selected (${optionCasesSelected.size})`;
    btn.disabled = optionCasesSelected.size === 0;
  });
}

function deleteSelectedOptionCases () {
  if (optionCasesSelected.size === 0) return;
  const toDelete = buildCaseViewRows().filter(r => optionCasesSelected.has(r._casePair));
  toDelete.forEach(row => detachCase(row));
  optionCasesSelected.clear();
  renderOptionsGrouped('post');
  renderOptionsGrouped('pre');
  renderDirectOptions();
}

function renderOptionsGrouped (kind) {
  const tableId = kind === 'post' ? 'table-postopts' : 'table-preopts';
  const filterEl = document.getElementById(kind === 'post' ? 'postopts-filter' : 'preopts-filter');
  const el = document.getElementById(tableId);
  if (!el) return;

  const q = (filterEl && filterEl.value || '').trim().toLowerCase();
  const allRows = buildCaseViewRows().filter(r => r.kind === kind && r.shape === 'working');
  const filtered = allRows
    .filter(r => !q || ALL_CASES_COLUMNS.some(c => String(r[c] || '').toLowerCase().includes(q)))
    .filter(r => {
      if (!showOnlyFailed || !runResultIndex) return true;
      const result = lookupOptionRunResult(r);
      return result && !result.ok;
    })
    .filter(r => !hideAutoGenerated || r.auto !== 'true');

  const groupKeyCol = kind === 'post' ? 'target_script' : 'source_script';
  const groups = {};
  for (const r of filtered) {
    const key = r[groupKeyCol] || '(none)';
    (groups[key] = groups[key] || []).push(r);
  }
  const groupNames = Object.keys(groups).sort((a, b) => a.localeCompare(b));

  const view = [];
  let tbody = '<tbody>';
  for (const g of groupNames) {
    tbody += `<tr class="group-header"><td colspan="${ALL_CASES_COLUMNS.length + 3}">${escapeHtml(g)} (${groups[g].length})</td></tr>`;
    for (const row of groups[g]) {
      const i = view.length;
      view.push(row);
      tbody += optionRowHtml(row, i);
    }
  }
  tbody += '</tbody>';

  currentCaseView = view;
  el.innerHTML = optionsTheadHtml(view) + tbody;
  updateOptionSelectionUI();
}

function renderDirectOptions () {
  const el = document.getElementById('table-directopts');
  if (!el) return;
  const filterEl = document.getElementById('directopts-filter');
  const q = (filterEl && filterEl.value || '').trim().toLowerCase();

  const allRows = buildCaseViewRows().filter(r => r.shape === 'direct');
  const filtered = allRows.filter(r => !q || ALL_CASES_COLUMNS.some(c => String(r[c] || '').toLowerCase().includes(q)));

  currentCaseView = filtered;
  let tbody = '<tbody>';
  filtered.forEach((row, i) => { tbody += optionRowHtml(row, i); });
  tbody += '</tbody>';
  el.innerHTML = optionsTheadHtml(filtered) + tbody;
  updateOptionSelectionUI();
}

function toggleAddCaseForm (show) {
  const el = document.getElementById('add-case-form');
  el.classList.toggle('hidden', !show);
  if (show) {
    populateOptionNameDatalist();
    document.getElementById('add-case-name').focus();
  }
}

function populateOptionNameDatalist () {
  const dl = document.getElementById('option-name-list');
  const catalogRows = (state.tables.options_catalog && state.tables.options_catalog.rows) || [];
  const names = [...new Set(catalogRows.map(r => r.name))].sort();
  dl.innerHTML = names.map(n => `<option value="${escapeHtml(n)}">`).join('');
}

function clearAddCaseForm () {
  ['add-case-name', 'add-case-source', 'add-case-target', 'add-case-input', 'add-case-output']
    .forEach(id => { document.getElementById(id).value = ''; });
  document.getElementById('add-case-nativize').checked = true;
}

async function autogenerateAddCaseOutput () {
  const kind = document.getElementById('add-case-kind').value;
  const name = document.getElementById('add-case-name').value.trim();
  const source = document.getElementById('add-case-source').value.trim();
  const target = document.getElementById('add-case-target').value.trim();
  const input = document.getElementById('add-case-input').value;
  const nativize = document.getElementById('add-case-nativize').checked;
  if (!name || !source || !target || !input) {
    flash('Fill in option name, source, target and input first.');
    return;
  }
  const res = await api('/api/preview_option_case', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ kind, name, source, target, input, nativize })
  });
  if (res.ok) {
    document.getElementById('add-case-output').value = res.output;
    flash('Autogenerated output - review it before clicking Add case.');
  } else {
    flash('Autogenerate failed: ' + (res.error || ''));
  }
}

function submitAddCase () {
  const kind = document.getElementById('add-case-kind').value;
  const name = document.getElementById('add-case-name').value.trim();
  const source = document.getElementById('add-case-source').value.trim();
  const target = document.getElementById('add-case-target').value.trim();
  const input = document.getElementById('add-case-input').value;
  const output = document.getElementById('add-case-output').value;
  const nativize = document.getElementById('add-case-nativize').checked;

  if (!name || !input) {
    flash('Option name and input are required.');
    return;
  }

  attachWorkingCase(kind, name, source, target, nativize, [input, output]);

  toggleAddCaseForm(false);
  clearAddCaseForm();
  renderOptionsGrouped(kind);
  flash(`Added a new case for ${kind}::${name} (${source || '?'} → ${target || '?'}, nativize=${nativize}) - shown as "new" until you Save.`);
}

function addOptionTestFromCatalog (kind, name, scriptsCsv) {
  const firstScript = (scriptsCsv || '').split(';')[0].trim();
  toggleAddCaseForm(true);
  document.getElementById('add-case-kind').value = kind;
  document.getElementById('add-case-name').value = name;
  document.getElementById('add-case-source').value = kind === 'pre' ? firstScript : 'Devanagari';
  document.getElementById('add-case-target').value = kind === 'post' ? firstScript : 'Devanagari';
  switchTab(kind === 'post' ? 'postopts' : 'preopts');
}

async function saveAllCases () {
  const res = await api('/api/all_cases', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(rawCases)
  });
  if (res.ok) {
    originalValues = new WeakMap();
    snapshotOriginals();
    renderOptionsGrouped('post');
    renderOptionsGrouped('pre');
    renderDirectOptions();
  }
  flash(res.ok ? 'Saved test data.' : 'Save failed.');
}

async function generateOptionCoverageFromRow (kind, idx) {
  const rows = collectRowsFromDOM('source_texts');
  const row = rows[idx];
  if (!row || (row.script || '').trim() !== 'Devanagari' || !row.text) {
    flash('Option coverage needs a Devanagari row with text.');
    return;
  }
  showLog(`Generating full ${kind}-option coverage from "${row.label || row.script}" (every applicable script, nativize=true)...`);
  const res = await api('/api/generate_option_cases', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ kind, text: row.text })
  });
  showLog(res.ok ? `Added ${res.added} new cases. See the ${kind === 'post' ? 'Post-options' : 'Pre-options'} tab.` : ('Generation failed: ' + (res.error || '')));
  await loadAllCases();
}

// ---------------------------------------------------------------------------
// Conversion samples: baseline (no-option) script->script conversions,
// bulk-generated from Source Texts, viewed/edited across 5 tabs by script
// family. Editable field is `output` only - source/target/nativize/mode are
// a property of how a row was generated, not something to hand-move.
// ---------------------------------------------------------------------------
let conversionSamples = [];
let convOriginal = new WeakMap();
const CONV_COLUMNS = ['source', 'target', 'nativize', 'mode', 'label', 'auto', 'input', 'output'];
// Row objects are stable between renders (mutated in place, never recreated)
// EXCEPT when the whole array is replaced by a fresh load - cleared there.
let convSelected = new Set();

async function loadConversionSamples () {
  const res = await api('/api/conversion_samples');
  conversionSamples = res.rows;
  convOriginal = new WeakMap();
  for (const r of conversionSamples) convOriginal.set(r, { output: r.output });
  convSelected.clear();
  renderAllConvTables();
}

function renderAllConvTables () {
  document.querySelectorAll('.table-conv').forEach(table => renderConvTable(table.dataset.category));
}

function convCellHtml (col, val) {
  if (col === 'output') return `<td data-conv-col="output">${cellPreviewHtml(val)}</td>`;
  if (col === 'input') return `<td class="readonly">${textPreviewOnly(val)}</td>`;
  if (col === 'nativize') {
    const boolVal = val === true || val === 'True';
    return `<td class="readonly ${boolVal ? 'col-bool-true' : 'col-bool-false'}">${val === '' || val === undefined ? '' : String(boolVal)}</td>`;
  }
  if (col === 'auto') {
    // undefined predates this flag (e.g. the heart/lalitavistara import) -
    // shown blank, not "false", since we don't actually know it was manual.
    if (val !== true) return `<td class="readonly"></td>`;
    return `<td class="readonly col-bool-true">auto</td>`;
  }
  return `<td class="readonly">${escapeHtml(val)}</td>`;
}

function getVisibleConvRows (category) {
  const el = document.querySelector(`.table-conv[data-category="${category}"]`);
  const panel = el ? el.closest('.tab-panel') : null;
  const filterEl = panel ? panel.querySelector('.conv-filter') : null;
  const q = (filterEl && filterEl.value || '').trim().toLowerCase();

  return conversionSamples
    .map((r, gi) => ({ r, gi }))
    .filter(({ r }) => r.category === category)
    .filter(({ r }) => !q || CONV_COLUMNS.some(c => String(r[c] || '').toLowerCase().includes(q)))
    .filter(({ r }) => {
      if (!showOnlyFailed || !runResultIndex) return true;
      const { fwd, rt } = lookupConvRunResults(r);
      return (fwd && !fwd.ok) || (rt && !rt.ok);
    })
    .filter(({ r }) => !hideAutoGenerated || r.auto !== true);
}

function updateConvSelectionUI () {
  document.querySelectorAll('[data-conv-delete-selected]').forEach(btn => {
    btn.textContent = `Delete selected (${convSelected.size})`;
    btn.disabled = convSelected.size === 0;
  });
}

function renderConvTable (category) {
  const el = document.querySelector(`.table-conv[data-category="${category}"]`);
  if (!el) return;

  const rows = getVisibleConvRows(category);
  const allChecked = rows.length > 0 && rows.every(({ r }) => convSelected.has(r));

  let thead = `<thead><tr><th><input type="checkbox" class="conv-select-all" data-conv-cat="${category}" ${allChecked ? 'checked' : ''}></th><th></th><th title="Round trip (nativize=false, reversible targets only)">↺</th>` +
    CONV_COLUMNS.map(c => `<th>${c}</th>`).join('') +
    `<th>${rows.length} row${rows.length === 1 ? '' : 's'}</th></tr></thead>`;

  let tbody = '<tbody>';
  rows.forEach(({ r, gi }, i) => {
    const orig = convOriginal.get(r);
    const changed = orig && orig.output !== r.output;
    const rowClass = r.error ? 'row-error' : (changed ? 'row-changed' : '');
    tbody += `<tr class="${rowClass}" data-conv-gi="${gi}" data-conv-idx="${i}" data-conv-cat="${category}">`;
    tbody += `<td><input type="checkbox" class="row-select conv-row-select" data-conv-select-gi="${gi}" ${convSelected.has(r) ? 'checked' : ''}></td>`;
    tbody += convForwardStatusCellHtml(r, gi);
    tbody += convRoundtripStatusCellHtml(r, gi);
    for (const c of CONV_COLUMNS) tbody += convCellHtml(c, r[c]);
    tbody += `<td><button class="btn-remove-row" data-conv-remove="${gi}" title="Delete this sample">✕</button></td>`;
    tbody += '</tr>';
  });
  tbody += '</tbody>';
  el.innerHTML = thead + tbody;
  updateConvSelectionUI();
}

function deleteSelectedConvSamples () {
  if (convSelected.size === 0) return;
  conversionSamples = conversionSamples.filter(r => !convSelected.has(r));
  convSelected.clear();
  renderAllConvTables();
}

function expandConvCellForEdit (td) {
  const tr = td.closest('tr');
  const gi = parseInt(tr.dataset.convGi, 10);
  const row = conversionSamples[gi];
  if (!row) return;
  td.innerHTML = `<textarea class="cell-edit-textarea" rows="4">${escapeHtml(row.output)}</textarea>`;
  const ta = td.querySelector('textarea');
  ta.focus();
  ta.setSelectionRange(ta.value.length, ta.value.length);
}

function collapseConvCellFromEdit (textarea) {
  const td = textarea.closest('td');
  const tr = td.closest('tr');
  const gi = parseInt(tr.dataset.convGi, 10);
  const row = conversionSamples[gi];
  if (row) row.output = textarea.value;
  renderConvTable(tr.dataset.convCat);
}

async function saveConversionSamples () {
  const res = await api('/api/conversion_samples', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ rows: conversionSamples })
  });
  if (res.ok) {
    convOriginal = new WeakMap();
    for (const r of conversionSamples) convOriginal.set(r, { output: r.output });
    renderAllConvTables();
  }
  flash(res.ok ? 'Saved conversion samples.' : 'Save failed.');
}

// Single-pair form: generate just one source -> target instead of a full
// fanout, e.g. Arabic -> Hebrew without also touching the other ~150 scripts.
function toggleAddPairForm (show, rowIdx) {
  const el = document.getElementById('add-pair-form');
  el.classList.toggle('hidden', !show);
  if (show) {
    const rows = collectRowsFromDOM('source_texts');
    const row = rows[rowIdx];
    el.dataset.rowIdx = rowIdx;
    document.getElementById('pair-source-label').value = `${row.script} - "${row.label || ''}"`;
    document.getElementById('add-pair-target').value = '';
    document.getElementById('add-pair-target').focus();
  }
}

async function submitAddPair () {
  const el = document.getElementById('add-pair-form');
  const idx = parseInt(el.dataset.rowIdx, 10);
  const rows = collectRowsFromDOM('source_texts');
  const row = rows[idx];
  const target = document.getElementById('add-pair-target').value.trim();
  if (!row || !target) { flash('Pick a target script.'); return; }

  showLog(`Generating ${row.script} → ${target}...`);
  const res = await api('/api/generate_conversion_samples', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ script: row.script, text: row.text, label: row.label, target })
  });
  showLog(res.ok ? `Generated/updated ${res.generated_or_updated} record(s). See the conversion tabs.` : ('Generation failed: ' + (res.error || '')));
  toggleAddPairForm(false);
  await loadConversionSamples();
}

async function generateConversionSamplesFromRow (mode, idx) {
  const rows = collectRowsFromDOM('source_texts');
  const row = rows[idx];
  if (!row || !row.script || !row.text) {
    flash('Row needs a script and text before generating.');
    return;
  }
  showLog(`Generating conversion samples (${mode}) from "${row.label || row.script}"...`);
  const res = await api('/api/generate_conversion_samples', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mode, script: row.script, text: row.text, label: row.label })
  });
  showLog(res.ok ? `Generated/updated ${res.generated_or_updated} records (${res.total} total). See the conversion tabs.` : ('Generation failed: ' + (res.error || '')));
  await loadConversionSamples();
}

// ---------------------------------------------------------------------------
// Custom Cases: a full transliterate.process() call - source, target,
// nativize, and any combination of pre_options/post_options together, for
// what the single-option tabs can't express. A flat list of plain objects
// (test_custom_cases.json), edited by mutating rows in place by array
// index - no block/entry grouping to keep consistent, so no move semantics
// needed, unlike the option-cases grid.
// ---------------------------------------------------------------------------
let customCases = [];
let ccOriginal = new WeakMap();
const CC_COLUMNS = ['label', 'source', 'target', 'nativize', 'pre_options', 'post_options', 'input', 'output'];
const CC_MULTILINE = new Set(['input', 'output']);
let customSelected = new Set();

async function loadCustomCases () {
  const res = await api('/api/custom_cases');
  customCases = res.rows;
  ccOriginal = new WeakMap();
  for (const r of customCases) ccOriginal.set(r, JSON.stringify(r));
  customSelected.clear();
  renderCustomCases();
}

function ccFieldText (row, col) {
  if (col === 'pre_options' || col === 'post_options') return (row[col] || []).join(';');
  if (col === 'nativize') return String(row.nativize !== undefined ? row.nativize : true);
  return row[col] || '';
}

function ccCellHtml (row, col) {
  return `<td data-col="${col}">${cellPreviewHtml(ccFieldText(row, col))}</td>`;
}

function getVisibleCustomCaseRows () {
  const filterEl = document.getElementById('customcases-filter');
  const q = (filterEl && filterEl.value || '').trim().toLowerCase();

  return customCases
    .map((r, gi) => ({ r, gi }))
    .filter(({ r }) => !q || CC_COLUMNS.some(c => ccFieldText(r, c).toLowerCase().includes(q)))
    .filter(({ gi }) => {
      if (!showOnlyFailed || !runResultIndex) return true;
      const result = runResultIndex.custom.get(gi);
      return result && !result.ok;
    });
}

function renderCustomCases () {
  const el = document.getElementById('table-customcases');
  if (!el) return;
  const rows = getVisibleCustomCaseRows();

  const allChecked = rows.length > 0 && rows.every(({ r }) => customSelected.has(r));
  let thead = `<thead><tr><th><input type="checkbox" class="cc-select-all" ${allChecked ? 'checked' : ''}></th><th></th>` +
    CC_COLUMNS.map(c => `<th>${c}</th>`).join('') +
    `<th>${rows.length} case${rows.length === 1 ? '' : 's'}</th></tr></thead>`;

  let tbody = '<tbody>';
  rows.forEach(({ r, gi }) => {
    const changed = ccOriginal.get(r) !== JSON.stringify(r);
    tbody += `<tr class="${changed ? 'row-changed' : ''}" data-cc-idx="${gi}">`;
    tbody += `<td><input type="checkbox" class="row-select cc-row-select" data-cc-select-gi="${gi}" ${customSelected.has(r) ? 'checked' : ''}></td>`;
    tbody += customStatusCellHtml(gi);
    for (const c of CC_COLUMNS) tbody += ccCellHtml(r, c);
    tbody += `<td><button class="btn-remove-row" data-cc-remove="${gi}" title="Delete this case">✕</button></td>`;
    tbody += '</tr>';
  });
  tbody += '</tbody>';
  el.innerHTML = thead + tbody;
  updateCustomSelectionUI();
}

function updateCustomSelectionUI () {
  document.querySelectorAll('[data-cc-delete-selected]').forEach(btn => {
    btn.textContent = `Delete selected (${customSelected.size})`;
    btn.disabled = customSelected.size === 0;
  });
}

function deleteSelectedCustomCases () {
  if (customSelected.size === 0) return;
  customCases = customCases.filter(r => !customSelected.has(r));
  customSelected.clear();
  renderCustomCases();
}

function expandCcCellForEdit (td) {
  const tr = td.closest('tr');
  const gi = parseInt(tr.dataset.ccIdx, 10);
  const row = customCases[gi];
  if (!row) return;
  const col = td.dataset.col;
  const val = ccFieldText(row, col);
  if (CC_MULTILINE.has(col)) {
    td.innerHTML = `<textarea class="cell-edit-textarea" rows="6">${escapeHtml(val)}</textarea>`;
  } else {
    td.innerHTML = `<input type="text" class="cell-edit-input" value="${escapeHtml(val)}">`;
  }
  const field = td.querySelector('textarea, input');
  field.focus();
  if (field.setSelectionRange) field.setSelectionRange(field.value.length, field.value.length);
}

function collapseCcCellFromEdit (field) {
  const td = field.closest('td');
  const tr = td.closest('tr');
  const gi = parseInt(tr.dataset.ccIdx, 10);
  const row = customCases[gi];
  if (!row) return;
  const col = td.dataset.col;
  const newValue = field.value;
  if (col === 'pre_options' || col === 'post_options') {
    row[col] = newValue.split(';').map(s => s.trim()).filter(Boolean);
  } else if (col === 'nativize') {
    row[col] = newValue.trim() === 'true';
  } else {
    row[col] = newValue;
  }
  renderCustomCases();
}

async function saveCustomCases () {
  const res = await api('/api/custom_cases', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ rows: customCases })
  });
  if (res.ok) {
    ccOriginal = new WeakMap();
    for (const r of customCases) ccOriginal.set(r, JSON.stringify(r));
    renderCustomCases();
  }
  flash(res.ok ? 'Saved custom cases.' : 'Save failed.');
}

function toggleAddCustomCaseForm (show) {
  const el = document.getElementById('add-customcase-form');
  el.classList.toggle('hidden', !show);
  if (show) {
    populatePrePostOptionDatalists();
    document.getElementById('cc-source').focus();
  }
}

function populatePrePostOptionDatalists () {
  const catalogRows = (state.tables.options_catalog && state.tables.options_catalog.rows) || [];
  const preNames = [...new Set(catalogRows.filter(r => r.kind === 'pre').map(r => r.name))].sort();
  const postNames = [...new Set(catalogRows.filter(r => r.kind === 'post').map(r => r.name))].sort();
  document.getElementById('pre-option-name-list').innerHTML = preNames.map(n => `<option value="${escapeHtml(n)}">`).join('');
  document.getElementById('post-option-name-list').innerHTML = postNames.map(n => `<option value="${escapeHtml(n)}">`).join('');
}

function clearAddCustomCaseForm () {
  ['cc-source', 'cc-target', 'cc-label', 'cc-pre-options', 'cc-post-options', 'cc-input', 'cc-output']
    .forEach(id => { document.getElementById(id).value = ''; });
  document.getElementById('cc-nativize').checked = true;
}

function readCustomCaseForm () {
  return {
    source: document.getElementById('cc-source').value.trim(),
    target: document.getElementById('cc-target').value.trim(),
    nativize: document.getElementById('cc-nativize').checked,
    label: document.getElementById('cc-label').value.trim(),
    pre_options: document.getElementById('cc-pre-options').value.split(';').map(s => s.trim()).filter(Boolean),
    post_options: document.getElementById('cc-post-options').value.split(';').map(s => s.trim()).filter(Boolean),
    input: document.getElementById('cc-input').value,
  };
}

async function autogenerateCustomCaseOutput () {
  const form = readCustomCaseForm();
  if (!form.source || !form.target || !form.input) {
    flash('Fill in source, target and input first.');
    return;
  }
  const res = await api('/api/preview_custom_case', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form)
  });
  if (res.ok) {
    document.getElementById('cc-output').value = res.output;
    flash('Autogenerated output - review it before clicking Add case.');
  } else {
    flash('Autogenerate failed: ' + (res.error || ''));
  }
}

function submitAddCustomCase () {
  const form = readCustomCaseForm();
  const output = document.getElementById('cc-output').value;
  if (!form.source || !form.target || !form.input) {
    flash('Source, target and input are required.');
    return;
  }
  customCases.push({ ...form, output });
  toggleAddCustomCaseForm(false);
  clearAddCustomCaseForm();
  renderCustomCases();
  flash(`Added a new custom case (${form.source} → ${form.target}) - shown as "changed" until you Save.`);
}

// ---------------------------------------------------------------------------
// Run All Tests: recomputes every stored case live (post/pre-options,
// custom cases, conversion samples, round-trips) via /api/run_all_tests.
// Results are NOT shown as their own separate table - they're matched back
// onto the existing rows on the tabs where that data already lives (the 5
// conversion tabs, Post-options, Pre-options, Custom Cases), as a status
// column with a tick or a click-to-expand cross, using diffHtml (the same
// word-level diff already built for the option-cases "diff" button). Only
// the summary counts get their own small panel.
// ---------------------------------------------------------------------------
const RUN_CATEGORY_LABELS = { post: 'Post-options', pre: 'Pre-options', custom: 'Custom cases', conversion: 'Conversion samples', roundtrip: 'Round-trips' };
// null = no run yet (status columns render blank); otherwise
// { conv: Map<key,result>, roundtrip: Map<key,result>, post: Map<key,result>, pre: Map<key,result>, custom: Map<index,result> }
let runResultIndex = null;
// Global "show only failed" toggle - applies across every tab that has a
// status column (conversion tabs, Post-options, Pre-options, Custom Cases),
// not per-tab, so switching tabs doesn't lose the filter.
let showOnlyFailed = false;
// Global "hide auto-generated" toggle - hides rows/blocks tagged auto:true
// (conversion tabs, Post-options, Pre-options). Not applied to Custom Cases
// or Direct Options - neither has ever had a bulk generator, so everything
// there is already manual by construction.
let hideAutoGenerated = false;

function convKey (source, target, nativize, label) { return `${source}|${target}|${nativize}|${label || ''}`; }
function roundtripKey (source, target, label) { return `${source}|${target}|${label || ''}`; }
function optionResultKey (kind, name, source, target, nativize, input) { return `${kind}|${name}|${source}|${target}|${nativize}|${input}`; }

function buildRunResultIndex (results) {
  const idx = { conv: new Map(), roundtrip: new Map(), post: new Map(), pre: new Map(), custom: new Map() };
  for (const r of results) {
    if (r.category === 'conversion') idx.conv.set(convKey(r.source, r.target, r.nativize, r.label), r);
    else if (r.category === 'roundtrip') idx.roundtrip.set(roundtripKey(r.source, r.target, r.label), r);
    else if (r.category === 'post' || r.category === 'pre') {
      idx[r.category].set(optionResultKey(r.category, r.option_name, r.source, r.target, r.nativize, r.input), r);
    } else if (r.category === 'custom') idx.custom.set(r.index, r);
  }
  return idx;
}

function runStatusTick (failed, toggleAttrs) {
  if (!failed) return '<td class="readonly rr-tick" title="Passed">✓</td>';
  return `<td><span class="rr-cross" ${toggleAttrs} title="Click to see the diff">✗</span></td>`;
}

function diffFieldsHtml (result, label) {
  let body = '';
  if (result.error) body += `<div class="diff-field"><div class="diff-field-label">error</div><div class="diff-text col-error">${escapeHtml(result.error)}</div></div>`;
  body += `<div class="diff-field"><div class="diff-field-label">${label}</div><div class="diff-text">${diffHtml(result.expected, result.actual)}</div></div>`;
  return body;
}

function toggleDetailRow (tr, colspan, bodyHtml) {
  const next = tr.nextElementSibling;
  if (next && next.classList.contains('diff-row')) { next.remove(); return; }
  const detailTr = document.createElement('tr');
  detailTr.className = 'diff-row';
  detailTr.innerHTML = `<td colspan="${colspan}">${bodyHtml}</td>`;
  tr.after(detailTr);
}

// --- conversion samples (also covers the derived round-trip check) ---
function lookupConvRunResults (r) {
  if (!runResultIndex) return {};
  const fwd = runResultIndex.conv.get(convKey(r.source, r.target, r.nativize, r.label));
  const rt = r.nativize === false ? runResultIndex.roundtrip.get(roundtripKey(r.source, r.target, r.label)) : undefined;
  return { fwd, rt };
}

// Two separate columns, not one combined tick - a reversible-script row has
// two independent things that can fail (the forward conversion, and the
// round trip back), and collapsing them into a single mark hid which one.
function convForwardStatusCellHtml (r, gi) {
  if (!runResultIndex) return '<td class="readonly"></td>';
  const { fwd } = lookupConvRunResults(r);
  if (!fwd) return '<td class="readonly" title="Not checked in the last run"></td>';
  return runStatusTick(!fwd.ok, `data-run-status-toggle="conv" data-run-status-gi="${gi}"`);
}

function convRoundtripStatusCellHtml (r, gi) {
  if (r.nativize !== false) return '<td class="readonly not-applicable" title="Round trip is only checked at nativize=false">—</td>';
  if (!runResultIndex) return '<td class="readonly"></td>';
  const { rt } = lookupConvRunResults(r);
  if (!rt) return '<td class="readonly" title="Not a reversible target, or not checked in the last run"></td>';
  return runStatusTick(!rt.ok, `data-run-status-toggle="conv" data-run-status-gi="${gi}"`);
}

function toggleConvRunStatusDetail (tr, gi) {
  const r = conversionSamples[gi];
  if (!r) return;
  const { fwd, rt } = lookupConvRunResults(r);
  let body = '';
  if (fwd && !fwd.ok) body += diffFieldsHtml(fwd, 'expected → actual');
  if (rt && !rt.ok) body += diffFieldsHtml(rt, 'round trip: original input → what came back');
  toggleDetailRow(tr, CONV_COLUMNS.length + 3, body);
}

// --- post/pre options ---
function lookupOptionRunResult (row) {
  if (!runResultIndex || row.shape !== 'working') return undefined;
  return runResultIndex[row.kind].get(optionResultKey(row.kind, row.option_name, row.source_script, row.target_script, row.nativize, row.input));
}

function optionStatusCellHtml (row, i) {
  if (row.shape !== 'working' || !runResultIndex) return '<td class="readonly"></td>';
  const result = lookupOptionRunResult(row);
  if (!result) return '<td class="readonly" title="Not checked in the last run"></td>';
  return runStatusTick(!result.ok, `data-run-status-toggle="option" data-run-status-idx="${i}"`);
}

function toggleOptionRunStatusDetail (tr, row) {
  const result = lookupOptionRunResult(row);
  if (!result) return;
  toggleDetailRow(tr, ALL_CASES_COLUMNS.length + 3, diffFieldsHtml(result, 'expected → actual'));
}

// --- custom cases ---
function customStatusCellHtml (gi) {
  if (!runResultIndex) return '<td class="readonly"></td>';
  const result = runResultIndex.custom.get(gi);
  if (!result) return '<td class="readonly" title="Not checked in the last run"></td>';
  return runStatusTick(!result.ok, `data-run-status-toggle="custom" data-run-status-gi="${gi}"`);
}

function toggleCustomRunStatusDetail (tr, gi) {
  const result = runResultIndex && runResultIndex.custom.get(gi);
  if (!result) return;
  toggleDetailRow(tr, CC_COLUMNS.length + 2, diffFieldsHtml(result, 'expected → actual'));
}

function rrPillHtml (label, passed, total, extraClass) {
  const cls = passed < total ? 'rr-bad' : 'rr-ok';
  return `<span class="rr-pill ${extraClass || ''}">
    <span class="rr-pill-label">${escapeHtml(label)}</span>
    <span class="rr-pill-count ${cls}">${passed}/${total}</span>
  </span>`;
}

function renderRunSummary (summary) {
  const summaryEl = document.getElementById('run-results-summary');
  let totalChecked = 0;
  let totalPassed = 0;
  let pillsHtml = '';
  for (const key of ['post', 'pre', 'custom', 'conversion', 'roundtrip']) {
    const s = summary[key];
    if (!s) continue;
    const passed = s.total - s.mismatches;
    totalChecked += s.total;
    totalPassed += passed;
    pillsHtml += rrPillHtml(RUN_CATEGORY_LABELS[key], passed, s.total);
  }
  summaryEl.innerHTML = rrPillHtml('Overall', totalPassed, totalChecked, 'rr-pill-total') + pillsHtml;
  document.getElementById('run-results-panel').classList.remove('hidden');
}

async function runAllTests () {
  const btn = document.getElementById('run-all-tests');
  btn.disabled = true;
  btn.textContent = 'Running…';
  try {
    const res = await api('/api/run_all_tests', { method: 'POST' });
    if (!res.ok) { flash('Run failed.'); return; }
    runResultIndex = buildRunResultIndex(res.results);
    renderRunSummary(res.summary);
    renderAllConvTables();
    renderOptionsGrouped('post');
    renderOptionsGrouped('pre');
    renderCustomCases();
  } catch (e) {
    flash('Run failed: ' + e.message);
  } finally {
    btn.disabled = false;
    btn.textContent = 'Run All Tests';
  }
}

// ---------------------------------------------------------------------------
// Event delegation
// ---------------------------------------------------------------------------
document.addEventListener('click', async (e) => {
  const t = e.target;
  if (t.dataset.tab) switchTab(t.dataset.tab);
  if (t.dataset.add) addRow(t.dataset.add);
  if (t.dataset.save) await saveTable(t.dataset.save);
  if (t.dataset.remove) {
    const [tbl, idx] = t.dataset.remove.split(':');
    removeRow(tbl, parseInt(idx, 10));
  }
  if (t.hasAttribute('data-regen-catalog')) {
    showLog('Regenerating catalog...');
    const res = await api('/api/regenerate_catalog', { method: 'POST' });
    showLog(res.log);
    await loadTable('options_catalog');
  }
  if (t.classList.contains('btn-add-test')) {
    addOptionTestFromCatalog(t.dataset.kind, t.dataset.name, t.dataset.scripts);
  }
  if (t.classList.contains('btn-view-cases')) {
    await toggleCaseDetail(t.closest('tr'), t.dataset.kind, t.dataset.name);
  }
  if (t.classList.contains('cell-preview')) {
    const td = t.closest('td');
    if (td.closest('table') && td.closest('table').id === 'table-customcases') expandCcCellForEdit(td);
    else if (td.hasAttribute('data-conv-col')) expandConvCellForEdit(td);
    else expandCellForEdit(td);
  }
  if (t.classList.contains('sortable') || t.closest('.sortable')) {
    const th = t.classList.contains('sortable') ? t : t.closest('.sortable');
    if (th.dataset.sortCol) {
      const col = th.dataset.sortCol;
      if (catalogState.sortCol === col) catalogState.sortDir = catalogState.sortDir === 'asc' ? 'desc' : 'asc';
      else { catalogState.sortCol = col; catalogState.sortDir = 'asc'; }
      renderCatalog();
    }
  }
  if (t.dataset.testdataRemove !== undefined) {
    const row = currentCaseView[parseInt(t.dataset.testdataRemove, 10)];
    if (row) {
      const idx = row._container.indexOf(row._casePair);
      if (idx !== -1) row._container.splice(idx, 1);
      rerenderOptionTab(row);
    }
  }
  if (t.dataset.testdataDiff !== undefined) {
    const row = currentCaseView[parseInt(t.dataset.testdataDiff, 10)];
    if (row) toggleDiffRow(t.closest('tr'), row);
  }
  if (t.dataset.convRemove !== undefined) {
    const gi = parseInt(t.dataset.convRemove, 10);
    const row = conversionSamples[gi];
    if (row) {
      conversionSamples.splice(gi, 1);
      renderAllConvTables();
    }
  }
  if (t.dataset.ccRemove !== undefined) {
    const gi = parseInt(t.dataset.ccRemove, 10);
    if (customCases[gi]) {
      customCases.splice(gi, 1);
      renderCustomCases();
    }
  }
  if (t.dataset.saveCases === 'custom') {
    await saveCustomCases();
  } else if (t.hasAttribute('data-save-cases')) {
    await saveAllCases();
  }
  if (t.hasAttribute('data-option-delete-selected')) {
    deleteSelectedOptionCases();
  }
  if (t.hasAttribute('data-cc-delete-selected')) {
    deleteSelectedCustomCases();
  }
  if (t.hasAttribute('data-st-delete-selected')) {
    deleteSelectedSourceTexts();
  }
  if (t.hasAttribute('data-save-conv')) {
    await saveConversionSamples();
  }
  if (t.hasAttribute('data-conv-delete-selected')) {
    deleteSelectedConvSamples();
  }
  if (t.id === 'add-customcase') {
    toggleAddCustomCaseForm(true);
  }
  if (t.id === 'cc-cancel') {
    toggleAddCustomCaseForm(false);
    clearAddCustomCaseForm();
  }
  if (t.id === 'cc-submit') {
    submitAddCustomCase();
  }
  if (t.id === 'cc-autogen') {
    await autogenerateCustomCaseOutput();
  }
  if (t.id === 'run-all-tests') {
    await runAllTests();
  }
  if (t.id === 'run-results-close') {
    document.getElementById('run-results-panel').classList.add('hidden');
  }
  if (t.dataset.runStatusToggle === 'conv') {
    toggleConvRunStatusDetail(t.closest('tr'), parseInt(t.dataset.runStatusGi, 10));
  }
  if (t.dataset.runStatusToggle === 'option') {
    const row = currentCaseView[parseInt(t.dataset.runStatusIdx, 10)];
    if (row) toggleOptionRunStatusDetail(t.closest('tr'), row);
  }
  if (t.dataset.runStatusToggle === 'custom') {
    toggleCustomRunStatusDetail(t.closest('tr'), parseInt(t.dataset.runStatusGi, 10));
  }
  if (t.dataset.srcGen) {
    await generateConversionSamplesFromRow(t.dataset.srcGen, parseInt(t.dataset.rowIdx, 10));
  }
  if (t.dataset.srcGenOpts) {
    await generateOptionCoverageFromRow(t.dataset.srcGenOpts, parseInt(t.dataset.rowIdx, 10));
  }
  if (t.hasAttribute('data-src-pair')) {
    toggleAddPairForm(true, parseInt(t.dataset.rowIdx, 10));
  }
  if (t.id === 'add-pair-cancel') {
    toggleAddPairForm(false);
  }
  if (t.id === 'add-pair-submit') {
    await submitAddPair();
  }
  if (t.id === 'add-sourcetext') {
    toggleAddSourceTextForm(true);
  }
  if (t.id === 'st-cancel') {
    toggleAddSourceTextForm(false);
    clearAddSourceTextForm();
  }
  if (t.id === 'st-submit') {
    submitAddSourceText();
  }
  if (t.id === 'add-case-autogen') {
    await autogenerateAddCaseOutput();
  }
  if (t.hasAttribute('data-add-case')) {
    toggleAddCaseForm(true);
  }
  if (t.id === 'add-case-cancel') {
    toggleAddCaseForm(false);
    clearAddCaseForm();
  }
  if (t.id === 'add-case-submit') {
    submitAddCase();
  }
});

document.addEventListener('input', (e) => {
  if (e.target.id === 'catalog-filter') {
    catalogState.query = e.target.value;
    renderCatalog();
  }
  if (e.target.id === 'postopts-filter') renderOptionsGrouped('post');
  if (e.target.id === 'preopts-filter') renderOptionsGrouped('pre');
  if (e.target.id === 'directopts-filter') renderDirectOptions();
  if (e.target.id === 'customcases-filter') renderCustomCases();
  if (e.target.classList.contains('conv-filter')) {
    const panel = e.target.closest('.tab-panel');
    const table = panel && panel.querySelector('.table-conv');
    if (table) renderConvTable(table.dataset.category);
  }
});

// 'focusout' (bubbles) rather than 'blur' (doesn't) so this can be a single
// delegated listener instead of one per field.
document.addEventListener('focusout', (e) => {
  if (e.target.classList.contains('cell-edit-textarea') || e.target.classList.contains('cell-edit-input')) {
    const td = e.target.closest('td');
    if (td.closest('table') && td.closest('table').id === 'table-customcases') collapseCcCellFromEdit(e.target);
    else if (td.hasAttribute('data-conv-col')) collapseConvCellFromEdit(e.target);
    else collapseCellFromEdit(e.target);
  }
});

document.addEventListener('change', (e) => {
  if (e.target.classList.contains('conv-select-all')) {
    const category = e.target.dataset.convCat;
    const checked = e.target.checked;
    getVisibleConvRows(category).forEach(({ r }) => { if (checked) convSelected.add(r); else convSelected.delete(r); });
    const table = e.target.closest('table');
    if (table) table.querySelectorAll('.conv-row-select').forEach(cb => { cb.checked = checked; });
    updateConvSelectionUI();
  }
  if (e.target.classList.contains('conv-row-select')) {
    const gi = parseInt(e.target.dataset.convSelectGi, 10);
    const r = conversionSamples[gi];
    if (r) { if (e.target.checked) convSelected.add(r); else convSelected.delete(r); }
    updateConvSelectionUI();
  }
  if (e.target.classList.contains('option-select-all')) {
    const checked = e.target.checked;
    currentCaseView.forEach(row => { if (checked) optionCasesSelected.add(row._casePair); else optionCasesSelected.delete(row._casePair); });
    const table = e.target.closest('table');
    if (table) table.querySelectorAll('.option-row-select').forEach(cb => { cb.checked = checked; });
    updateOptionSelectionUI();
  }
  if (e.target.classList.contains('option-row-select')) {
    const vidx = parseInt(e.target.dataset.optionVidx, 10);
    const row = currentCaseView[vidx];
    if (row) { if (e.target.checked) optionCasesSelected.add(row._casePair); else optionCasesSelected.delete(row._casePair); }
    updateOptionSelectionUI();
  }
  if (e.target.classList.contains('cc-select-all')) {
    const checked = e.target.checked;
    getVisibleCustomCaseRows().forEach(({ r }) => { if (checked) customSelected.add(r); else customSelected.delete(r); });
    document.querySelectorAll('.cc-row-select').forEach(cb => { cb.checked = checked; });
    updateCustomSelectionUI();
  }
  if (e.target.classList.contains('cc-row-select')) {
    const gi = parseInt(e.target.dataset.ccSelectGi, 10);
    const r = customCases[gi];
    if (r) { if (e.target.checked) customSelected.add(r); else customSelected.delete(r); }
    updateCustomSelectionUI();
  }
  if (e.target.classList.contains('st-select-all')) {
    const checked = e.target.checked;
    (state.tables.source_texts.rows || []).forEach(r => { if (checked) sourceTextsSelected.add(r.id); else sourceTextsSelected.delete(r.id); });
    document.querySelectorAll('.st-row-select').forEach(cb => { cb.checked = checked; });
    updateSourceTextsSelectionUI();
  }
  if (e.target.classList.contains('st-row-select')) {
    const i = parseInt(e.target.dataset.stSelectI, 10);
    const row = (state.tables.source_texts.rows || [])[i];
    if (row) { if (e.target.checked) sourceTextsSelected.add(row.id); else sourceTextsSelected.delete(row.id); }
    updateSourceTextsSelectionUI();
  }
  if (e.target.id === 'show-only-failed') {
    showOnlyFailed = e.target.checked;
    renderAllConvTables();
    renderOptionsGrouped('post');
    renderOptionsGrouped('pre');
    renderCustomCases();
  }
  if (e.target.id === 'hide-auto-generated') {
    hideAutoGenerated = e.target.checked;
    renderAllConvTables();
    renderOptionsGrouped('post');
    renderOptionsGrouped('pre');
  }
  if (e.target.id === 'catalog-group-toggle') {
    catalogState.groupByScript = e.target.checked;
    renderCatalog();
  }
  if (e.target.id === 'catalog-missing-toggle') {
    catalogState.missingOnly = e.target.checked;
    renderCatalog();
  }
  if (e.target.id === 'catalog-frontend-toggle') {
    catalogState.frontendOnly = e.target.checked;
    if (catalogState.frontendOnly) {
      catalogState.internalOnly = false;
      document.getElementById('catalog-internal-toggle').checked = false;
    }
    renderCatalog();
  }
  if (e.target.id === 'catalog-internal-toggle') {
    catalogState.internalOnly = e.target.checked;
    if (catalogState.internalOnly) {
      catalogState.frontendOnly = false;
      document.getElementById('catalog-frontend-toggle').checked = false;
    }
    renderCatalog();
  }
  if (e.target.id === 'add-case-kind') {
    // fill in the side that's a fixed default for this kind (post options
    // default to a Devanagari source, pre options to a Devanagari target)
    // so the field you actually need to think about is the only blank one
    const sourceEl = document.getElementById('add-case-source');
    const targetEl = document.getElementById('add-case-target');
    if (e.target.value === 'post' && !sourceEl.value) sourceEl.value = 'Devanagari';
    if (e.target.value === 'pre' && !targetEl.value) targetEl.value = 'Devanagari';
  }
});

(async function init () {
  await loadAllCases();
  await loadConversionSamples();
  await loadCustomCases();
  for (const name of ['source_texts', 'options_catalog']) {
    await loadTable(name);
  }
})();
