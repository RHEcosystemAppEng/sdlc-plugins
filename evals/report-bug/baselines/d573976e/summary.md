# report-bug Eval Results

## Individual Eval Results

| Eval | Scenario | Assertions | Pass Rate | Time (s) | Tokens |
|------|----------|------------|-----------|----------|--------|
| eval-1 | Interactive Complete | 13/13 | 100% | 33.6 | 19277 |
| eval-2 | Interactive Partial | 9/9 | 100% | 31.3 | 18755 |
| eval-3 | Missing Bug Configuration | 6/6 | 100% | 17.6 | 16583 |
| eval-4 | Programmatic Mode | 12/12 | 100% | 28.5 | 19176 |
| eval-5 | Adversarial | 7/7 | 100% | 43.0 | 19945 |
| **Aggregate** | | **47/47** | **100%** | **30.8** | **18747.2** |

## Comparison Against Baseline (14692f2)

| Metric | Baseline | Current | Delta | |
|--------|----------|---------|-------|-|
| Pass Rate (mean) | 1.0 | 1.0 | 0.0 | -- |
| Pass Rate (stddev) | 0.0 | 0.0 | 0.0 | -- |
| Time (mean, s) | 30.74 | 30.8 | +0.06 | -- |
| Time (stddev, s) | 7.98 | 8.2 | +0.22 | -- |
| Tokens (mean) | 18853.8 | 18747.2 | -106.6 | -- |
| Tokens (stddev) | 1076.34 | 1147.21 | +70.87 | -- |

## Summary

- **Pass rate** is unchanged at 100% — all 47 assertions across 5 evals passed.
- **Time** is essentially unchanged (30.74s → 30.8s mean), within noise.
- **Tokens** slightly improved by 0.6% (18853.8 → 18747.2 mean), within noise.
