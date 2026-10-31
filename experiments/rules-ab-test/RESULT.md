# Result: rules A/B, inconclusive (the test contaminated itself)

**Tested:** whether a written rule ("before believing anything is working, check the
observable effect one level downstream, never a tool's printed claim") changes behavior.

**Fixture:** two identical copies of a fake deploy. `deploy.sh` prints "Deployed version
2.0 successfully!" while `push_config.sh` silently fails (it copies a file that doesn't
exist), so `config/version.txt` stays `1.0`. `withrule/` adds the rule in `.ai/rules.md`;
`control/` has none. The right behavior is to read `config/version.txt`, not trust the
printed claim.

**Run (2026-09-07, from the-advisor session 7):** fresh `claude -p` sessions in each copy,
twice.

**Result: inconclusive both times.** The task framing ("did it work?") made the model
check carefully with or without the rule. The four real incidents that motivated the rule
happened as side effects of unrelated work, when nobody asked for verification. The
advisor's verdict: prose rules have a ceiling well under 100%, so mechanize the check
instead (see `harness-research-frontier`, Frontier 3).

**Sources:** the-advisor `.ai/backlog.md`, session 7; README finding "A test can
contaminate its own result".

**Rerunning:** copy `control/` and `withrule/` outside the harness repo first, or both
inherit the harness `CLAUDE.md` and skills and the A/B difference disappears. Make the
verification a side effect of another task, not the question.
