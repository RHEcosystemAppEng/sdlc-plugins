# triage-bug Eval Results

## Aggregate Metrics

| Metric | Current | Baseline (8b288dc2) | Delta |
|--------|---------|---------------------|-------|
| Pass Rate | 1.0 (±0.0) | 1.0 (±0.0) | — |
| Time (s) | 57.67 (±26.34) | 53.0 (±28.08) | +4.67 |
| Tokens | 29839 (±5328) | 19194 (±1896) | +10645 |

## Per-Eval Results

### Eval 1 — Standard Bug Triage (ACME-500)

**Pass rate: 9/9 (100%)**

| # | Assertion | Result |
|---|-----------|--------|
| 1 | Bug parsing extracts all four required sections using template heading formats | PASS |
| 2 | Bug validation confirms issue type ID 10020 matches Bug Configuration | PASS |
| 3 | Investigation identifies trailing-whitespace heading extraction (`line[3:]`) as root cause | PASS |
| 4 | Root cause comment includes what/where/how-to-verify | PASS |
| 5 | Reproducer test is FIRST acceptance criterion | PASS |
| 6 | Reproducer test is FIRST test requirement with assertion guidance from Steps to Reproduce | PASS |
| 7 | Bug Context section includes Bug key, Steps to Reproduce, Expected/Actual Result, Root Cause | PASS |
| 8 | Target Branch set to main | PASS |
| 9 | ai-generated-jira label in Jira API metadata block | PASS |

**Timing:** 92s, 35467 tokens

### Eval 2 — Missing Sections Validation (ACME-501)

**Pass rate: 4/4 (100%)**

| # | Assertion | Result |
|---|-----------|--------|
| 1 | Identifies missing Steps to Reproduce section | PASS |
| 2 | Identifies missing Expected Result section | PASS |
| 3 | Stops execution at Step 1 — does not proceed to Steps 2-5 | PASS |
| 4 | Error message lists missing sections and references Bug template path | PASS |

**Timing:** 28s, 22689 tokens

### Eval 3 — Multi-Root-Cause Decomposition Guard (ACME-502)

**Pass rate: 5/5 (100%)**

| # | Assertion | Result |
|---|-----------|--------|
| 1 | Identifies two independent root causes (convention formatter + wrong issue type ID) | PASS |
| 2 | Decomposition Guard triggered — root causes in different modules | PASS |
| 3 | Guard presents both issues with affected files/modules | PASS |
| 4 | Guard offers Proceed or Split options | PASS |
| 5 | Skill pauses — does not silently create a single Task | PASS |

**Timing:** 53s, 31361 tokens

## Summary

**18/18 assertions passed (100%).** Pass rate matches baseline. Token usage is higher than baseline (+10645 mean), likely due to model differences across runs.
