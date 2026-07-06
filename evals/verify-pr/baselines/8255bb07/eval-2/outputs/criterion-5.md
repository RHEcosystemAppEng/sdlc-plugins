## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict: FAIL**

### Analysis

This criterion requires that the API response includes a `threshold_applied` boolean field that indicates whether threshold filtering is active (`true` when a threshold parameter is provided, `false` otherwise).

### Code Inspection

The filtered response is constructed in `modules/fundamental/src/advisory/endpoints/get.rs`:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The `AdvisorySummary` struct in the response contains only severity count fields (`critical`, `high`, `medium`, `low`, `total`). There is no `threshold_applied` boolean field anywhere in the response.

Neither the `AdvisorySummary` struct definition (in `modules/fundamental/src/advisory/model/summary.rs`, not modified in this PR) nor the endpoint handler adds a `threshold_applied` field. The `None => summary` branch also returns the unmodified `AdvisorySummary` without any additional field.

### What Should Happen

The response struct should be extended (or a wrapper struct created) to include a `threshold_applied: bool` field:

- When `params.threshold` is `Some(...)` and valid: `threshold_applied: true`
- When `params.threshold` is `None`: `threshold_applied: false`

This would require either modifying the `AdvisorySummary` struct or creating a new response wrapper that includes both the summary data and the `threshold_applied` indicator.

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`
- **Defect:** No `threshold_applied` field exists in the response
- **Expected behavior:** Response JSON includes `"threshold_applied": true` when threshold is provided, `"threshold_applied": false` otherwise
- **Actual behavior:** Response contains only `critical`, `high`, `medium`, `low`, and `total` fields
- **Struct definition:** `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` was not modified to add the field
