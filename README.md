<div align="center">

<p>
  <img src="assets/pumpkin-automata-banner.webp" alt="Pumpkin Automata — AL102 DFA/NFA simulator" width="1200" height="400" />
</p>

### **Pick a machine. Type a string. Watch every step.**

**Pumpkin Automata — interactive finite-automaton lab for AL102 (Week 7 & 10)**

<p>
  <strong>① Pick</strong> a slide machine &nbsp;·&nbsp;
  <strong>② Type</strong> a string over Σ &nbsp;·&nbsp;
  <strong>③ Trace</strong> → ACCEPT · REJECT · INVALID
</p>

</div>

<p align="center">
  <img src="https://img.shields.io/badge/AL102-DFA%20%26%20NFA-orange?style=flat" alt="AL102">
  <img src="https://img.shields.io/badge/runtime-static%20HTML%20%2B%20ESM-14425b?style=flat" alt="Static site">
  <img src="https://img.shields.io/badge/tests-67%20e2e-brightgreen?style=flat" alt="E2E tests">
  <img src="https://img.shields.io/badge/Python-3-generate%20SVG-3776AB?style=flat&logo=python&logoColor=white" alt="Python generators">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"></a>
</p>

<p align="center">
  <a href="#get-started"><strong>Run locally</strong></a> ·
  <a href="#demo">Demo</a> ·
  <a href="#machines">Machines</a> ·
  <a href="#how-the-simulator-works">Simulator</a> ·
  <a href="#verify">Tests</a> ·
  <a href="#project-layout">Layout</a> ·
  <a href="#regenerate">Regenerate</a>
</p>

---

> **Pedagogy first:** **INVALID** means a symbol ∉ Σ. **REJECTED** means a legal string outside the language. Logic: `source/automata/simulator.js`. Definitions: `source/automata/machines.js`.

## Get started

```bash
git clone https://github.com/aaron-devx/pumpkin-automata.git
cd pumpkin-automata
python3 -m http.server 5500 --bind 0.0.0.0
```

| Device | URL |
|--------|-----|
| This machine | http://localhost:5500 |
| Phone (same Wi‑Fi) | `http://<your-lan-ip>:5500` |

No `npm install`. Optional CDN (Lenis + GSAP) adds scroll polish; the lab works without it. `prefers-reduced-motion` disables animation.

## Demo

**2‑minute class flow**

1. **DFA — ends with 10** → run `1010` → **ACCEPTED** → step the trace.
2. Same machine → `11` → **REJECTED**.
3. **NFA — ends with aab** → `baab` → **ACCEPTED** → point at **multiple active states** on one step.

**Page map**

| Section | What it does |
|---------|----------------|
| Hero | Machine dropdown, input, **Run** |
| Problems | Six flip cards → **Try** loads the lab |
| Example strings | Carousel of slide samples |
| Lab | Verdict, δ table, graph, step slider, trace table |

Canonical app: **repo root `index.html`** (built from `source/template.html`).

## Machines

Σ is **fixed per machine** (lab note `Σ={…}` and δ table headers).

| ID | Kind | Σ | Language |
|----|------|---|----------|
| `dfa-begins-0` | DFA | `0, 1` | Begins with `0` |
| `dfa-ends-10` | DFA | `0, 1` | Ends with `10` |
| `dfa-contains-bab` | DFA | `a, b` | Contains `bab` |
| `dfa-a-then-bstar` | DFA | `a, b` | `a` then `b*` |
| `nfa-abc-slide` | NFA | `0, 1` | Slide A,B,C · accept `C` |
| `nfa-ends-aab` | NFA | `a, b` | Ends with `aab` |

Edit **`source/automata/machines.js`**; build copies to `automata/`.

## How the simulator works

```text
machines.js          simulator.js              automata_app.js
  (δ, Σ, F)    →     run(machine, input)   →   trace + UI
                     ├─ DFA: one state
                     └─ NFA: set + ε-closure (when ε edges exist)
```

| Verdict | Meaning |
|---------|---------|
| `INVALID` | Character not in Σ |
| `REJECTED` | Valid string, not accepted |
| `ACCEPTED` | Final state(s) in `F` |

## Verify

```bash
# Terminal 1
python3 -m http.server 5500

# Terminal 2 — Chrome (default macOS path in script)
node tests/e2e/lab.e2e.mjs
```

## Tech stack

| Layer | Technology |
|-------|------------|
| Lab | Vanilla JS (ESM), inline SVG diagram |
| Site | Generated `index.html`, `main.js` |
| Art | Python in `source/` → `svg/*.svg` |
| Motion | CSS keyframes / SMIL + optional GSAP |
| Tests | Node ≥22, Chrome CDP (`tests/e2e/lab.e2e.mjs`) |

## Project layout

| Path | Role |
|------|------|
| `source/template.html` | Page + styles |
| `source/build_site.py` | Build `index.html`, copy `automata/` |
| `source/automata/*.js` | Machines, simulator, UI (**edit here**) |
| `source/hero.py`, `source/scenes.py` | Vector scenes |
| `automata/` | Built JS at runtime |
| `assets/pumpkin-automata-banner.webp` | README hero (1200×400) |

## Regenerate

```bash
cd source && python3 hero.py && python3 scenes.py && python3 build_site.py
```

Writes `svg/*`, `index.html`, and `main.js` at repo root. Do not hand-edit `index.html` long-term.

## License

MIT — see [LICENSE](LICENSE).