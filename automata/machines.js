/** @typedef {{ id: string, label: string, kind: 'DFA' | 'NFA', alphabet: string[], start: string, accept: string[], transitions: Record<string, string | string[]>, epsilon?: Record<string, string[]>, source?: string, layout?: { width: number, height: number, nodes: { id: string, x: number, y: number }[] }, samples?: { s: string, hint: string }[] }} Machine */

/** @type {Machine[]} */
export const MACHINES = [
  {
    id: 'dfa-ends-10',
    kind: 'DFA',
    label: 'DFA — ends with 10',
    source: 'AL102 Week 7 cont. P2',
    alphabet: ['0', '1'],
    start: 'q0',
    accept: ['q2'],
    transitions: {
      'q0,0': 'q0',
      'q0,1': 'q1',
      'q1,0': 'q2',
      'q1,1': 'q1',
      'q2,0': 'q0',
      'q2,1': 'q1',
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
      { s: '10', hint: 'accept' },
      { s: '110', hint: 'accept' },
      { s: '0010', hint: 'accept' },
      { s: '101', hint: 'reject' },
      { s: '100', hint: 'reject' },
      { s: '01', hint: 'reject' },
    ],
  },
  {
    id: 'nfa-ends-aab',
    kind: 'NFA',
    label: 'NFA — ends with aab',
    source: 'AL102 Week 10 Q2',
    alphabet: ['a', 'b'],
    start: 'q0',
    accept: ['q3'],
    transitions: {
      'q0,a': ['q0', 'q1'],
      'q0,b': 'q0',
      'q1,a': 'q2',
      'q2,b': 'q3',
    },
    layout: {
      width: 420,
      height: 150,
      nodes: [
        { id: 'q0', x: 50, y: 75 },
        { id: 'q1', x: 160, y: 75 },
        { id: 'q2', x: 270, y: 75 },
        { id: 'q3', x: 375, y: 75 },
      ],
    },
    samples: [
      { s: 'aab', hint: 'accept' },
      { s: 'baab', hint: 'accept' },
      { s: 'aaab', hint: 'accept' },
      { s: 'ab', hint: 'reject' },
      { s: 'aba', hint: 'reject' },
      { s: 'aabb', hint: 'reject' },
    ],
  },
  {
    id: 'dfa-contains-bab',
    kind: 'DFA',
    label: 'DFA — contains bab',
    source: 'AL102 Week 7 cont. P3',
    alphabet: ['a', 'b'],
    start: 'q0',
    accept: ['q3'],
    transitions: {
      'q0,a': 'q0',
      'q0,b': 'q1',
      'q1,a': 'q2',
      'q1,b': 'q1',
      'q2,a': 'q0',
      'q2,b': 'q3',
      'q3,a': 'q3',
      'q3,b': 'q3',
    },
    layout: {
      width: 420,
      height: 150,
      nodes: [
        { id: 'q0', x: 50, y: 75 },
        { id: 'q1', x: 160, y: 75 },
        { id: 'q2', x: 270, y: 75 },
        { id: 'q3', x: 375, y: 75 },
      ],
    },
    samples: [
      { s: 'bab', hint: 'accept' },
      { s: 'ababb', hint: 'accept' },
      { s: 'babb', hint: 'accept' },
      { s: 'aabab', hint: 'accept' },
      { s: 'ab', hint: 'reject' },
      { s: 'ba', hint: 'reject' },
      { s: 'bb', hint: 'reject' },
      { s: 'abba', hint: 'reject' },
      { s: 'aaa', hint: 'reject' },
    ],
  },
  {
    id: 'dfa-begins-0',
    kind: 'DFA',
    label: 'DFA — begins with 0',
    source: 'AL102 Week 7 cont. P1',
    alphabet: ['0', '1'],
    start: 'q0',
    accept: ['q1'],
    transitions: {
      'q0,0': 'q1',
      'q0,1': 'qd',
      'q1,0': 'q1',
      'q1,1': 'q1',
      'qd,0': 'qd',
      'qd,1': 'qd',
    },
    layout: {
      width: 320,
      height: 160,
      nodes: [
        { id: 'q0', x: 60, y: 80 },
        { id: 'q1', x: 200, y: 45 },
        { id: 'qd', x: 200, y: 120 },
      ],
    },
    samples: [
      { s: '0', hint: 'accept' },
      { s: '01', hint: 'accept' },
      { s: '001', hint: 'accept' },
      { s: '0111', hint: 'accept' },
      { s: '1', hint: 'reject → dead' },
      { s: '10', hint: 'reject' },
      { s: '110', hint: 'reject' },
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
