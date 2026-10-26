# report-bug Eval Results

## Individual Eval Results

| Eval | Scenario | Assertions | Pass Rate | Time (s) | Tokens |
|------|----------|------------|-----------|----------|--------|
| eval-1 | Interactive Complete | 14/14 | 100% | 45.9 | 19290 |
| eval-2 | Interactive Partial | 10/10 | 100% | 39.1 | 18591 |
| eval-3 | Missing Bug Configuration | 6/6 | 100% | 16.3 | 15686 |
| eval-4 | Programmatic Mode | 13/13 | 100% | 47.4 | 19318 |
| eval-5 | Adversarial | 8/8 | 100% | 71.7 | 20601 |
| **Aggregate** | | **51/51** | **100%** | **44.08** | **18697.2** |

## Comparison Against Baseline (f32bd713)

| Metric | Baseline | Current | Delta | |
|--------|----------|---------|-------|-|
| Pass Rate (mean) | 1.0 | 1.0 | 0.0 | -- |
| Pass Rate (stddev) | 0.0 | 0.0 | 0.0 | -- |
| Time (mean, s) | 45.28 | 44.08 | -1.20 | ↓ improved |
| Time (stddev, s) | 7.69 | 17.74 | +10.05 | ↑ regressed |
| Tokens (mean) | 20926.6 | 18697.2 | -2229.40 | ↓ improved |
| Tokens (stddev) | 3740.21 | 1639.5 | -2100.71 | ↓ improved |

## Summary

- **Pass rate** is unchanged at 100% — all 51 assertions across 5 evals passed.
- **Time** mean improved slightly (45.28s → 44.08s), but stddev increased (7.69 → 17.74) due to the adversarial eval taking longer (71.7s).
- **Tokens** improved by 10.7% (20926.6 → 18697.2 mean), with lower variance (stddev 3740.21 → 1639.5).
