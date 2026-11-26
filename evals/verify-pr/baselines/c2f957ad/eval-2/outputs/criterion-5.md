# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict: FAIL**

## Evidence

The filtered response literal in `modules/fundamental/src/advisory/endpoints/get.rs`:

```rust
AdvisorySummary {
    critical: ...,
    high: ...,
    medium: ...,
    low: ...,
    total: ...,
}
```

## Reasoning

- The struct literal has only `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field.
- The response model `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary`) is not modified in the diff, so the field was never added to the serialized response type.
- The `None => summary` branch also returns the struct without the field. A client cannot tell from the response whether filtering was applied.
- No test checks the field.

The criterion is not met.
