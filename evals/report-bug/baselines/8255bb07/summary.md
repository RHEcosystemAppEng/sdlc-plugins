# report-bug Eval Results

## Individual Eval Results

| Eval | Scenario | Assertions | Pass Rate | Time (s) | Tokens |
|------|----------|------------|-----------|----------|--------|
| eval-1 | Interactive Complete | 13/13 | 100% | 38.9 | 20084 |
| eval-2 | Interactive Partial | 9/9 | 100% | 37.0 | 19641 |
| eval-3 | Missing Bug Configuration | 6/6 | 100% | 19.3 | 17261 |
| eval-4 | Programmatic Mode | 12/12 | 100% | 40.8 | 20081 |
| eval-5 | Adversarial | 7/7 | 100% | 59.6 | 20978 |
| **Aggregate** | | **47/47** | **100%** | **39.12** | **19609.0** |

## Comparison Against Baseline (7b46435b)

| Metric | Baseline | Current | Delta | |
|--------|----------|---------|-------|-|
| Pass Rate (mean) | 1.0 | 1.0 | 0.0 | -- |
| Pass Rate (stddev) | 0.0 | 0.0 | 0.0 | -- |
| Time (mean, s) | 59.03 | 39.12 | -19.91 | ↓ improved |
| Time (stddev, s) | 15.27 | 12.8 | -2.47 | ↓ improved |
| Tokens (mean) | 27544.2 | 19609.0 | -7935.2 | ↓ improved |
| Tokens (stddev) | 3807.38 | 1251.94 | -2555.44 | ↓ improved |

## Summary

- **Pass rate** is unchanged at 100% — all 47 assertions across 5 evals passed.
- **Time** improved by 33.7% (59.03s → 39.12s mean), with lower variance (stddev 15.27 → 12.8).
- **Tokens** improved by 28.8% (27544.2 → 19609.0 mean), with significantly lower variance (stddev 3807.38 → 1251.94).
