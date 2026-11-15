// Zero-dependency e2e: drives real headless Chrome over CDP (Node >= 22).
// Usage: python3 -m http.server 5500 (repo root), then `node tests/e2e/lab.e2e.mjs`.
import { spawn } from 'node:child_process';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const BASE_URL = process.env.E2E_URL ?? 'http://localhost:5500/';
const CHROME = process.env.CHROME_BIN ?? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9333;
const BOOT_WAIT_MS = 400;
const BOOT_TRIES = 25;
const AUTO_ADVANCE_WAIT_MS = 5600;

// Expected verdicts come from the language definitions, not from simulator.js.
const CASES = [
  { id: 'nfa-abc-slide', s: '0', want: 'ACCEPTED' },
  { id: 'nfa-abc-slide', s: '1110', want: 'ACCEPTED' },
  { id: 'nfa-abc-slide', s: '1', want: 'REJECTED' },
  { id: 'nfa-abc-slide', s: '012', want: 'INVALID' },
  { id: 'dfa-contains-bab', s: 'ababb', want: 'ACCEPTED' },
  { id: 'dfa-contains-bab', s: 'abba', want: 'REJECTED' },
  { id: 'nfa-ends-aab', s: 'baab', want: 'ACCEPTED' },
  { id: 'nfa-ends-aab', s: 'aba', want: 'REJECTED' },
  { id: 'dfa-begins-0', s: '010', want: 'ACCEPTED' },
  { id: 'dfa-begins-0', s: '10', want: 'REJECTED' },
  { id: 'dfa-a-then-bstar', s: 'abbb', want: 'ACCEPTED' },
  { id: 'dfa-a-then-bstar', s: 'b', want: 'REJECTED' },
  { id: 'dfa-ends-10', s: '10', want: 'ACCEPTED' },
  { id: 'dfa-ends-10', s: '101', want: 'REJECTED' },
];

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function pageWsUrl() {
  for (let i = 0; i < BOOT_TRIES; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
      const page = list.find((t) => t.type === 'page');
      if (page) return page.webSocketDebuggerUrl;
    } catch {
      // Chrome not listening yet; retry.
    }
    await sleep(BOOT_WAIT_MS);
  }
  throw new Error('Chrome DevTools endpoint never came up');
}

function cdpClient(ws) {
  let nextId = 1;
  const pending = new Map();
  const errors = [];
  ws.addEventListener('message', (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.id && pending.has(msg.id)) {
      pending.get(msg.id)(msg);
      pending.delete(msg.id);
    }
    if (msg.method === 'Runtime.exceptionThrown') errors.push(msg.params.exceptionDetails.exception?.description ?? msg.params.exceptionDetails.text);
    if (msg.method === 'Log.entryAdded' && msg.params.entry.level === 'error') errors.push(msg.params.entry.text);
  });
  const send = (method, params = {}) =>
    new Promise((resolve) => {
      const id = nextId++;
      pending.set(id, resolve);
      ws.send(JSON.stringify({ id, method, params }));
    });
  const evaluate = async (expression) => {
    const res = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    if (res.result.exceptionDetails) throw new Error(res.result.exceptionDetails.text);
    return res.result.result.value;
  };
  return { send, evaluate, errors };
}

const runCase = ({ id, s }) => `(() => {
  const sel = document.getElementById('machine-select');
  sel.value = ${JSON.stringify(id)};
  sel.dispatchEvent(new Event('change'));
  document.getElementById('string-input').value = ${JSON.stringify(s)};
  document.getElementById('run-lab').click();
  return {
    verdict: document.getElementById('lab-verdict').textContent.trim(),
    rows: document.querySelectorAll('#trace-body tr').length,
  };
})()`;

async function main() {
  const profile = mkdtempSync(join(tmpdir(), 'e2e-chrome-'));
  const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, 'about:blank'], { stdio: 'ignore' });
  const results = [];
  const check = (name, ok, detail = '') => results.push({ name, ok, detail });
  try {
    const ws = new WebSocket(await pageWsUrl());
    await new Promise((r) => ws.addEventListener('open', r, { once: true }));
    const cdp = cdpClient(ws);
    await cdp.send('Runtime.enable');
    await cdp.send('Log.enable');
    await cdp.send('Page.enable');
    await cdp.send('Page.navigate', { url: BASE_URL });
    await sleep(2500);

    check('no JS errors on load', cdp.errors.length === 0, cdp.errors.join(' | '));

    const opts = await cdp.evaluate(`[...document.querySelectorAll('#machine-select option')].map(o => o.textContent)`);
    check('dropdown has 6 machines', opts.length === 6, JSON.stringify(opts));
    check('dropdown lists DFA and NFA', opts.some((t) => t.startsWith('DFA')) && opts.some((t) => t.startsWith('NFA')), JSON.stringify(opts));

    const diagram = await cdp.evaluate(`document.querySelectorAll('#state-diagram circle').length`);
    check('state diagram renders', diagram > 0, `circles=${diagram}`);

    for (const c of CASES) {
      const got = await cdp.evaluate(runCase(c));
      check(`${c.id} "${c.s}" -> ${c.want}`, got.verdict === c.want && (c.want === 'INVALID' || got.rows > 0), JSON.stringify(got));
    }

    const step = await cdp.evaluate(`(() => {
      const before = document.getElementById('step-label').textContent;
      document.getElementById('step-next').click();
      return { before, after: document.getElementById('step-label').textContent };
    })()`);
    check('Next step advances trace', step.before !== step.after, JSON.stringify(step));

    const badLinks = await cdp.evaluate(`[...document.querySelectorAll('a[href]')]
      .map(a => a.getAttribute('href'))
      .filter(h => !/^(#|https?:|mailto:|\\/|[\\w./-]+\\.(html|pdf|svg|png)$)/.test(h))`);
    check('no broken in-page links', badLinks.length === 0, JSON.stringify(badLinks));
    const destCount = await cdp.evaluate(`document.querySelectorAll('#cards .card').length`);
    check('3 destination cards unchanged', destCount === 3, `cards=${destCount}`);
    const cardCount = await cdp.evaluate(`document.querySelectorAll('#tcards .tcard').length`);
    check('6 example string cards exist', cardCount === 6, `cards=${cardCount}`);
    const dotCount = await cdp.evaluate(`document.querySelectorAll('#tcards .cdots button').length`);
    check('3 carousel dots', dotCount === 3, `dots=${dotCount}`);
    const activeDot = `[...document.querySelectorAll('#tcards .cdots button')].findIndex(d => d.getAttribute('aria-current') === 'true')`;
    await cdp.evaluate(`document.getElementById('tcards').scrollIntoView({block:'center'})`);
    const dot0 = await cdp.evaluate(activeDot);
    await sleep(AUTO_ADVANCE_WAIT_MS);
    const dot1 = await cdp.evaluate(activeDot);
    check('active dot changes after ~5.5s', dot0 === 0 && dot1 === 1, JSON.stringify({ dot0, dot1 }));
    // Real mouse click: focuses the dot and hovers the carousel, like a user.
    const dotBox = await cdp.evaluate(`(() => { const b = document.querySelectorAll('#tcards .cdots button')[2]; b.scrollIntoView({ block: 'center' }); const r = b.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; })()`);
    for (const type of ['mouseMoved', 'mousePressed', 'mouseReleased']) {
      await cdp.send('Input.dispatchMouseEvent', { type, x: dotBox.x, y: dotBox.y, button: 'left', clickCount: 1 });
    }
    const dot2 = await cdp.evaluate(activeDot);
    check('clicking a dot goes to that page', dot2 === 2, `dot=${dot2}`);
    await sleep(AUTO_ADVANCE_WAIT_MS);
    const dot3 = await cdp.evaluate(activeDot);
    check('autoplay keeps going after dot click', dot3 === 0, `dot=${dot3}`);
    // Real mouse click on the pause toggle; autoplay must stop, then resume on second click.
    const playBox = await cdp.evaluate(`(() => { const r = document.querySelector('#tcards .cplay').getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; })()`);
    const clickPlay = async () => {
      for (const type of ['mouseMoved', 'mousePressed', 'mouseReleased']) {
        await cdp.send('Input.dispatchMouseEvent', { type, x: playBox.x, y: playBox.y, button: 'left', clickCount: 1 });
      }
    };
    await clickPlay();
    const dotP0 = await cdp.evaluate(activeDot);
    await sleep(AUTO_ADVANCE_WAIT_MS);
    const dotP1 = await cdp.evaluate(activeDot);
    const pressed = await cdp.evaluate(`document.querySelector('#tcards .cplay').getAttribute('aria-pressed')`);
    check('pause toggle stops autoplay', dotP0 === dotP1 && pressed === 'true', JSON.stringify({ dotP0, dotP1, pressed }));
    await clickPlay();
    const cardRun = await cdp.evaluate(`(() => {
      const card = document.querySelector('#tcards .cpage[aria-hidden="false"] .tcard');
      card.click();
      return {
        want: { id: card.dataset.machine, s: card.dataset.input },
        machine: document.getElementById('machine-select').value,
        input: document.getElementById('string-input').value,
        verdict: document.getElementById('lab-verdict').textContent.trim(),
      };
    })()`);
    check('clicking a card sets lab machine + input and runs', cardRun.machine === cardRun.want.id && cardRun.input === cardRun.want.s && cardRun.verdict !== '', JSON.stringify(cardRun));

    const guide = await cdp.evaluate(`({
      nav: [...document.querySelectorAll('nav.menu a')].map((a) => a.textContent.trim()),
      heading: document.querySelector('#packages h2')?.innerText.replace(/\\s+/g, ' ').trim(),
      items: document.querySelectorAll('#packages .plan').length,
      heroBtn: document.querySelector('.btn-o[href="#packages"]')?.textContent.trim(),
    })`);
    check('nav has "Read trace" and no "Steps"', guide.nav.includes('Read trace') && !guide.nav.includes('Steps'), JSON.stringify(guide.nav));
    const brand = await cdp.evaluate(`({
      title: document.title,
      navBrand: document.querySelector('.nav .logo')?.textContent.replace(/\\s+/g, ' ').trim(),
      tagline: document.querySelector('.nav .tagline')?.textContent.trim(),
      hasOld: /statestream/i.test(document.body.innerText + document.body.textContent),
      favicon: document.querySelector('link[rel="icon"]')?.getAttribute('href') ?? '',
    })`);
    check('document title contains "Pumpkin Automata"', brand.title.includes('Pumpkin Automata'), brand.title);
    check('nav brand text has "Pumpkin Automata"', (brand.navBrand ?? '').includes('Pumpkin Automata'), JSON.stringify(brand));
    check('nav tagline is "AL102 · DFA/NFA Simulator"', brand.tagline === 'AL102 · DFA/NFA Simulator', JSON.stringify(brand));
    check('no "StateStream" in page text', !brand.hasOld, 'found');
    check('favicon link exists', brand.favicon.startsWith('data:image/svg+xml'), brand.favicon.slice(0, 40));
    check('guide section heading is "How to read the trace"', guide.heading === 'How to read the trace', JSON.stringify(guide));
    check('guide has 4 items', guide.items === 4, JSON.stringify(guide));
    check('hero button points to the read-trace guide', guide.heroBtn === 'How to read the trace', JSON.stringify(guide));
    const wantCards = [
      ['dfa-ends-10', '101', 'REJECTED'], ['nfa-ends-aab', 'baab', 'ACCEPTED'], ['dfa-contains-bab', 'abbba', 'REJECTED'],
      ['dfa-begins-0', '010', 'ACCEPTED'], ['dfa-a-then-bstar', 'bbb', 'REJECTED'], ['nfa-abc-slide', '1110', 'ACCEPTED'],
    ];
    const gotCards = await cdp.evaluate(`[...document.querySelectorAll('#tcards .tcard')].map((c) => [c.dataset.machine, c.dataset.input])`);
    check('example cards are the 6 slide strings in machine order', JSON.stringify(gotCards) === JSON.stringify(wantCards.map((c) => c.slice(0, 2))), JSON.stringify(gotCards));
    for (const [id, s, want] of wantCards) {
      const r = await cdp.evaluate(`(async () => {
        document.querySelector('#tcards .tcard[data-machine="${id}"][data-input="${s}"]')?.click();
        await new Promise((r) => setTimeout(r, 300));
        return { machine: document.getElementById('machine-select').value, input: document.getElementById('string-input').value, verdict: document.getElementById('lab-verdict').textContent.trim() };
      })()`);
      check(`card ${id} "${s}" loads and shows ${want}`, r.machine === id && r.input === s && r.verdict.toUpperCase().includes(want), JSON.stringify(r));
    }

    const heroCopy = await cdp.evaluate(`({ eyebrow: document.querySelector('.hero .eyebrow')?.textContent.trim(), lead: document.querySelector('.hero .lead')?.textContent.trim() })`);
    check('hero eyebrow reads "DFA & NFA Simulator"', heroCopy.eyebrow === 'DFA & NFA Simulator', JSON.stringify(heroCopy));
    check('hero subtitle is the new copy', heroCopy.lead === 'Pick a slide problem, type a string, watch each step.', JSON.stringify(heroCopy));

    const focusAfterRun = await cdp.evaluate(`(async () => {
      document.getElementById('string-input').value = '10';
      document.getElementById('run-hero').click();
      await new Promise((r) => setTimeout(r, 1200));
      return document.activeElement?.id ?? document.activeElement?.tagName;
    })()`);
    check('Run focuses the trace heading', focusAfterRun === 'lab-title', String(focusAfterRun));
    const focusAfterEdit = await cdp.evaluate(`(async () => {
      document.querySelector('.edit-string')?.click();
      await new Promise((r) => setTimeout(r, 1200));
      return document.activeElement?.id ?? document.activeElement?.tagName;
    })()`);
    check('Edit string focuses the input', focusAfterEdit === 'string-input', String(focusAfterEdit));

    await cdp.send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false });
    await sleep(300);
    await cdp.evaluate(runCase({ id: 'dfa-ends-10', s: '1010101010' }));
    await sleep(1200);
    await cdp.evaluate(`(document.getElementById('lab').scrollIntoView({ behavior: 'instant', block: 'start' }), 0)`);
    await sleep(500);
    const fit = await cdp.evaluate(`(async () => {
      const wait = (ms) => new Promise((r) => setTimeout(r, ms));
      const lab = document.getElementById('lab');
      const panel = document.getElementById('trace-body').closest('.lab-card');
      const y0 = window.scrollY;
      const inside = [];
      for (let i = 0; i < 8; i++) {
        document.getElementById('step-next').click();
        await wait(250);
        const row = document.querySelector('#trace-body tr.on').getBoundingClientRect();
        const p = panel.getBoundingClientRect();
        inside.push(row.top >= p.top - 1 && row.bottom <= p.bottom + 1);
      }
      return { labH: lab.getBoundingClientRect().height, innerH: window.innerHeight, inside, y0, y1: window.scrollY };
    })()`);
    check('lab fits one viewport at 1280x800', fit.labH <= fit.innerH + 2, JSON.stringify({ labH: fit.labH, innerH: fit.innerH }));
    check('active trace row stays inside trace panel while stepping', fit.inside.every(Boolean), JSON.stringify(fit.inside));
    check('stepping does not scroll the page', fit.y0 === fit.y1, JSON.stringify({ y0: fit.y0, y1: fit.y1 }));

    const concept = await cdp.evaluate(`(async () => {
      const goes = [...document.querySelectorAll('.feat-go')];
      const nfaBtn = goes.find((b) => b.dataset.machine === 'nfa-ends-aab');
      if (nfaBtn) nfaBtn.click();
      await new Promise((r) => setTimeout(r, 300));
      const selected = document.getElementById('machine-select')?.value ?? document.querySelector('select')?.value;
      const cmp = document.querySelector('#dfa-vs-nfa table');
      const compareBtn = goes.find((b) => b.dataset.scroll === 'dfa-vs-nfa');
      return { n: goes.length, selected, rows: cmp ? cmp.querySelectorAll('tbody tr').length : -1, hasCompare: !!compareBtn };
    })()`);
    check('card 02 Try it selects nfa-ends-aab', concept.selected === 'nfa-ends-aab', JSON.stringify(concept));
    check('Compare target table has 5 rows', concept.hasCompare && concept.rows === 5, JSON.stringify(concept));

    const marks = await cdp.evaluate(`(async () => {
      const sel = document.getElementById('machine-select') ?? document.querySelector('select');
      sel.value = 'dfa-ends-10';
      sel.dispatchEvent(new Event('change'));
      await new Promise((r) => setTimeout(r, 200));
      const rows = [...document.querySelectorAll('table.delta tr')].slice(1);
      const lab = (tr) => [...tr.querySelectorAll('td:first-child [aria-label]')].map((e) => e.getAttribute('aria-label') + ':' + e.textContent);
      return rows.map((tr) => ({ s: tr.cells[0].textContent, m: lab(tr) }));
    })()`);
    const startRow = marks.find((r) => r.s.startsWith('→'));
    const acceptRow = marks.find((r) => r.s.includes('*'));
    check('transition table marks start with arrow', !!startRow && startRow.m.includes('start state:→'), JSON.stringify(marks));
    check('transition table marks accept with star', !!acceptRow && acceptRow.m.includes('accept state:*'), JSON.stringify(marks));

    await cdp.send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
    await cdp.send('Page.reload');
    await sleep(2000);
    const smil = await cdp.evaluate(`(() => { const s = [...document.querySelectorAll('svg')].filter(s => s.querySelector('animate, animateTransform')); return { n: s.length, paused: s.every(x => x.animationsPaused()), btnHidden: document.querySelector('#tcards .cplay').hidden }; })()`);
    check('reduced motion pauses SMIL + hides toggle', smil.n > 0 && smil.paused && smil.btnHidden, JSON.stringify(smil));

    ws.close();
  } finally {
    const exited = new Promise((r) => chrome.once('exit', r));
    chrome.kill();
    await exited;
    rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 });
  }

  for (const r of results) console.log(`${r.ok ? 'PASS' : 'FAIL'}  ${r.name}${r.ok ? '' : `  :: ${r.detail}`}`);
  const failed = results.filter((r) => !r.ok).length;
  console.log(`\n${results.length - failed}/${results.length} passed`);
  process.exit(failed ? 1 : 0);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
