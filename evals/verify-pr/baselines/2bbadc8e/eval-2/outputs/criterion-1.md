# Criterion 1: Threshold=high returns counts for critical and high only

## Criterion
`GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: PASS

## Reasoning

The diff in `get.rs` adds threshold filtering logic. When `threshold=high`, the code:

1. Looks up `"high"` in `severity_order = ["critical", "high", "medium", "low"]`
2. Finds index 1 (`threshold_idx = 1`)
3. Builds a filtered `AdvisorySummary`:
   - `critical`: always included (`summary.critical`)
   - `high`: included because `threshold_idx <= 1` is true (1 <= 1)
   - `medium`: excluded because `threshold_idx <= 2` is false (1 <= 2 is true — wait)

**Re-evaluation:** Actually, the condition `if threshold_idx <= 2` for medium evaluates to `1 <= 2` which is TRUE. This means medium IS included when threshold=high. This is INCORRECT — when threshold=high, only critical and high should be returned, but medium is also included.

However, looking more carefully at the indexing logic:
- `threshold_idx = 1` (position of "high")
- `high`: `threshold_idx <= 1` → `1 <= 1` → true (correct, include high)
- `medium`: `threshold_idx <= 2` → `1 <= 2` → true (INCORRECT — medium should be excluded when threshold=high)

**Revised Verdict: FAIL**

The filtering logic is wrong. When `threshold=high`, medium and low should be zeroed out, but the index comparison `threshold_idx <= 2` incorrectly includes medium. The threshold filtering does not correctly limit counts to only critical and high.

The correct logic should compare against the threshold position differently — the condition should be `threshold_idx >= position_of_severity` rather than `threshold_idx <= position_of_severity`.

Wait, let me re-read the logic again more carefully:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

For threshold=high: threshold_idx = 1

```rust
high: if threshold_idx <= 1 { summary.high } else { 0 },
medium: if threshold_idx <= 2 { summary.medium } else { 0 },
low: if threshold_idx <= 3 { summary.low } else { 0 },
```

- high: 1 <= 1 = true → included
- medium: 1 <= 2 = true → included (BUG: should be excluded)
- low: 1 <= 3 = true → included (BUG: should be excluded)

**Final Verdict: FAIL**

The threshold filtering logic is incorrect. When threshold=high, all four severities are still included because the comparison logic is inverted. The conditions should check whether the severity level's index is <= threshold_idx (i.e., the severity is at or above the threshold), not whether threshold_idx <= the severity's position.
