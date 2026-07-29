# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Reasoning

The code correctly handles the case where no `threshold` query parameter is provided. The `SummaryParams` struct defines `threshold` as `Option<String>`:

```rust
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

In the `advisory_summary` handler, the match expression handles the `None` case by returning the original, unfiltered summary:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

When no `threshold` parameter is present in the query string, `params.threshold` is `None`, and the original `summary` (containing all severity counts: critical, high, medium, low, and total) is returned unchanged.

This preserves backward compatibility -- existing API consumers that do not pass a `threshold` parameter will continue to receive the same response format and data as before this change.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `None` branch of the match returns the unmodified `summary` from `AdvisoryService::aggregate_severities`
- No changes were made to the `AdvisoryService::aggregate_severities` method itself (the diff for `advisory.rs` shows only a blank line addition)
