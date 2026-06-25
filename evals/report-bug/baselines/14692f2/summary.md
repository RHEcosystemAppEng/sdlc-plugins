# report-bug Eval Results

## Individual Eval Results

| Eval | Scenario | Assertions | Pass Rate | Time (s) | Tokens |
|------|----------|------------|-----------|----------|--------|
| eval-1 | Interactive Complete | 13/13 | 100% | 35.4 | 19499 |
| eval-2 | Interactive Partial | 9/9 | 100% | 24.9 | 18682 |
| eval-3 | Missing Bug Configuration | 6/6 | 100% | 19.6 | 16853 |
| eval-4 | Programmatic Mode | 12/12 | 100% | 31.3 | 19320 |
| eval-5 | Adversarial | 7/7 | 100% | 42.5 | 19915 |
| **Aggregate** | | **47/47** | **100%** | **30.74** | **18853.8** |

## Comparison Against Baseline (bae6630)

| Metric | Baseline | Current | Delta | |
|--------|----------|---------|-------|-|
| Pass Rate (mean) | 1.0 | 1.0 | 0.0 | -- |
| Pass Rate (stddev) | 0.0 | 0.0 | 0.0 | -- |
| Time (mean, s) | 58.6 | 30.74 | -27.86 | ↓ improved |
| Time (stddev, s) | 15.23 | 7.98 | -7.25 | ↓ improved |
| Tokens (mean) | 26828 | 18853.8 | -7974.2 | ↓ improved |
| Tokens (stddev) | 3318.49 | 1076.34 | -2242.15 | ↓ improved |

## Summary

- **Pass rate** is unchanged at 100% — all 47 assertions across 5 evals passed.
- **Time** improved by 47.5% (58.6s → 30.74s mean), with lower variance (stddev 15.23 → 7.98).
- **Tokens** improved by 29.7% (26828 → 18853.8 mean), with lower variance (stddev 3318.49 → 1076.34).
