# Criterion 5: Response includes threshold_applied boolean field

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict:** FAIL

## Analysis

The PR does NOT add a `threshold_applied` boolean field to the response. Examining the `AdvisorySummary` struct construction in the filtering branch:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The constructed response contains only the existing fields: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field.

Furthermore, the `AdvisorySummary` struct definition is not modified anywhere in the diff. The diff for `modules/fundamental/src/advisory/service/advisory.rs` shows no changes to the struct -- only unchanged context lines around the existing `aggregate_severities` method.

The `None` branch also returns the original `summary` without a `threshold_applied` field:

```rust
None => summary,
```

## What should have been implemented

The `AdvisorySummary` struct (likely in `modules/fundamental/src/advisory/model/summary.rs`) should have been extended with:

```rust
pub threshold_applied: bool,
```

And the response construction should set:
- `threshold_applied: true` when a threshold parameter is provided
- `threshold_applied: false` when no threshold is provided (backward compatible default)

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- no `threshold_applied` field in the `AdvisorySummary` construction
- File: `modules/fundamental/src/advisory/service/advisory.rs` -- no changes to the struct definition
- File: `modules/fundamental/src/advisory/model/summary.rs` -- not present in the diff at all, meaning the `AdvisorySummary` struct was not modified
- The acceptance criterion explicitly requires this field in the response
