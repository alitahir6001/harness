# harness

A working notebook for making coding agents behave: Claude Code's configuration surface
treated as something to test rather than guess at.

This is a **workspace, not an application**. There is no build and no test suite. What
lives here is configuration, documented findings, and a small amount of runnable code
under `experiments/`.

## Why it exists

Agent harnesses are configured mostly by folklore. Rules get added to a `CLAUDE.md`,
behavior seems to change, nobody checks whether it actually did. This repo is the
opposite habit: a claim about agent behavior isn't accepted here until a fresh session
demonstrates it.

## The validation bar

The evidence is the tool calls, not the reply. A model will happily *say* it consulted
an advisor without ever invoking one, so behavior is verified by running a fresh session
and reading the event stream:

```
claude -p "<prompt>" --model haiku --output-format stream-json --verbose
```

Then parse the stream for actual `tool_use` entries. Testing against a small model is
deliberate: rules that only work on a frontier model aren't rules, they're suggestions
that happened to land.

## What's here

```
.claude/skills/     seven project skills, the durable knowledge layer
.ai/                live session state (handoff, current task, backlog, rules)
CLAUDE.md           per-turn rules only
SKILLS_AVAILABLE.md catalog of stock + custom skills
experiments/        runnable code
```

The split is deliberate and enforced: **skills hold durable knowledge, `.ai/` holds
session state, `CLAUDE.md` holds per-turn rules.** One home per fact. When those blur,
an agent reads three versions of the same thing and picks the wrong one.

## Findings worth keeping

A few results from testing that generalize past this repo.

**Behavior**

- **A model agreeing to a rule is not evidence it will follow it.** An escalation rule
  ("You MUST get a second opinion before finalizing...") was tested in a fresh session on
  a project that never mentioned the advisor. The model read the rule, said it would act
  on it, then made zero tool calls on a real hard-to-reverse decision. An earlier test had
  passed, but its prompts contained the rule's own trigger words. Stronger wording didn't
  close the gap; a deterministic hook is the remaining option, not yet built or tested.
- **Check that a rule is visible before testing whether it works.** MCP tool descriptions
  can be deferred out of context, and Task-tool subagents never see agent descriptions at
  all, only the bare tool name. A rule the model can't see fails for a different reason
  than one it ignores.
- **A test can contaminate its own result.** Two A/B runs on whether a written "verify
  the downstream effect" rule changed behavior were both inconclusive: asking "did it
  work?" made the model check carefully with or without the rule. The real failures had
  happened during unrelated work, when nobody asked.
- **Duplicate installs compete.** Providing the same agent both manually and via a plugin
  yielded two advisor agents and two MCP servers in one session. One source, or neither.

**Cost** (measured September 2026, from an audit of 171 sessions)

- **Session memory should load lazily.** Reading every session file at startup cost about
  49,000 tokens per session in the largest project. Reading only the handoff, pulling
  rules and backlog on demand, and cutting duplicated sections from `CLAUDE.md` brought it
  to about 15,000, a 69% cut.
- **Write the handoff at a task boundary, not at the end.** Late wrap-ups cost about twice
  the output of early ones (~11,200 vs ~5,700 tokens), and the gap held when
  sessions were matched on workload.
- **Transcript token counts double unless deduped.** Claude Code's JSONL stores one
  response as several records, each repeating the same `usage` object. Dedupe by
  `requestId`. Dense markdown also ran about 2.5 bytes per token, not the usual 4.

## The Advisor

The advisor/workhorse pattern started here and has **graduated into its own repo**:

> **[the-advisor](https://github.com/alitahir6001/the-advisor)**: a Claude Code plugin
> that lets a cheap workhorse model get a second opinion from a stronger advisor (Claude,
> Gemini, GPT or a local model) on hard-to-reverse decisions, through `/consult`.

`experiments/advisor-pattern/` is a frozen snapshot of the original development version.
It is kept for history and **is not what runs**. Edit the plugin repo instead.

## Status

Advisor pattern shipped and lives in its own repo. Its proactive-escalation test came back
negative (see Findings), so it is invoked on demand. This repo's own session files have
not been moved to the leaner layout yet.
