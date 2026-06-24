## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

### Result: FAIL

### Evidence

The task requires:
> Response includes a `threshold_applied` boolean field indicating whether filtering is active

Examining the filtered response construction in `modules/fundamental/src/advisory/endpoints/get.rs`:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The constructed `AdvisorySummary` contains only five fields: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field.

Additionally, examining the `None` branch:

```rust
None => summary,
```

The unmodified summary is returned as-is, also without a `threshold_applied` field.

Neither branch of the match expression includes a `threshold_applied` boolean. The `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs` based on the repository structure) would also need to be updated to include this field, but no changes to that file appear in the diff.

### What the code should do

1. Add a `threshold_applied: bool` field to the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs`
2. Set `threshold_applied: true` when a threshold parameter is provided and valid
3. Set `threshold_applied: false` when no threshold parameter is provided

### Conclusion

This criterion is not met. The `threshold_applied` boolean field is entirely absent from the response. Neither the model struct nor the endpoint handler includes this field.
