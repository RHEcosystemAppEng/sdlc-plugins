# report-bug Eval Results

## Individual Eval Results

| Eval | Scenario | Assertions | Pass Rate | Time (s) | Tokens |
|------|----------|------------|-----------|----------|--------|
| eval-1 | Interactive Complete | 13/13 | 100% | 41.5 | 20272 |
| eval-2 | Interactive Partial | 9/9 | 100% | 36.5 | 19711 |
| eval-3 | Missing Bug Configuration | 6/6 | 100% | 20.9 | 17210 |
| eval-4 | Programmatic Mode | 12/12 | 100% | 37.9 | 19938 |
| eval-5 | Adversarial | 7/7 | 100% | 51.3 | 20541 |
| **Aggregate** | | **47/47** | **100%** | **37.62** | **19534.4** |

## Comparison Against Baseline (14692f2)

| Metric | Baseline | Current | Delta | |
|--------|----------|---------|-------|-|
| Pass Rate (mean) | 1.0 | 1.0 | 0.0 | -- |
| Pass Rate (stddev) | 0.0 | 0.0 | 0.0 | -- |
| Time (mean, s) | 30.74 | 37.62 | +6.88 | ↑ slower |
| Time (stddev, s) | 7.98 | 10.17 | +2.19 | ↑ |
| Tokens (mean) | 18853.8 | 19534.4 | +680.6 | ↑ |
| Tokens (stddev) | 1076.34 | 1168.49 | +92.15 | ↑ |

## Summary

- **Pass rate** is unchanged at 100% — all 47 assertions across 5 evals passed.
- **Time** increased by 22.4% (30.74s -> 37.62s mean), within normal variance for agent-based evals.
- **Tokens** increased by 3.6% (18853.8 -> 19534.4 mean), a minor increase within noise range.
