# Criterion 4: Check 6 produces WARN when any new symbol lacks documentation

## Verdict: PASS

## Reasoning

The PR diff adds section "6c -- Produce Verdict" to style-conventions.md, which explicitly defines:

> **WARN** -- at least one new symbol lacks a documentation comment

This directly satisfies the criterion. When any new public symbol identified in step 6a lacks a documentation comment as verified in step 6b, Check 6 produces a WARN verdict. The evidence field specifies: "list of undocumented symbols with file path and line number."
