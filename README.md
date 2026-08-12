# harness

A working notebook for making coding agents behave — Claude Code's configuration surface
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
deliberate — rules that only work on a frontier model aren't rules, they're suggestions
that happened to land.

## What's here

```
.claude/skills/     seven project skills — the durable knowledge layer
.ai/                live session state (handoff, current task, backlog, rules)
CLAUDE.md           per-turn rules only
SKILLS_AVAILABLE.md catalog of stock + custom skills
experiments/        runnable code
```

The split is deliberate and enforced: **skills hold durable knowledge, `.ai/` holds
session state, `CLAUDE.md` holds per-turn rules.** One home per fact. When those blur,
an agent reads three versions of the same thing and picks the wrong one.

## Findings worth keeping

A few results from testing that generalize past this repo:

- **Directive wording beats polite wording.** "You MUST consult BEFORE finalizing…"
  produces the behavior; "consult when appropriate" does not. Verified against a small
  workhorse model, where the gap is widest.
- **Placement decides whether a rule fires.** Escalation policy lives in a subagent's
  description, because agent descriptions are always in context while MCP tool
  descriptions can be deferred — and a deferred description can't drive proactive
  behavior.
- **Duplicate installs compete.** Providing the same agent both manually and via a plugin
  yielded two advisor agents and two MCP servers in one session. One source, or neither.

## The Advisor

The advisor/workhorse pattern started here and has **graduated into its own repo**:

> **[the-advisor](https://github.com/alitahir6001/the-advisor)** — a Claude Code plugin
> that routes architectural and hard-to-reverse decisions to a stronger model for a second
> opinion, while cheap models carry the everyday workload.

`experiments/advisor-pattern/` is a frozen snapshot of the original development version.
It is kept for history and **is not what runs** — edit the plugin repo instead.

## Status

Advisor pattern shipped. Current work is cross-project validation, then confirming the
setup reproduces on a second machine.
