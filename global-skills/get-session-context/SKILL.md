---
name: get-session-context
description: Orient a new session on an existing project by reading .ai/handoff.md — one file — then report where things left off and what the current task is. Loads rules, backlog, CLAUDE.md and project skills only on demand. Use at the start of a session when the user says get up to speed, orient me, where did we leave off, catch me up, or resume work on this project. Keywords: orient, catch up, resume, where did we leave off, session start, get up to speed.
disable-model-invocation: true
---

# get-session-context

Orient on an existing project by reading its memory files, then tell the user two things: where things left off and what the current task is. Read-only — no side effects.

## Precondition
- If `.ai/` doesn't exist, stop and tell the user to run `create-session-context` first.

## Steps

1. **Read `.ai/handoff.md`. That's it.** One file. Use the Read tool on the path directly rather than a Bash existence check (`ls`/`test`) first — a missing file is normal and the Read tool reports it plainly instead of surfacing a misleading non-zero exit in the UI.

   Do NOT eagerly read `CLAUDE.md`, `.ai/rules.md`, or `.ai/backlog.md`. Measured 2026-09-20: across the user's 12 projects with this system, reading the full set costs 5k–49k tokens per session start (job-apply alone is ~49,000), and most of it goes unused for the session's actual work. Those files are still there and still authoritative — pull them in when you need them:
   - **`.ai/rules.md`** — when you're about to change code, or when handoff points at a rule.
   - **root `CLAUDE.md`** — the harness usually loads this on its own. Read it only if you can't see it and you need architecture or gotchas.
   - **`.ai/backlog.md`** — only when the user asks about parked work, or asks you to add something to it.
   - **`.ai/history.md`** — only when the user asks about past work or why something was decided.
   - **`.ai/current-task.md`** — legacy layout only. If the project still has one and `handoff.md` doesn't name the active task, read it too.
   - **a project skill** — for subsystem depth (a runbook, a resume/PDF skill, an architecture contract). Their descriptions are already in context; load the one that matches the work.

2. **Synthesize, don't transcribe.** Don't repeat full file contents or the project's entire history back to the user.

3. **Report exactly two things:**
   - **Where we left off** — a few sentences from `handoff.md`: what was last done, its result, any open thread.
   - **Current task** — what handoff's Active task section says is live right now, including its out-of-scope note.

   If a file is missing or empty (e.g. fresh scaffold with only headers), say so plainly rather than inventing content.

## Do not
- Do not echo full file contents into the conversation.
- Do not read `rules.md`, `backlog.md` or `CLAUDE.md` "to be thorough" — that's the cost this skill exists to avoid.
- Do not modify any files — this skill is read-only.

## See also
- `create-session-context` — scaffolds these files for a new project.
- `update-session-context` — rewrites `handoff.md` at a task boundary.
