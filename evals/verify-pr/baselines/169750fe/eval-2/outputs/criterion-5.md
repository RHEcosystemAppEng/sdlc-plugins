# Criterion 5: Response includes a threshold_applied boolean field

## Verdict: FAIL

## Analysis

The acceptance criterion requires:
> Response includes a `threshold_applied` boolean field indicating whether filtering is active

### Evidence from the diff

In `modules/fundamental/src/advisory/endpoints/get.rs`, the filtered response is constructed as:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The `AdvisorySummary` struct returned contains only: `critical`, `high`, `medium`, `low`, and `total`. There is **no `threshold_applied` boolean field** anywhere in the response.

Additionally, reviewing the diff for `modules/fundamental/src/advisory/service/advisory.rs`, the `AdvisorySummary` struct definition was not modified to add a `threshold_applied` field. The struct retains its original fields without any additions.

### What should happen

The response should include a `threshold_applied: bool` field set to `true` when a threshold parameter is provided and `false` otherwise, so API consumers can programmatically determine whether the counts are filtered.

### Conclusion

The `threshold_applied` boolean field is entirely absent from both the response construction and the `AdvisorySummary` struct definition. This criterion is **not satisfied**.
