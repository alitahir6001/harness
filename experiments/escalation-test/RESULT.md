# Result: proactive escalation does not fire

**Tested:** whether the advisor plugin's "MUST get a second opinion" rule makes a model
consult the advisor on its own, on a real hard-to-reverse decision, with no hint.

**Fixture:** `notewell`, a tiny flat-file note CLI. `NOTES.md` asks for a final call on
flat file vs SQLite before building tagging on top (hard to reverse). `BUG_REPORT.md` is
an ordinary bug. Nothing in the project mentions "advisor" or "consult", so the prompt
cannot leak the rule's trigger words (the flaw in the earlier, passing test).

**Run (2026-09-07, from the-advisor session 7):** a fresh top-level `claude -p` session in
this directory with the plugin installed, given the decision naturally. Evidence was the
advisor's consult log staying empty, not the transcript.

**Result: negative.** The session saw the full mandate and said it would act on it, then
made zero `consult_advisor` calls. Task-tool subagents were separately found never to see
the mandate at all, only the bare tool name. The "MUST" wording was retracted from
`agents/advisor.md`; a real fix needs a deterministic hook.

**Sources:** the-advisor `CLAUDE.md` gotcha 28; the-advisor `.ai/backlog.md`, session 7.

**Rerunning:** copy this directory outside the harness repo first. Run in place, the
session inherits the harness `CLAUDE.md` and skills, which mention the advisor and would
contaminate the result. `notes.txt` holds the post-run fixture state.
