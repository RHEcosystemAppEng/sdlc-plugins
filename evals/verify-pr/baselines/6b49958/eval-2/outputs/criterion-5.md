# Criterion 5: Response includes threshold_applied boolean field

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict: FAIL**

## Analysis

The PR diff constructs an `AdvisorySummary` struct in the filtered response:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

There is no `threshold_applied` field in this struct construction. The fields present are: `critical`, `high`, `medium`, `low`, and `total`. A `threshold_applied: bool` field is completely absent.

For this criterion to be satisfied, the `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repository structure) would need to be updated to include a `threshold_applied: bool` field, and the handler would need to set it to `true` when a threshold is provided and `false` otherwise. Neither change appears in the diff.

Furthermore, the `advisory.rs` service file diff shows no structural changes -- no new field is added to the aggregation output:

```rust
impl AdvisoryService {
    low: counts.get("low").copied().unwrap_or(0),
    total: counts.values().sum(),
```

The model file `modules/fundamental/src/advisory/model/summary.rs` is not modified in the PR at all.

**Evidence:**
- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- the `AdvisorySummary` struct construction has no `threshold_applied` field
- File: `modules/fundamental/src/advisory/model/summary.rs` -- not modified in the PR diff
- The `None => summary` branch also does not add a `threshold_applied: false` field

**Conclusion:** This criterion FAILS. The `threshold_applied` boolean field is completely missing from the response.
