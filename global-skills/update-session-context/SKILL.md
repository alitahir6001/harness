---
name: update-session-context
description: Rewrite .ai/handoff.md from the current session's work so the next session can resume. Use at a task boundary or when the user says to wrap up, update the session files, populate handoff, or save state before stopping. Does NOT touch rules.md, backlog.md or CLAUDE.md unless the user asks by name. Keywords: wrap up, end of session, update .ai, populate handoff, save state, session handoff.
disable-model-invocation: true
---

# update-session-context

Rewrite `.ai/handoff.md` from **this session's** work so a cold session can resume. Manual and side-effecting. Run it at a task boundary or around 50% context — not after every task, and not only at the bitter end.

## Precondition
- If `.ai/` doesn't exist, stop and tell the user to run `create-session-context` first.

## How to write
- **Write files directly.** After writing, give only a 2–4 line summary of what changed per file. Do NOT echo full file contents back into the conversation.
- **Respect line caps.** If a file would exceed its cap, condense or prune older low-value content rather than blow the cap.

## What to write

**One file: `.ai/handoff.md`. OVERWRITE it.** Rewrite in place, never append like a log.

```
# Handoff — live state snapshot
## Last updated
<date + session N>
## Current state
<3 sentences max: what is true right now>
## Active task
<what / why / the numbered steps left, marked [ ] [~] [x] [!], owner agent|user>
## Open threads
<max 5 bullets>
## Next recommended step
<one line>
## Out of scope
<one line>
```

**Cap: 8 KB.** Cap in BYTES, not lines — a line cap on paragraph-length entries is no cap at all (that's how one project's rules file reached 57 KB against a "200 line" limit). If it won't fit, cut the oldest open thread.

**Do NOT write "Changed files this session."** `git log` and `git diff` answer it for free and can never go stale.

## Files this skill no longer touches

Measured across 56 past wrap-ups: `CLAUDE.md` was edited **109 times** against a contract that said "durable, permanent facts only," and the rules file 27 times against "only when a rule itself changes." Stated-but-unenforced limits don't hold, so these are now explicit user asks, never automatic:

- **`./CLAUDE.md`** — only when the user says to, or to add a genuinely permanent gotcha they've agreed to.
- **`.ai/rules.md`** — only on "add a project rule: X". Then apply the admission test: it belongs here only if it applies to ANY change in this project, isn't a general engineering principle (that goes in `~/.claude/CLAUDE.md`), isn't subsystem depth (that goes in a project skill), and breaking it costs real money, data, or the user's candidacy.
- **`.ai/backlog.md`** — only on "add that to the backlog" / "move that to the backlog".
- **`.ai/current-task.md`** — legacy layout. Don't create one; fold its content into handoff's Active task section.

## When to run

**At a task boundary or around 50% context — not at session end.** Measured: wrap-ups in light sessions cost ~5,700 output tokens versus ~11,200 in heavy ones, and the gap survives controlling for how much work the session contained. A wrap-up written while you can still see the work is also more accurate than one reconstructed from a 275k-token session.

## Do not
- Do not run after every task.
- Do not echo full file contents into the conversation.
- Do not exceed the 8 KB cap.

## See also
- `create-session-context` — scaffolds these files for a new project.
- `get-session-context` — reads these files at the start of a new session to orient on where things left off.
