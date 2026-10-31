# Available Claude Code Skills

Generated 2026-10-31 from a live session's skill list (Claude Code 2.1.281, desktop app Code
tab, working dir = this repo). Skills marked manual-only set `disable-model-invocation`
and don't appear in that list; they come from `~/.claude/skills/`. The bundled set differs
by client: a CLI `claude -p` init event (same date) also listed `batch`, `debug`,
`design`, `design-sync`, `doctor`, `run-skill-generator`, `verify`, `workflow-authoring`
and lacked the `anthropic-skills:` set.

## Custom

### Project (`.claude/skills/`, this repo)

| Skill | What it does |
|---|---|
| `harness-architecture-contract` | Why files live where they do; three-store separation; known weak points |
| `harness-change-control` | Which config edits are free, which need a fresh-session test or user sign-off |
| `harness-evidence-and-analysis` | Discriminating probes, premise teardown, root cause for "Claude ignored my rule" |
| `harness-reference` | Config layers: where each lives, when it loads, what it costs |
| `harness-research-frontier` | Open problems: own harness on the Agent SDK, trigger reliability, first hooks |
| `harness-runbook` | Setup, config catalog, diagnostic scripts, symptom triage, validation bar |
| `harness-token-efficiency-campaign` | Phased plan against the Pro 5-hour usage cap |

### Global (`~/.claude/skills/`)

| Skill | Source | What it does |
|---|---|---|
| `create-session-context` | `global-skills/` (symlink), manual-only | Scaffold `.ai/` (handoff, rules, backlog) and a root CLAUDE.md |
| `get-session-context` | `global-skills/` (symlink), manual-only | Orient a fresh session from `.ai/handoff.md` only |
| `update-session-context` | `global-skills/` (symlink), manual-only | Rewrite `.ai/handoff.md` at a task boundary |
| `build-skill-library` | `global-skills/` (symlink) | Author a 5-skill project library (this repo's seven came from it) |
| `grill-me` | `~/.claude/skills/` only | Interview the user about a plan until each decision branch is resolved |

### Plugin: `the-advisor` (github.com/alitahir6001/the-advisor)

| Skill | What it does |
|---|---|
| `the-advisor:consult` | Ask the advisor a direct question |
| `the-advisor:second-opinion` | Route a question to a named provider's CLI (claude, gemini, codex) |
| `the-advisor:advisor-model` | Show or change the advisor model without a restart |
| `the-advisor:doctor` | Check that the advisor install works |

## Bundled

### Claude Code built-in

`code-review`, `simplify`, `security-review`, `init`, `run`, `loop`, `schedule`,
`claude-api`, `update-config`, `keybindings-help`, `fewer-permission-prompts`,
`plugin-authoring`, `dataviz`, `artifact-design`, `artifact-diagramming`,
`artifact-capabilities`

### From the Anthropic account (claude.ai)

- `anthropic-skills:` `built-in-browser`, `chrome-browser`, `computer-use`,
  `consolidate-memory`, `deep-research`, `docs`, `docx`, `explain-usage`,
  `google-workspace`, `import-memory`, `morning`, `pdf`, `pptx`, `setup-claude`,
  `skill-creator`, `xlsx`
- `cowork-plugin-management:` `cowork-plugin-customizer`, `create-cowork-plugin`

## Summary

- Custom: 16 (7 project, 5 global, 4 plugin)
- Bundled: 34 (16 Claude Code built-in, 18 from the Anthropic account)
- Total: 50
