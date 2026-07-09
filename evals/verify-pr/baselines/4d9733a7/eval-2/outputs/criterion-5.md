## Criterion 5: Response includes a threshold_applied boolean field

**Verdict: FAIL**

### Requirement

Response includes a `threshold_applied` boolean field indicating whether filtering is active.

### Analysis

The PR diff does not add a `threshold_applied` field to the response. The constructed `AdvisorySummary` in the filtered branch contains only the severity count fields and `total`:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

No `threshold_applied` field is set in either the `Some(threshold)` branch (where it should be `true`) or the `None` branch (where it should be `false`).

Furthermore, the diff does not modify the `AdvisorySummary` struct definition (located in `modules/fundamental/src/advisory/model/summary.rs` per the repo structure). The struct would need a new boolean field added to support this requirement. The diff only touches `endpoints/get.rs` and `service/advisory.rs`, but `model/summary.rs` is not modified.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 47-53 in the diff -- no `threshold_applied` field in the constructed `AdvisorySummary`
- File: `modules/fundamental/src/advisory/model/summary.rs` -- not modified in the diff, so the `AdvisorySummary` struct does not have a `threshold_applied` field
- The `None` branch returns the original `summary` as-is, also without `threshold_applied`
- Clients cannot determine from the response whether threshold filtering was applied

### Conclusion

The `threshold_applied` boolean field is completely absent from the implementation. Neither the response struct nor the endpoint handler includes this field. The criterion is not satisfied.
