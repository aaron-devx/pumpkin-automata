# AGENTS.md (router, max 55 lines). Read fully. Everything else loads on demand.

## 0. Autonomy (highest priority)
- Run commands yourself. Never tell the user to run them.
- Ask the user only for: secrets, or ONE yes/no before an irreversible action.
- Never ask what you can learn from `.ogi/` or the code.

## 1. Start of every session (silent, in order)
1. Read `.ogi/handoff.md`.
2. Task type (bugfix/feature/refactor/research/automation) -> global `ogi-<type>` skill loads itself; follow it.

## 2. Finding code: tool order, never skip
1. Where is X / how do A and B connect -> `graphify query "..."`, `graphify path A B`, `graphify explain X`
2. Exact lines to edit -> `Read` WITH `offset` and `limit`
3. Output may exceed 5 KB (logs, tests, web pages, big JSON) -> `ctx_execute`, `ctx_batch_execute`, `ctx_fetch_and_index`
4. Whole-file `Read` of a file over ~800 lines is the LAST resort. A hook may block it. Follow the hook message.

## 3. Working rules
- Challenge first: if the plan has a real flaw, say it in max 2 bullets with the better option. Then do what the user chose. Do not block on taste.
- One task at a time. Finish, verify, report.
- Verify before saying done: run the check named in the skill's Verify list. No check run = say "unverified".
- Never invent file paths, functions, or APIs. If the tools cannot find it, say "not found".
- Never hand-edit lock files or generated files. Never touch `.env*`, secrets, `node_modules`.

## 4. Subagents
- Pick the specialist that fits the task. State the pick in one line.
- Subagents obey section 2 too. If a subagent file has no tool protocol, paste section 2 into its prompt.

## 5. Memory: what to write and where
- Decision made -> one line in `.ogi/decisions.md` (date, decision, why).
- Approach tried and rejected -> one line under "Dead ends" in the same file.
- User corrected you -> one line in `.ogi/corrections.md` (what you did / what they wanted).
- End of session or long pause -> rewrite `.ogi/handoff.md` (max 25 lines; top 3: Next action / Blocked on / Don't touch).
- `.ogi` = symlink to vault `10_Projects/snaptrips-vector-clean/` (git-ignored). Missing -> run `ogi init`.

## 6. Replies to the user (final message only)
- Short. Bullets. Order: Done, Why, Next.
- Plans, code, and reasoning may be as long as needed. Brevity applies to the final message only.
