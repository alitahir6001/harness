---
name: create-session-context
description: Scaffold a brand-new project's memory system — create .ai/ (handoff, rules, backlog) and a pruned root CLAUDE.md. Stack-agnostic. Use when starting or bootstrapping a new project from scratch. Keywords: new project, bootstrap, scaffold, set up .ai, initialize project memory, project setup.
disable-model-invocation: true
---

# create-session-context

Scaffold the **current directory** as a project root: create the `.ai/` memory files and a root `CLAUDE.md` from the template. Stack-agnostic. Manual and side-effecting — only runs when invoked.

## Steps

1. **Confirm location.** Run `pwd`. This scaffolds the *current* directory. If that isn't the intended project root, stop and ask.

2. **Guard against clobbering.** Never overwrite anything that exists. Scaffold only what's missing, without asking — e.g. a repo that has `.ai/` but no `CLAUDE.md` gets just the `CLAUDE.md` (step 4), and vice versa. Report what was skipped as already present; only ask if the user explicitly wants an existing file replaced.

3. **Create `.ai/` and three files.** `rules.md` ships with the full maintenance contract below — it's the one file a cold agent can read to learn how to use this directory, so create it exactly as written. The other two start as bare skeletons; `update-session-context` fills `handoff.md` in at a task boundary.

   `.ai/rules.md`:
   ```
   # Project rules & how to maintain .ai/

   ## Maintaining these files
   At session start, read `handoff.md` ONLY. Everything else loads on demand.

   - **handoff.md** - live state snapshot, and the only file read at startup. Rewrite in place, never append like a log. Cap 8 KB.
   - **rules.md** - this file. Read when you're about to change code, or when handoff points at a rule. Edit only on an explicit "add a project rule: X".
   - **backlog.md** - parked work. Read only when the user asks about it or asks you to add to it. Never read at startup.
   - Permanent gotchas / non-obvious behavior that stays true for the project's life -> root `CLAUDE.md`, not here.
   - Subsystem depth (how the renderer works, what the pipeline costs) -> a project skill under `.claude/skills/`, not here. Skill descriptions sit in context for ~20 tokens each and the body loads only when relevant.

   ## What earns a place in this file
   A rule belongs here only if ALL FOUR hold. Otherwise route it:
   1. It applies to ANY change in this project - not one subsystem. (Subsystem -> a skill.)
   2. It is not a general engineering or epistemic principle. (General -> `~/.claude/CLAUDE.md`, where it works across every project.)
   3. It is not a standing user preference. (Preference -> `~/.claude/CLAUDE.md`.)
   4. Breaking it costs real money, real data, or something the user cannot undo.

   **Cap 8 KB, measured in bytes, not lines.** A line cap on paragraph-length entries is not a cap - one project's rules file reached 57 KB and 105 rules against a "200 line" limit, and ~70% of it had already been superseded by project skills. One sentence per rule plus a pointer; the long version lives in the skill.

   ## Status marks
   Use these for any step or task that needs a status — in handoff's Active task section and elsewhere:
   - `[ ]` todo
   - `[~]` in progress
   - `[x]` done
   - `[!]` blocked

   ## Populating from empty
   - **handoff.md** - Last updated (date + session N) / Current state (3 sentences) / Active task (what, why, remaining steps with status marks and owner) / Open threads (max 5) / Next recommended step / Out of scope. No "changed files" section - `git log` and `git diff` answer that for free and never go stale.
   - **backlog.md** - parked items only. Not a session log.

   ## Quick reference: when to touch what
   | Event | handoff.md | rules.md | backlog.md | CLAUDE.md |
   |---|---|---|---|---|
   | Made a code change | yes | - | - | - |
   | Hit a blocker / found a bug | yes | - | - | - |
   | Finished task, starting new one | yes | - | - | - |
   | Task boundary / ~50% context | yes | - | - | - |
   | User says "add a project rule" | - | yes | - | - |
   | User says "park that" / "add to backlog" | - | - | yes | - |
   | Discovered a permanent gotcha | yes | - | - | only if user agrees |

   ## Project-specific rules
   <!-- Tech stack, code conventions, agent workflow constraints (e.g. "never run git"), security rules - append as discovered. Skip anything guessable from the code. -->
   ```
   `.ai/handoff.md` — the only file read at session start:
   ```
   # Handoff — live state snapshot

   ## Last updated

   ## Current state

   ## Active task

   ## Open threads

   ## Next recommended step

   ## Out of scope
   ```
   `.ai/backlog.md`:
   ```
   # Backlog

   Parked work. Not read at session start — pull it in when asked.

   ## Parked items
   ```

4. **Create root `CLAUDE.md` from the template.** Copy `~/.claude/skills/create-session-context/CLAUDE.template.md` to `./CLAUDE.md`. Fill in only what you can confidently infer from the directory (project name; a one-line "what this project is" if obvious from a README or `package.json` description). Leave everything else as bracketed placeholders and keep the guidance comment block so the user can prune later — including the note about small projects skipping File map / Architecture. **Cap at 12 KB** (bytes, not lines) — this file is loaded on every single session, so it is the most expensive text in the project.

5. **Report + reminder.** List the files created (do not echo their full contents). Remind the user: run `build-skill-library` *later*, once the project has real code — not now. `handoff.md` gets filled at the first task boundary via `update-session-context`.

## Do not
- Do not run `git init` or commit.
- Do not run `build-skill-library`.
- Do not populate the `.ai/` files with content — leave them as headers.
- Do not echo full file contents into chat; just list what was created.

## See also
- `update-session-context` — rewrites `handoff.md` at a task boundary.
- `get-session-context` — reads these files at the start of a new session to orient on where things left off.
