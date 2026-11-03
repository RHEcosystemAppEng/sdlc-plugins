# Criterion 4: Check 6 produces WARN when any new symbol lacks documentation

**Verdict: PASS**

## Evidence

Sub-step `#### 6c — Produce Verdict`:

> - **WARN** — at least one new symbol lacks a documentation comment
>
> Evidence: list of undocumented symbols with file path and line number.

## Reasoning

"At least one" means the same as "any". The check also has to list each undocumented symbol with its file and line, so the WARN can be acted on. That matches the evidence style of Checks 2 and 3 in the same file.
