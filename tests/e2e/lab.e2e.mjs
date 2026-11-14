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

// Expected verdicts come from the language definitions, not from simulator.js.
const CASES = [
  { id: 'nfa-abc-slide', s: '0', want: 'ACCEPTED' },
  { id: 'nfa-abc-slide', s: '1110', want: 'ACCEPTED' },
  { id: 'nfa-abc-slide', s: '1', want: 'REJECTED' },
  { id: 'nfa-abc-slide', s: '012', want: 'INVALID' },
  { id: 'dfa-aba-dead', s: 'aba', want: 'ACCEPTED' },
  { id: 'dfa-aba-dead', s: 'abb', want: 'REJECTED' },
  { id: 'dfa-a-then-bstar', s: 'abbb', want: 'ACCEPTED' },
  { id: 'dfa-a-then-bstar', s: 'b', want: 'REJECTED' },
  { id: 'dfa-suffix-01', s: '101', want: 'ACCEPTED' },
  { id: 'dfa-suffix-01', s: '10', want: 'REJECTED' },
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
    check('dropdown has 4 machines', opts.length === 4, JSON.stringify(opts));
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
