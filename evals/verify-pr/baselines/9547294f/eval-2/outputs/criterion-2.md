# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The handler checks `params.threshold` via a `match` expression:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the original `summary` (with all severity counts) is returned directly via `Ok(Json(filtered))`.

The `SummaryParams` struct uses `Option<String>` for the threshold field, which correctly makes it optional in the query string:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

## Evidence

- The `None` branch of the match returns the unmodified `summary` object
- The `SummaryParams.threshold` field is `Option<String>`, making the parameter optional
- The existing aggregation logic in `advisory.rs` is unchanged (the diff shows no modifications to the `aggregate_severities` method)

## Verdict Rationale

This criterion is satisfied. Backward compatibility is preserved -- when no threshold parameter is provided, the endpoint behaves identically to its pre-change behavior, returning all four severity counts.
