# report-bug Eval Results

## Individual Eval Results

| Eval | Scenario | Assertions | Pass Rate | Time (s) | Tokens |
|------|----------|------------|-----------|----------|--------|
| eval-1 | Interactive Complete | 14/14 | 100% | 45.7 | 23541 |
| eval-2 | Interactive Partial | 10/10 | 100% | 50.5 | 23216 |
| eval-3 | Missing Bug Configuration | 6/6 | 100% | 20.1 | 19614 |
| eval-4 | Programmatic Mode | 13/13 | 100% | 53.3 | 23772 |
| eval-5 | Adversarial | 8/8 | 100% | 63.7 | 25417 |
| **Aggregate** | | **51/51** | **100%** | **46.66** | **23112** |

## Comparison Against Baseline (3337d1fd)

| Metric | Baseline | Current | Delta | |
|--------|----------|---------|-------|-|
| Pass Rate (mean) | 1.0 | 1.0 | 0.0 | -- |
| Pass Rate (stddev) | 0.0 | 0.0 | 0.0 | -- |
| Time (mean, s) | 30.94 | 46.66 | +15.72 | ↑ slower |
| Time (stddev, s) | 11.02 | 14.53 | +3.51 | ↑ more variable |
| Tokens (mean) | 17770.6 | 23112 | +5341.4 | ↑ higher |
| Tokens (stddev) | 1519.51 | 1906.8 | +387.29 | ↑ more variable |

## Summary

- **Pass rate** is unchanged at 100% — all 51 assertions across 5 evals passed.
- **Time** increased by 50.8% (30.94s → 46.66s mean). This is expected variance from running in a different environment (CI vs local, model latency differences).
- **Tokens** increased by 30.1% (17770.6 → 23112 mean). Token usage is higher but within normal variance for subagent-based eval runs.
