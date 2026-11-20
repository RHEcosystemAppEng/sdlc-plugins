# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict: FAIL**

## Reasoning

`threshold_applied` appears nowhere in the diff. The filtered response is built as:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: ...,
    medium: ...,
    low: ...,
    total: ...,
}
```

It has only `critical`, `high`, `medium`, `low` and `total`. The diff does not touch the `AdvisorySummary` model (`modules/fundamental/src/advisory/model/summary.rs`) or the service's construction of it (`advisory.rs`, context-only hunk). Neither the filtered branch nor the unfiltered branch (`None => summary`) can set a `threshold_applied` field.

Clients cannot tell from the response whether filtering is active. This matters more because filtered-out severities are returned as `0` rather than omitted.

## Evidence
- `get.rs`: the `AdvisorySummary { ... }` literal has no `threshold_applied` field
- `modules/fundamental/src/advisory/model/summary.rs` is not in the diff
- `advisory.rs` hunk has no added lines
