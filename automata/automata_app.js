import { MACHINES, getMachine } from './machines.js';
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

function renderDiagram(m, active) {
  const svg = els.diagram();
  if (!svg) return;
  const states = machineStates(m);
  const w = 520;
  const h = 120;
  const pad = 36;
  const step = states.length > 1 ? (w - pad * 2) / (states.length - 1) : 0;
  const nodes = states
    .map((q, i) => {
      const x = pad + step * i;
      const y = h / 2;
      const on = active.includes(q);
      const acc = m.accept.includes(q);
      const r = acc ? 22 : 18;
      const fill = on ? '#f58a45' : acc ? '#55b45c' : '#e9f7ff';
      const stroke = on ? '#0d2230' : '#14425b';
      return `<g><circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" stroke="${stroke}" stroke-width="2"/><text x="${x}" y="${y + 5}" text-anchor="middle" font-size="12" fill="#0d2230" font-family="Poppins,sans-serif">${q}</text></g>`;
    })
    .join('');
  svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
  svg.innerHTML = nodes;
}

function syncStepControls(max) {
  const range = els.stepRange();
  const label = els.stepLabel();
  if (!range) return;
  range.min = '0';
  range.max = String(Math.max(0, max));
  range.value = String(stepIndex);
  if (label) label.textContent = `Step ${stepIndex} / ${max}`;
}

function highlightStep() {
  if (!session) return;
  const { machine, result } = session;
  const row = result.trace[stepIndex];
  const active =
    machine.kind === 'DFA'
      ? row && row.state
        ? [row.state]
        : []
      : row && row.states
        ? row.states
        : [];
  renderDiagram(machine, active);
  els.traceBody()?.querySelectorAll('tr').forEach((tr, i) => {
    tr.classList.toggle('on', i === stepIndex);
  });
  syncStepControls(result.trace.length - 1);
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

function bind() {
  fillMachines();
  const sel = els.machine();
  sel?.addEventListener('change', () => {
    renderTransitionTable(getMachine(sel.value));
    renderDiagram(getMachine(sel.value), [getMachine(sel.value).start]);
  });
  if (sel) {
    const m = getMachine(sel.value);
    renderTransitionTable(m);
    renderDiagram(m, [m.start]);
  }

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
