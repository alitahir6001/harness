# Available Claude Code Skills

## Stock Skills (Bundled with Claude)

* **build-skill-library**
  * Create a tailor-made skill library under .claude/skills/ with five foundational skills to document your project for future sessions and smaller models.

* **code-review**
  * Review code diffs for correctness bugs and efficiency cleanups at multiple effort levels, with options to post findings as PR comments or apply fixes.

* **simplify**
  * Review changed code for reuse, simplification, efficiency, and refactor opportunities, then automatically apply fixes.

* **fewer-permission-prompts**
  * Scan your transcripts for common read-only tool calls and add an allowlist to settings.json to reduce permission prompts.

* **loop**
  * Run a prompt or slash command on a recurring interval with self-pacing or fixed delays.

* **schedule**
  * Create and manage cloud agents on cron schedules for automated recurring tasks.

* **claude-api**
  * Reference for Claude API / Anthropic SDK — model IDs, pricing, streaming, tool use, and token counting.

* **run**
  * Launch this project's app and verify changes work in the real environment.

* **init**
  * Initialize a new CLAUDE.md file with codebase documentation.

* **review**
  * Review a GitHub pull request.

* **security-review**
  * Perform security-focused code review.

* **verify**
  * Verify that a code change actually works by running the app and observing behavior.

---

## Custom Skills (Project/Harness-Specific)

* **harness-architecture-contract**
  * Documents the load-bearing design decisions of the harness workspace — why files live where they do and known weak points.

* **harness-change-control**
  * Explains how config changes are classified and gated — which edits are free vs. which need testing or sign-off.

* **harness-evidence-and-analysis**
  * Provides recipes for verifying harness behavior through discriminating probes and root-cause analysis.

* **harness-reference**
  * Domain reference for Claude Code harness configuration layers — where each lives, when it loads, and its token cost.

* **harness-research-frontier**
  * Documents open problems and next-level harness projects, including building a custom harness on the Agent SDK.

* **harness-runbook**
  * Runbook for harness operations and troubleshooting.

* **harness-token-efficiency-campaign**
  * Campaign guide for optimizing token usage in the harness.

* **update-config**
  * Configure the Claude Code harness via settings.json, manage permissions, set env vars, and troubleshoot hooks.

* **keybindings-help**
  * Customize keyboard shortcuts and rebind keys in ~/.claude/keybindings.json.

* **create-session-context**
  * Scaffold a new project's `.ai/` memory files (rules, current-task, handoff, backlog) and an optional root CLAUDE.md. Manual-only — invoke with `/create-session-context`. Renamed from `new-project-bootstrap`.

* **update-session-context**
  * Populate the `.ai/` memory files from the current session's work, run once at session end. Manual-only — invoke with `/update-session-context`. Renamed from `populate-ai-files`.

* **get-session-context**
  * Orient a fresh session on an existing project by reading CLAUDE.md + `.ai/` files, then report where things left off and what the current task is. Manual-only — invoke with `/get-session-context`.

* **anthropic-skills:consolidate-memory**
  * Reflective pass over memory files — merge duplicates, fix stale facts, and prune the index.

* **anthropic-skills:docx**
  * Tools for working with Word documents (.docx format).

* **anthropic-skills:pdf**
  * Tools for working with PDF documents.

* **anthropic-skills:pptx**
  * Tools for working with PowerPoint presentations.

* **anthropic-skills:setup-cowork**
  * Set up cowork plugin integration.

* **anthropic-skills:skill-creator**
  * Create custom skills.

* **anthropic-skills:xlsx**
  * Tools for working with Excel spreadsheets.

* **cowork-plugin-management:cowork-plugin-customizer**
  * Customize cowork plugins.

* **cowork-plugin-management:create-cowork-plugin**
  * Create new cowork plugins.

---

## Summary

- **Stock Skills:** 12
- **Custom Skills:** 20
- **Total:** 32 skills available
