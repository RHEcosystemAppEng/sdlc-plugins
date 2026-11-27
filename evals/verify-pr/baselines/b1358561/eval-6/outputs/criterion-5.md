# Criterion 5 — Check 6 produces N/A when no new symbols are introduced in the PR

**Verdict: PASS**

## Evidence
- `#### 6a`: "If no new symbols are found, skip to the Verdict and record N/A."
- `#### 6c`: "**N/A** — no new symbols introduced in the PR"

## Reasoning
N/A is defined in two places: an early exit in 6a and the verdict list in 6c. The early exit follows the same pattern as Check 2a and Check 5a ("skip to the Verdict and record N/A"). Because Markdown files are skipped in 6b, a Markdown-only PR also has no applicable new symbols and gets N/A. That is consistent with the task's definition.
