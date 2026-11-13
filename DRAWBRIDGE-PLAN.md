# Drawbridge plan (9 tasks)

**Source:** `.moat/moat-tasks.md` · generated 2026-11-13

## P0 — Lab works

| # | Task | Status |
|---|------|--------|
| 1 | Hero machine field | **done** flex min-width; JS `node --check` OK (not syntax err) |

## P1 — CSS + card copy

| # | Task | Status |
|---|------|--------|
| 3 | Footer underline hover-only | **done** template |
| 4 | Remove card hover lift/zoom | **done** |
| 5 | White card body AL102 meta | **done** build_site.py |
| 7 | Run button no hover shadow | **done** |

## P2 — Vector art (next slice)

| # | Task | Files |
|---|------|--------|
| 2 | Avatar1 contrast | `source/scenes.py` avatar(1) |
| 6 | Hero island dog/human | `source/hero.py` |
| 8 | Why scene dog collar/arm | `source/scenes.py` why_scene |
| 9 | Why woman + chair | `source/scenes.py` + ref PNG |

**Regen after art:** `cd source && python3 hero.py && python3 scenes.py && python3 build_site.py`

**Moat lifecycle:** set JSON status doing → done per task when verified.
