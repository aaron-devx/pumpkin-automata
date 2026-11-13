import { MACHINES, getMachine } from './machines.js';
import { run } from './simulator.js';

const machineSelect = document.getElementById('machine');
const inputEl = document.getElementById('input');
const runBtn = document.getElementById('run');
const verdictEl = document.getElementById('verdict');
const reasonEl = document.getElementById('reason');
const traceBody = document.getElementById('trace-body');
const metaEl = document.getElementById('meta');
const examplesEl = document.getElementById('examples');

function fillMachines() {
  for (const m of MACHINES) {
    const opt = document.createElement('option');
    opt.value = m.id;
    opt.textContent = `${m.kind}: ${m.label.replace(/^DFA — |^NFA — /, '')}`;
    machineSelect.appendChild(opt);
  }
}

function renderMeta(id) {
  const m = getMachine(id);
  metaEl.innerHTML = `
    <p class="muted"><strong>${m.label}</strong><span class="badge">${m.kind}</span></p>
    <p class="muted">Σ = {${m.alphabet.join(', ')}} · start <code>${m.start}</code> · F = {${m.accept.join(', ')}}</p>
    <p class="muted">${m.source ?? ''}</p>
  `;
  examplesEl.textContent = exampleFor(id);
}

function exampleFor(id) {
  const map = {
    'dfa-starts-0': 'Try: 010 ✓, 100 ✓, 1 ✗',
    'dfa-ends-10': 'Try: 10 ✓, 1010 ✓, 11 ✗',
    'dfa-has-bab': 'Try: bab ✓, abab ✓, bbb ✗',
    'dfa-len-3': 'Try: aba ✓, ab ✗, abab ✗',
    'nfa-ends-aab': 'Try: aab ✓, baab ✓, aa ✗',
    'nfa-has-0101': 'Try: 0101 ✓, 00101 ✓, 010 ✗',
  };
  return map[id] ?? '';
}

function renderTrace(machine, result) {
  traceBody.replaceChildren();
  const rows = result.trace;
  for (const row of rows) {
    const tr = document.createElement('tr');
    const stateCell =
      machine.kind === 'DFA'
        ? row.state
        : (row.states ?? []).join(', ') || '∅';
    tr.innerHTML = `<td>${row.step}</td><td><code>${row.read || 'ε'}</code></td><td><code>${stateCell}</code></td><td>${row.note}</td>`;
    traceBody.appendChild(tr);
  }
}

function execute() {
  const m = getMachine(machineSelect.value);
  const input = inputEl.value;
  const result = run(m, input);
  verdictEl.className = 'verdict';
  if (!result.ok) {
    verdictEl.textContent = 'INVALID';
    verdictEl.classList.add('invalid');
  } else if (result.accepted) {
    verdictEl.textContent = 'ACCEPTED';
    verdictEl.classList.add('accept');
  } else {
    verdictEl.textContent = 'REJECTED';
    verdictEl.classList.add('reject');
  }
  reasonEl.textContent = result.reason;
  renderTrace(m, result);
}

fillMachines();
renderMeta(machineSelect.value);
machineSelect.addEventListener('change', () => renderMeta(machineSelect.value));
runBtn.addEventListener('click', execute);
inputEl.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') execute();
});
