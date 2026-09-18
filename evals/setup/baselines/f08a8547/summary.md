# setup Eval Results

## Run Summary

| Metric | Current | Baseline (f1caf724) | Delta |
|--------|---------|---------------------|-------|
| Pass rate | **1.00** | 0.98 | +0.02 |
| Time (mean) | **74.1s** | 147.9s | -73.8s (-49.9%) |
| Tokens (mean) | **28,035** | 37,506 | -9,471 (-25.2%) |

## Per-Eval Results

| Eval | Name | Assertions | Passed | Pass Rate | Time | Tokens |
|------|------|------------|--------|-----------|------|--------|
| 1 | Greenfield setup | 9 | 9 | 1.00 | 58.6s | 29,464 |
| 2 | Incremental update | 8 | 8 | 1.00 | 62.1s | 28,447 |
| 3 | No-Serena/no-MCP | 8 | 8 | 1.00 | 54.9s | 33,619 |
| 4 | Adversarial | 7 | 7 | 1.00 | 151.1s | 31,241 |
| 5 | Security opt-in | 8 | 8 | 1.00 | 69.9s | 27,774 |
| 6 | Full idempotency | 7 | 7 | 1.00 | 47.7s | 17,666 |
| **Total** | | **47** | **47** | **1.00** | | |

## Baseline Comparison

- **Pass rate**: 1.00 vs 0.98 baseline (+0.02) — improvement
- **Time**: 74.1s vs 147.9s baseline (-49.9%) — significant improvement
- **Tokens**: 28,035 vs 37,506 baseline (-25.2%) — significant improvement

## Failed Assertions

None — all 47 assertions passed across 6 evals.
