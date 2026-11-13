/** @typedef {{ id: string, label: string, kind: 'DFA' | 'NFA', alphabet: string[], start: string, accept: string[], transitions: Record<string, string | string[]>, epsilon?: Record<string, string[]>, source?: string, layout?: { width: number, height: number, nodes: { id: string, x: number, y: number }[] }, samples?: { s: string, hint: string }[] }} Machine */

/** @type {Machine[]} */
export const MACHINES = [
  {
    id: 'nfa-abc-slide',
    kind: 'NFA',
    label: 'NFA — prof diagram A,B,C',
    source: 'Slide 1 · accept C · {0,1}',
    alphabet: ['0', '1'],
    start: 'A',
    accept: ['C'],
    transitions: {
      'A,0': 'C',
      'A,1': ['A', 'B'],
      'B,1': 'B',
      'B,0': 'C',
      'C,1': 'B',
    },
    layout: {
      width: 360,
      height: 200,
      nodes: [
        { id: 'A', x: 70, y: 120 },
        { id: 'B', x: 200, y: 50 },
        { id: 'C', x: 290, y: 120 },
      ],
    },
    samples: [
      { s: '0', hint: 'A→C accept' },
      { s: '1110', hint: 'ends 0 → C' },
      { s: '1', hint: 'may branch' },
    ],
  },
  {
    id: 'dfa-aba-dead',
    kind: 'DFA',
    label: 'DFA — contains aba (dead D)',
    source: 'Slide 2 · accept qf',
    alphabet: ['a', 'b'],
    start: 'q0',
    accept: ['qf'],
    transitions: {
      'q0,a': 'q1',
      'q0,b': 'D',
      'q1,b': 'q2',
      'q1,a': 'D',
      'q2,a': 'qf',
      'q2,b': 'D',
      'qf,a': 'qf',
      'qf,b': 'qf',
      'D,a': 'D',
      'D,b': 'D',
    },
    layout: {
      width: 420,
      height: 180,
      nodes: [
        { id: 'q0', x: 40, y: 90 },
        { id: 'q1', x: 120, y: 40 },
        { id: 'q2', x: 200, y: 90 },
        { id: 'qf', x: 300, y: 90 },
        { id: 'D', x: 200, y: 155 },
      ],
    },
    samples: [
      { s: 'aba', hint: 'accept' },
      { s: 'xabab', hint: 'still has aba' },
      { s: 'abb', hint: 'reject → D' },
    ],
  },
  {
    id: 'dfa-a-then-bstar',
    kind: 'DFA',
    label: 'DFA — a then b*',
    source: 'Slide 3 · accept B',
    alphabet: ['a', 'b'],
    start: 'A',
    accept: ['B'],
    transitions: {
      'A,a': 'B',
      'A,b': 'C',
      'B,b': 'B',
      'B,a': 'C',
      'C,a': 'C',
      'C,b': 'C',
    },
    layout: {
      width: 320,
      height: 160,
      nodes: [
        { id: 'A', x: 60, y: 80 },
        { id: 'B', x: 180, y: 50 },
        { id: 'C', x: 180, y: 120 },
      ],
    },
    samples: [
      { s: 'a', hint: 'accept' },
      { s: 'abbb', hint: 'accept' },
      { s: 'b', hint: 'trap C' },
    ],
  },
  {
    id: 'dfa-suffix-01',
    kind: 'DFA',
    label: 'DFA — suffix 01 (q2 accept)',
    source: 'Slide 4 · orange q2',
    alphabet: ['0', '1'],
    start: 'q0',
    accept: ['q2'],
    transitions: {
      'q0,1': 'q0',
      'q0,0': 'q1',
      'q1,0': 'q1',
      'q1,1': 'q2',
      'q2,0': 'q1',
      'q2,1': 'q0',
    },
    layout: {
      width: 400,
      height: 140,
      nodes: [
        { id: 'q0', x: 70, y: 70 },
        { id: 'q1', x: 200, y: 70 },
        { id: 'q2', x: 330, y: 70 },
      ],
    },
    samples: [
      { s: '01', hint: 'accept' },
      { s: '101', hint: 'accept on …01' },
      { s: '10', hint: 'reject' },
    ],
  },
];

export function getMachine(id) {
  return MACHINES.find((m) => m.id === id) ?? MACHINES[0];
}

export function layoutEdges(m) {
  const out = [];
  for (const [key, val] of Object.entries(m.transitions)) {
    const [from, sym] = key.split(',');
    const tos = Array.isArray(val) ? val : [val];
    for (const to of tos) out.push({ from, to, sym });
  }
  return out;
}
