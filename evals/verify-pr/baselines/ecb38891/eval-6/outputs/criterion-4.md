# Acceptance Criterion 4

## Criterion

> Check 6 produces WARN when any new symbol lacks documentation

## Verdict: PASS

## Reasoning

The PR diff adds Step 6c ("Produce Verdict") to Check 6, which explicitly includes the WARN verdict condition:

> WARN -- at least one new symbol lacks a documentation comment

This directly satisfies the criterion. When any new symbol identified in Step 6a does not have a corresponding documentation comment (as verified in Step 6b), the check produces a WARN verdict. The evidence section also specifies that undocumented symbols are listed with file path and line number, providing actionable detail.

## Evidence

From the PR diff in style-conventions.md:

```
#### 6c — Produce Verdict

- **PASS** — all new symbols have documentation comments
- **WARN** — at least one new symbol lacks a documentation comment
- **N/A** — no new symbols introduced in the PR

Evidence: list of undocumented symbols with file path and line number.
```
