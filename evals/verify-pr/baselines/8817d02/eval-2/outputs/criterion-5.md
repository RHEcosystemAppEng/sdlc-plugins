# Criterion 5: Response includes threshold_applied boolean

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict:** FAIL

## Reasoning

The PR diff does not add a `threshold_applied` boolean field to the response. Examining the `AdvisorySummary` struct construction in the diff:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The constructed `AdvisorySummary` contains only `critical`, `high`, `medium`, `low`, and `total` fields. There is no `threshold_applied` field.

Additionally, the `None` branch returns the unfiltered `summary` directly, which also would not contain a `threshold_applied` field.

**What should exist:** The response struct should include a `threshold_applied: bool` field that is:
- `true` when a valid threshold parameter is provided
- `false` when no threshold parameter is provided

**What is missing:**
1. No modification to the `AdvisorySummary` struct (in `modules/fundamental/src/advisory/model/summary.rs`) to add the `threshold_applied` field
2. No setting of `threshold_applied` in either the `Some` or `None` arms of the match expression
3. The model file `summary.rs` does not appear in the diff at all

**Evidence:**
- Lines 47-53 of the diff show the `AdvisorySummary` struct literal with only severity count fields and `total`
- No reference to `threshold_applied` anywhere in the diff
- The `AdvisorySummary` model definition (in `modules/fundamental/src/advisory/model/summary.rs` per the repo structure) is not modified in the diff
