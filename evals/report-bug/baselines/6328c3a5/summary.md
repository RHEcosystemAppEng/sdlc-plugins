# report-bug Eval Results

## Individual Eval Results

| Eval | Scenario | Assertions | Pass Rate | Time (s) | Tokens |
|------|----------|------------|-----------|----------|--------|
| eval-1 | Interactive Complete | 14/14 | 100% | 42 | 19217 |
| eval-2 | Interactive Partial | 10/10 | 100% | 34 | 18439 |
| eval-3 | Missing Bug Configuration | 6/6 | 100% | 16 | 15704 |
| eval-4 | Programmatic Mode | 13/13 | 100% | 39 | 19419 |
| eval-5 | Adversarial | 8/8 | 100% | 50 | 20000 |
| **Aggregate** | | **51/51** | **100%** | **36.2** | **18555.8** |

## Comparison Against Baseline (14692f2)

| Metric | Baseline | Current | Delta | |
|--------|----------|---------|-------|-|
| Pass Rate (mean) | 1.0 | 1.0 | 0.0 | -- |
| Pass Rate (stddev) | 0.0 | 0.0 | 0.0 | -- |
| Time (mean, s) | 30.74 | 36.2 | +5.46 | ↑ slower |
| Time (stddev, s) | 7.98 | 11.36 | +3.38 | ↑ higher variance |
| Tokens (mean) | 18853.8 | 18555.8 | -298.0 | ↓ improved |
| Tokens (stddev) | 1076.34 | 1511.01 | +434.67 | ↑ higher variance |

## Summary

- **Pass rate** is unchanged at 100% — all 51 assertions across 5 evals passed.
- **Time** increased by 17.8% (30.74s → 36.2s mean), with higher variance (stddev 7.98 → 11.36). The adversarial eval (50s) was the slowest.
- **Tokens** improved slightly by 1.6% (18853.8 → 18555.8 mean), with higher variance (stddev 1076.34 → 1511.01).
