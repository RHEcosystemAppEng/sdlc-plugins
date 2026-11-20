# Criterion 4: Check 6 produces WARN when any new symbol lacks documentation

**Verdict: PASS**

## Evidence
New sub-step **6c — Produce Verdict**:

> - **WARN** — at least one new symbol lacks a documentation comment
>
> Evidence: list of undocumented symbols with file path and line number.

## Reasoning
"At least one" matches "any". WARN is the right severity: it matches the other Style/Conventions checks, where WARN is informational and not a FAIL. The check also has to list each undocumented symbol with its file path and line number, so the WARN is actionable.
