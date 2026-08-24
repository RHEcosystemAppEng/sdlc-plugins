# Criterion 5 Analysis

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict:** FAIL

## Reasoning

The PR diff does not add a `threshold_applied` boolean field to the response. The `AdvisorySummary` struct is not modified anywhere in the diff.

### What the diff shows

The handler constructs an `AdvisorySummary` in the filtered case:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields are: `critical`, `high`, `medium`, `low`, `total`. There is no `threshold_applied` field.

### What is missing

1. The `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repository structure) needs a new `threshold_applied: bool` field
2. The handler must set this field to `true` when a threshold parameter is provided and `false` when it is not
3. The `aggregate_severities` method's return value would need to accommodate the new field, or it should be added at the handler level

### Impact

API consumers have no way to determine from the response whether the returned counts reflect all severities or a filtered subset. This is important for UI display and downstream processing, where the consumer needs to know if the data is complete or filtered.
