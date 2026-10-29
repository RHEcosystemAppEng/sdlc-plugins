# Criterion 5: Response includes threshold_applied boolean field

## Criterion
Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Reasoning

The diff does not add a `threshold_applied` field to the response. Examining the filtering logic in `get.rs`:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ...filtering logic...
        AdvisorySummary {
            critical: summary.critical,
            high: if threshold_idx <= 1 { summary.high } else { 0 },
            medium: if threshold_idx <= 2 { summary.medium } else { 0 },
            low: if threshold_idx <= 3 { summary.low } else { 0 },
            total: summary.critical + summary.high + summary.medium + summary.low,
        }
    }
    None => summary,
};

Ok(Json(filtered))
```

The `AdvisorySummary` struct being constructed contains only `critical`, `high`, `medium`, `low`, and `total` fields. There is no `threshold_applied: bool` field.

Additionally, neither the `AdvisorySummary` struct definition in `modules/fundamental/src/advisory/model/summary.rs` nor the service layer in `advisory.rs` is modified to include a `threshold_applied` field — the diff for `advisory.rs` shows only a whitespace change (no structural modifications).

**What should happen:** The response should include `threshold_applied: true` when a threshold parameter is provided and `threshold_applied: false` (or the field absent) when no threshold is provided.

**What actually happens:** The field is entirely absent from the response struct and the implementation.

**Evidence:** The `AdvisorySummary` construction in the diff contains only `critical`, `high`, `medium`, `low`, `total` — no `threshold_applied` field. No modification to the model struct definition is present in the diff.
