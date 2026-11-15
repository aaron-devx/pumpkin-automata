import { MACHINES, getMachine, layoutEdges } from './machines.js';
import { run } from './simulator.js';

/** @type {{ machine: import('./machines.js').Machine, result: ReturnType<typeof run> } | null} */
let session = null;
let stepIndex = 0;

const els = {
  machine: () => document.getElementById('machine-select'),
  input: () => document.getElementById('string-input'),
  verdict: () => document.getElementById('lab-verdict'),
  reason: () => document.getElementById('lab-reason'),
  traceBody: () => document.getElementById('trace-body'),
  stepRange: () => document.getElementById('step-range'),
  stepLabel: () => document.getElementById('step-label'),
  table: () => document.getElementById('transition-table'),
  diagram: () => document.getElementById('state-diagram'),
  machineNote: () => document.getElementById('machine-note'),
  samples: () => document.getElementById('sample-chips'),
};

function fillMachines() {
  const sel = els.machine();
  if (!sel) return;
  sel.replaceChildren();
  for (const m of MACHINES) {
    const opt = document.createElement('option');
    opt.value = m.id;
    opt.textContent = `${m.kind}: ${m.label.replace(/^DFA — |^NFA — /, '')}`;
    sel.appendChild(opt);
  }
}

function machineStates(m) {
  const set = new Set([m.start, ...m.accept]);
  for (const key of Object.keys(m.transitions)) {
    const [q] = key.split(',');
    set.add(q);
    const v = m.transitions[key];
    const list = Array.isArray(v) ? v : [v];
    list.forEach((t) => set.add(t));
  }
  return [...set].sort();
}

function renderSamples(m) {
  const box = els.samples();
  if (!box) return;
  box.replaceChildren();
  const title = document.createElement('span');
  title.className = 'muted';
  title.textContent = 'Try:';
  box.appendChild(title);
  for (const { s, hint } of m.samples ?? []) {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'chip';
    btn.title = hint;
    btn.textContent = s;
    btn.addEventListener('click', () => {
      const input = els.input();
      if (input) input.value = s;
      execute(true);
    });
    box.appendChild(btn);
  }
}

function stateMarks(m, q) {
  const start = q === m.start ? '<span class="mark" role="img" aria-label="start state">→</span>' : '';
  const accept = m.accept.includes(q) ? '<span class="mark" role="img" aria-label="accept state">*</span>' : '';
  return `${start}${accept}`;
}

function renderTransitionTable(m) {
  const wrap = els.table();
  if (!wrap) return;
  const states = machineStates(m);
  const hdr = `<tr><th>δ</th>${m.alphabet.map((a) => `<th>${a}</th>`).join('')}</tr>`;
  const rows = states
    .map((q) => {
      const cells = m.alphabet.map((a) => {
        const v = m.transitions[`${q},${a}`];
        if (!v) return '∅';
        return Array.isArray(v) ? `{${v.join(',')}}` : v;
      });
      return `<tr><td>${stateMarks(m, q)}${q}</td>${cells.map((c) => `<td>${c}</td>`).join('')}</tr>`;
    })
    .join('');
  wrap.innerHTML = `<table class="delta">${hdr}${rows}</table>`;
}

function nodePos(m, id) {
  const hit = m.layout?.nodes.find((n) => n.id === id);
  if (hit) return hit;
  const states = machineStates(m);
  const i = states.indexOf(id);
  return { id, x: 40 + i * 72, y: 70 };
}

const NODE_R = 18;
const ACC_R = 22;
const LOOP_RISE = 34;
const LOOP_HALF = 14;
const ADJ_BEND = 36;
const LONG_BEND_MAX = 100;
const LONG_BEND_RATIO = 0.45;
const LABEL_GAP = 10;
const ARROW_PAD = 4;
const COLOR_IDLE = '#94a8b5';
const COLOR_HOT = '#f58a45';

function groupEdges(m) {
  const map = new Map();
  for (const { from, to, sym } of layoutEdges(m)) {
    const k = `${from}|${to}`;
    const cur = map.get(k) ?? { from, to, syms: [] };
    map.set(k, { ...cur, syms: [...cur.syms, sym] });
  }
  return [...map.values()];
}

function radiusOf(m, id) {
  return m.accept.includes(id) ? ACC_R + 5 : NODE_R;
}

function loopGeometry(m, id, h) {
  const { x, y } = nodePos(m, id);
  const r = radiusOf(m, id);
  const dir = y <= h / 2 ? -1 : 1;
  const y0 = y + dir * r;
  const yc = y0 + dir * LOOP_RISE * 1.35;
  return {
    d: `M ${x - LOOP_HALF} ${y0} C ${x - LOOP_HALF * 2.2} ${yc}, ${x + LOOP_HALF * 2.2} ${yc}, ${x + LOOP_HALF} ${y0}`,
    end: { x: x + LOOP_HALF, y: y0 },
    lx: x,
    ly: y0 + dir * (LOOP_RISE * 1.0 + LABEL_GAP) + 4,
  };
}

function curveGeometry(m, from, to) {
  const a = nodePos(m, from);
  const b = nodePos(m, to);
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  const len = Math.hypot(dx, dy) || 1;
  const nx = dy / len;
  const ny = -dx / len;
  const isLong = len > 150;
  const bend = isLong ? Math.min(LONG_BEND_MAX, len * LONG_BEND_RATIO) : ADJ_BEND;
  const cx = (a.x + b.x) / 2 + nx * bend;
  const cy = (a.y + b.y) / 2 + ny * bend;
  const tx = b.x - cx;
  const ty = b.y - cy;
  const tl = Math.hypot(tx, ty) || 1;
  const pad = radiusOf(m, to) + ARROW_PAD;
  const ex = b.x - (tx / tl) * pad;
  const ey = b.y - (ty / tl) * pad;
  const sx = a.x + ((cx - a.x) / (Math.hypot(cx - a.x, cy - a.y) || 1)) * radiusOf(m, from);
  const sy = a.y + ((cy - a.y) / (Math.hypot(cx - a.x, cy - a.y) || 1)) * radiusOf(m, from);
  const mx = 0.25 * sx + 0.5 * cx + 0.25 * ex;
  const my = 0.25 * sy + 0.5 * cy + 0.25 * ey;
  return { d: `M ${sx} ${sy} Q ${cx} ${cy} ${ex} ${ey}`, lx: mx + nx * LABEL_GAP, ly: my + ny * LABEL_GAP + 4 };
}

function arrowMarker(id, color) {
  return `<marker id="${id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="${color}"/></marker>`;
}

function renderDiagram(m, active, prev, hotChar) {
  const svg = els.diagram();
  if (!svg) return;
  const w = m.layout?.width ?? 420;
  const h = m.layout?.height ?? 160;
  const edgeSvg = groupEdges(m)
    .map(({ from, to, syms }) => {
      const loop = from === to;
      const on =
        syms.includes(hotChar) &&
        ((prev.includes(from) && active.includes(to)) || (loop && active.includes(from) && prev.includes(from)));
      const geo = loop ? loopGeometry(m, from, h) : curveGeometry(m, from, to);
      const stroke = on ? COLOR_HOT : COLOR_IDLE;
      const sw = on ? 3.2 : 1.6;
      const mk = on ? 'url(#ah-hot)' : 'url(#ah-idle)';
      return `<path d="${geo.d}" fill="none" stroke="${stroke}" stroke-width="${sw}" marker-end="${mk}"/><text x="${geo.lx}" y="${geo.ly}" text-anchor="middle" font-size="11" fill="${on ? COLOR_HOT : '#5a6b75'}" font-family="Poppins,sans-serif">${syms.join(',')}</text>`;
    })
    .join('');
  const nodes = machineStates(m)
    .map((id) => {
      const { x, y } = nodePos(m, id);
      const on = active.includes(id);
      const acc = m.accept.includes(id);
      const r = acc ? ACC_R : NODE_R;
      const fill = on ? '#f58a45' : acc ? '#55b45c' : '#e9f7ff';
      const stroke = on ? '#0d2230' : '#14425b';
      const ring = acc ? `<circle cx="${x}" cy="${y}" r="${r + 5}" fill="none" stroke="#55b45c" stroke-width="2"/>` : '';
      const entry = id === m.start ? `<path d="M ${x - r - 26} ${y} L ${x - r - 4} ${y}" stroke="${COLOR_IDLE}" stroke-width="1.6" marker-end="url(#ah-idle)"/>` : '';
      return `<g>${entry}${ring}<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" stroke="${stroke}" stroke-width="2"/><text x="${x}" y="${y + 4}" text-anchor="middle" font-size="12" fill="#0d2230" font-family="Poppins,sans-serif">${id}</text></g>`;
    })
    .join('');
  svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
  svg.innerHTML = `<defs>${arrowMarker('ah-idle', COLOR_IDLE)}${arrowMarker('ah-hot', COLOR_HOT)}</defs>${edgeSvg}${nodes}`;
}

function syncStepControls(max) {
  const range = els.stepRange();
  const label = els.stepLabel();
  if (!range) return;
  range.min = '0';
  range.max = String(Math.max(0, max));
  range.value = String(stepIndex);
  range.disabled = max === 0;
  if (label) label.textContent = `Step ${stepIndex} / ${max}`;
}

function prevStates(machine, row, prevRow) {
  if (machine.kind === 'DFA') {
    if (!prevRow) return row?.state ? [machine.start] : [];
    return prevRow.state ? [prevRow.state] : [];
  }
  if (!prevRow) return [machine.start];
  return prevRow.states ?? [];
}

function highlightStep() {
  if (!session) return;
  const { machine, result } = session;
  const row = result.trace[stepIndex];
  const prevRow = stepIndex > 0 ? result.trace[stepIndex - 1] : null;
  const active =
    machine.kind === 'DFA'
      ? row && row.state
        ? [row.state]
        : [machine.start]
      : row && row.states
        ? row.states
        : [machine.start];
  const prev = prevStates(machine, row, prevRow);
  const hotChar = row?.char ?? '';
  renderDiagram(machine, active, prev, hotChar);
  els.traceBody()?.querySelectorAll('tr').forEach((tr, i) => {
    tr.classList.toggle('on', i === stepIndex);
  });
  syncStepControls(result.trace.length - 1);
  revealActiveRow();
}

function revealActiveRow() {
  const row = els.traceBody()?.querySelector('tr.on');
  const panel = row?.closest('.lab-trace');
  if (!row || !panel) return;
  const head = panel.querySelector('thead')?.offsetHeight ?? 0;
  const p = panel.getBoundingClientRect();
  const r = row.getBoundingClientRect();
  const delta = r.top < p.top + head ? r.top - p.top - head : r.bottom > p.bottom ? r.bottom - p.bottom : 0;
  if (delta !== 0) panel.scrollTop += delta;
}

function renderTrace(machine, result) {
  const body = els.traceBody();
  if (!body) return;
  body.replaceChildren();
  result.trace.forEach((row, i) => {
    const tr = document.createElement('tr');
    const stateCell =
      machine.kind === 'DFA' ? row.state : (row.states ?? []).join(', ') || '∅';
    tr.innerHTML = `<td>${row.step}</td><td><code>${row.read || 'ε'}</code></td><td><code>${stateCell}</code></td><td>${row.note}</td>`;
    tr.addEventListener('click', () => {
      stepIndex = i;
      highlightStep();
    });
    body.appendChild(tr);
  });
}

function scrollToId(id, focus = false) {
  const el = document.getElementById(id);
  if (!el) return;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
  if (focus) el.focus({ preventScroll: true });
}

function execute(scrollToLab) {
  const m = getMachine(els.machine()?.value ?? MACHINES[0].id);
  const input = els.input()?.value ?? '';
  const result = run(m, input);
  session = { machine: m, result };
  stepIndex = 0;

  const v = els.verdict();
  const r = els.reason();
  if (v) {
    v.className = 'lab-verdict';
    if (!result.ok) {
      v.textContent = 'INVALID';
      v.classList.add('invalid');
    } else if (result.accepted) {
      v.textContent = 'ACCEPTED';
      v.classList.add('accept');
    } else {
      v.textContent = 'REJECTED';
      v.classList.add('reject');
    }
  }
  if (r) r.textContent = result.reason;

  const note = els.machineNote();
  if (note) {
    note.innerHTML = `<strong>${m.label}</strong> · Σ={${m.alphabet.join(',')}} · F={${m.accept.join(',')}} · <span class="muted">${m.source ?? ''}</span>`;
  }

  renderTransitionTable(m);
  renderTrace(m, result);
  highlightStep();

  if (scrollToLab) scrollToId('lab-title', true);
}

function selectMachine(id) {
  const m = getMachine(id);
  renderTransitionTable(m);
  renderSamples(m);
  renderDiagram(m, [m.start], [m.start], '');
}

function bindCards() {
  document.querySelectorAll('.card[data-machine], .tcard[data-machine], .feat-go[data-machine]').forEach((card) => {
    // Flip cards: only the back's "Try" button loads the lab; the rest of the card flips.
    const target = card.matches('.card') ? card.querySelector('.card-go') : card;
    target?.addEventListener('click', () => {
      const sel = els.machine();
      const input = els.input();
      if (!sel || !input) return;
      sel.value = card.dataset.machine;
      sel.dispatchEvent(new Event('change'));
      input.value = card.dataset.input ?? '';
      execute(true);
    });
  });
}

function bindScrollButtons() {
  document.querySelectorAll('[data-scroll]').forEach((btn) => {
    btn.addEventListener('click', () => scrollToId(btn.dataset.scroll, true));
  });
}

function bind() {
  fillMachines();
  bindCards();
  bindScrollButtons();
  const sel = els.machine();
  sel?.addEventListener('change', () => selectMachine(sel.value));
  if (sel) selectMachine(sel.value);

  document.getElementById('run-hero')?.addEventListener('click', () => execute(true));
  document.getElementById('run-lab')?.addEventListener('click', () => execute(false));
  els.input()?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') execute(true);
  });

  document.getElementById('step-prev')?.addEventListener('click', () => {
    if (!session) return;
    stepIndex = Math.max(0, stepIndex - 1);
    highlightStep();
  });
  document.getElementById('step-next')?.addEventListener('click', () => {
    if (!session) return;
    stepIndex = Math.min(session.result.trace.length - 1, stepIndex + 1);
    highlightStep();
  });
  els.stepRange()?.addEventListener('input', (e) => {
    if (!session) return;
    stepIndex = Number(e.target.value);
    highlightStep();
  });
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', bind);
else bind();
