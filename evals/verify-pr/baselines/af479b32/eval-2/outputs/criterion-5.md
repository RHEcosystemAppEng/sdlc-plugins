# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Reasoning

The diff does not add a `threshold_applied` boolean field to the response. The `AdvisorySummary` struct is not modified anywhere in the diff to include this field.

### Code Analysis

The filtered response constructs an `AdvisorySummary` with only severity count fields and a total:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields present are: `critical`, `high`, `medium`, `low`, `total`. There is no `threshold_applied` field.

### What's Missing

1. The `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repo structure) is not modified in the diff to add a `threshold_applied: bool` field
2. The response construction does not set `threshold_applied: true` when a threshold is provided
3. The `None` branch returns the original summary as-is, which also lacks a `threshold_applied: false` field

### Expected Implementation

The `AdvisorySummary` struct should include:
```rust
pub threshold_applied: bool,
```

And the handler should set:
- `threshold_applied: true` when `params.threshold` is `Some(_)`
- `threshold_applied: false` when `params.threshold` is `None`

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- no `threshold_applied` field in the `AdvisorySummary` construction
- File: `modules/fundamental/src/advisory/model/summary.rs` -- not modified in the diff (no struct change)
- The response JSON will not contain a `threshold_applied` key
