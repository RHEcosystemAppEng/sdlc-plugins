# Criterion 4 — Check 6 produces WARN when any new symbol lacks documentation

**Verdict: MET (PASS)**

## Evidence (from the PR diff, `style-conventions.md`, `#### 6c — Produce Verdict`)

> - **WARN** — at least one new symbol lacks a documentation comment
>
> Evidence: list of undocumented symbols with file path and line number.

## Reasoning

"At least one new symbol lacks a documentation comment" means the same as "any new symbol lacks documentation". The verdict is WARN, not FAIL, which fits the Style/Conventions sub-agent's design: every check there is informational, using PASS/WARN/N/A only. The check also tells the agent to list each undocumented symbol with its file path and line number. That makes the WARN actionable, and it is the same level of evidence that Check 3 (Test Documentation) asks for.
