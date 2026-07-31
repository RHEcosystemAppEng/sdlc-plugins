# Acceptance Criterion 5

## Criterion

> Check 6 produces N/A when no new symbols are introduced in the PR

## Verdict: PASS

## Reasoning

The PR diff includes N/A handling at two levels:

1. **Step 6a (early exit):** "If no new symbols are found, skip to the Verdict and record N/A." This provides an early exit path when there are no new symbols to check, avoiding unnecessary processing.

2. **Step 6c (verdict definition):** The verdict list explicitly includes "N/A -- no new symbols introduced in the PR" as a defined outcome.

Both the early exit mechanism and the verdict definition consistently support the N/A case, satisfying this criterion.

## Evidence

From the PR diff in style-conventions.md:

Step 6a:
```
If no new symbols are found, skip to the Verdict and record N/A.
```

Step 6c:
```
- **N/A** — no new symbols introduced in the PR
```
