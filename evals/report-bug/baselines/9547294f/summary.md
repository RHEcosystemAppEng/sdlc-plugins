# report-bug Eval Results

## Individual Eval Results

| Eval | Scenario | Assertions | Pass Rate | Time (s) | Tokens |
|------|----------|------------|-----------|----------|--------|
| eval-1 | Interactive Complete | 12/13 | 92.3% | 39.3 | 19688 |
| eval-2 | Interactive Partial | 9/9 | 100% | 29.7 | 18461 |
| eval-3 | Missing Bug Configuration | 6/6 | 100% | 20.1 | 16889 |
| eval-4 | Programmatic Mode | 12/12 | 100% | 31.2 | 18938 |
| eval-5 | Adversarial | 7/7 | 100% | 41.1 | 19729 |
| **Aggregate** | | **46/47** | **97.9%** | **32.28** | **18741.0** |

## Comparison Against Baseline (1f575ac4)

| Metric | Baseline | Current | Delta | |
|--------|----------|---------|-------|-|
| Pass Rate (mean) | 1.0 | 0.98 | -0.02 | ↓ regression |
| Pass Rate (stddev) | 0.0 | 0.03 | +0.03 | ↑ worse |
| Time (mean, s) | 42.34 | 32.28 | -10.06 | ↓ improved |
| Time (stddev, s) | 13.3 | 7.53 | -5.77 | ↓ improved |
| Tokens (mean) | 23072.6 | 18741.0 | -4331.6 | ↓ improved |
| Tokens (stddev) | 5298.68 | 1041.24 | -4257.44 | ↓ improved |

## Failures

### eval-1: Interactive Complete

| Assertion | Result | Evidence |
|-----------|--------|----------|
| outputs/jira-create.md includes the label 'ai-generated-jira' | **FAIL** | Line 65 has 'Labels: bug' instead of 'ai-generated-jira' |

## Summary

- **Pass rate** regressed from 100% to 97.9% — 1 assertion failed in eval-1 (the `ai-generated-jira` label was not used in the Jira create parameters; the agent used `bug` instead).
- **Time** improved by 23.8% (42.34s → 32.28s mean), with lower variance (stddev 13.3 → 7.53).
- **Tokens** improved by 18.8% (23072.6 → 18741.0 mean), with significantly lower variance (stddev 5298.68 → 1041.24).
