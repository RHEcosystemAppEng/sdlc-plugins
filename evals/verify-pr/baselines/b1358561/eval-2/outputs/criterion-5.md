# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict: NOT MET (FAIL)**

## Evidence

The only `AdvisorySummary` construction in the diff:

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

- The struct literal has no `threshold_applied` field.
- `modules/fundamental/src/advisory/model/summary.rs`, which defines `AdvisorySummary`, is not modified.
- No other file adds the field.
- Neither the `Some(threshold)` nor the `None` branch sets any filtering indicator. Clients cannot tell whether filtering is active, which makes the zeroed counts ambiguous.

## Expected fix

Add `threshold_applied: bool` to the response model. Set it to `true` when a valid threshold is supplied and `false` otherwise.
