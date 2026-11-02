# Criterion 5 — FAIL

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict:** FAIL

**Analysis:**

The `AdvisorySummary` struct constructed in the response does not include a `threshold_applied` field. The filtered response contains only the severity count fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields constructed are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied: bool` field in the response.

The `None` branch also returns the raw `summary` without adding a `threshold_applied: false` field.

Neither the `AdvisorySummary` struct definition (not shown in the diff but referenced) nor the construction code includes this field. The acceptance criteria require a boolean field so clients can distinguish between filtered and unfiltered responses.

**Evidence:**
- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 46–52
- The `AdvisorySummary` struct is constructed with 5 fields: `critical`, `high`, `medium`, `low`, `total`
- No `threshold_applied` field appears anywhere in the diff
- The `None` branch returns the unmodified `summary` which also lacks this field
