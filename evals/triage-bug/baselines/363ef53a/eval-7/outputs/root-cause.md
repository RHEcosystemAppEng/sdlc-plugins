# Step 4: Root Cause Analysis

## Root Cause

The division operands in `compute_risk_score()` (`modules/risk/src/score.rs`) are reversed. The function computes `total_deps / vulnerable_deps` instead of the correct `vulnerable_deps / total_deps`.

### Current (buggy) code

```rust
pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64 {
    total_deps as f64 / vulnerable_deps as f64
}
```

### Correct behavior

```rust
pub fn compute_risk_score(total_deps: u32, vulnerable_deps: u32) -> f64 {
    vulnerable_deps as f64 / total_deps as f64
}
```

## Impact Summary

- **Severity**: High. Every risk assessment ever created contains an incorrect score.
- **Scope**: All assessments in the `assessments` table have inflated, inverted risk scores.
- **Persistence**: The buggy value is persisted at write time in `create_assessment()` and is never recomputed on read. A code-only fix corrects future assessments but leaves all historical data incorrect.
- **Required remediation**: Both a code fix and a data migration are needed.

## Why It Went Undetected

The only existing test (`test_risk_score_all_vulnerable`) uses `total_deps = 10, vulnerable_deps = 10`, producing `10 / 10 = 1.0` regardless of operand order. No test case exercises the asymmetric scenario where `total_deps != vulnerable_deps`.
