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
      const mark = q === m.start ? '→' : m.accept.includes(q) ? '*' : '';
      return `<tr><td>${mark}${q}</td>${cells.map((c) => `<td>${c}</td>`).join('')}</tr>`;
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

function edgePath(x1, y1, x2, y2) {
  const mx = (x1 + x2) / 2;
  const my = (y1 + y2) / 2 - 18;
  return `M ${x1} ${y1} Q ${mx} ${my} ${x2} ${y2}`;
}

function renderDiagram(m, active, prev, hotChar) {
  const svg = els.diagram();
  if (!svg) return;
  const edges = layoutEdges(m);
  const w = m.layout?.width ?? 420;
  const h = m.layout?.height ?? 160;
  const edgeSvg = edges
    .map(({ from, to, sym }) => {
      const a = nodePos(m, from);
      const b = nodePos(m, to);
      const on =
        hotChar === sym &&
        ((prev.includes(from) && active.includes(to)) ||
          (from === to && active.includes(from) && prev.includes(from)));
      const stroke = on ? '#f58a45' : '#94a8b5';
      const sw = on ? 3.2 : 1.6;
      const d = edgePath(a.x, a.y, b.x, b.y);
      const lx = (a.x + b.x) / 2;
      const ly = (a.y + b.y) / 2 - 22;
      return `<path d="${d}" fill="none" stroke="${stroke}" stroke-width="${sw}"/><text x="${lx}" y="${ly}" text-anchor="middle" font-size="11" fill="${on ? '#f58a45' : '#5a6b75'}" font-family="Poppins,sans-serif">${sym}</text>`;
    })
    .join('');
  const nodes = machineStates(m)
    .map((id) => {
      const { x, y } = nodePos(m, id);
      const on = active.includes(id);
      const acc = m.accept.includes(id);
      const r = acc ? 22 : 18;
      const fill = on ? '#f58a45' : acc ? '#55b45c' : '#e9f7ff';
      const stroke = on ? '#0d2230' : '#14425b';
      const ring = acc ? `<circle cx="${x}" cy="${y}" r="${r + 5}" fill="none" stroke="#55b45c" stroke-width="2"/>` : '';
      return `<g>${ring}<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" stroke="${stroke}" stroke-width="2"/><text x="${x}" y="${y + 4}" text-anchor="middle" font-size="12" fill="#0d2230" font-family="Poppins,sans-serif">${id}</text></g>`;
    })
    .join('');
  svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
  svg.innerHTML = `${edgeSvg}${nodes}`;
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

  if (scrollToLab) {
    document.getElementById('lab')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

function selectMachine(id) {
  const m = getMachine(id);
  renderTransitionTable(m);
  renderSamples(m);
  renderDiagram(m, [m.start], [m.start], '');
}

function bindCards() {
  document.querySelectorAll('.card[data-machine]').forEach((card) => {
    card.addEventListener('click', () => {
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

function bind() {
  fillMachines();
  bindCards();
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
