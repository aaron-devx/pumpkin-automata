/**
 * @param {import('./machines.js').Machine} machine
 * @param {string} input
 */
export function run(machine, input) {
  if (machine.kind === 'DFA') return runDfa(machine, input);
  return runNfa(machine, input);
}

/**
 * @param {import('./machines.js').Machine} machine
 * @param {string} input
 */
function runDfa(machine, input) {
  /** @type {{ step: number, read: string, state: string, note: string }[]} */
  const trace = [];
  let state = machine.start;
  trace.push({ step: 0, read: '', state, note: 'start' });

  for (let i = 0; i < input.length; i += 1) {
    const sym = input[i];
    if (!machine.alphabet.includes(sym)) {
      return {
        ok: false,
        accepted: false,
        reason: `reject: "${sym}" not in Σ={${machine.alphabet.join(',')}}`,
        trace,
        states: [state],
      };
    }
    const key = `${state},${sym}`;
    const next = machine.transitions[key];
    if (!next || Array.isArray(next)) {
      trace.push({ step: i + 1, read: input.slice(0, i + 1), state, note: `no transition on ${sym}` });
      return { ok: true, accepted: false, reason: 'reject: dead state', trace, states: [state] };
    }
    state = next;
    trace.push({ step: i + 1, read: input.slice(0, i + 1), state, char: sym, note: `read ${sym}` });
  }

  const accepted = machine.accept.includes(state);
  return {
    ok: true,
    accepted,
    reason: accepted ? 'accept: final state is accepting' : 'reject: final state not accepting',
    trace,
    states: [state],
  };
}

/**
 * @param {import('./machines.js').Machine} machine
 * @param {string} input
 */
function runNfa(machine, input) {
  const eps = machine.epsilon ?? {};
  const epsilonClosure = (states) => {
    const stack = [...states];
    const seen = new Set(states);
    while (stack.length) {
      const s = stack.pop();
      for (const t of eps[s] ?? []) {
        if (!seen.has(t)) {
          seen.add(t);
          stack.push(t);
        }
      }
    }
    return [...seen].sort();
  };

  const move = (states, sym) => {
    const out = new Set();
    for (const s of states) {
      const key = `${s},${sym}`;
      const next = machine.transitions[key];
      if (!next) continue;
      const list = Array.isArray(next) ? next : [next];
      for (const t of list) out.add(t);
    }
    return epsilonClosure([...out]);
  };

  /** @type {{ step: number, read: string, states: string[], note: string }[]} */
  const trace = [];
  let current = epsilonClosure([machine.start]);
  trace.push({ step: 0, read: '', states: current, note: 'start (ε-closure)' });

  for (let i = 0; i < input.length; i += 1) {
    const sym = input[i];
    if (!machine.alphabet.includes(sym)) {
      return {
        ok: false,
        accepted: false,
        reason: `reject: "${sym}" not in Σ={${machine.alphabet.join(',')}}`,
        trace,
        states: current,
      };
    }
    current = move(current, sym);
    if (!current.length) {
      trace.push({ step: i + 1, read: input.slice(0, i + 1), states: [], note: `no path on ${sym}` });
      return { ok: true, accepted: false, reason: 'reject: no active states', trace, states: [] };
    }
    trace.push({ step: i + 1, read: input.slice(0, i + 1), states: current, char: sym, note: `read ${sym}` });
  }

  const accepted = current.some((s) => machine.accept.includes(s));
  return {
    ok: true,
    accepted,
    reason: accepted ? 'accept: ∃ path to accepting state' : 'reject: no accepting state reachable',
    trace,
    states: current,
  };
}
