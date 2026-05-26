# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The filtering logic is wrapped in a `match` expression on `params.threshold`. When no `threshold` query parameter is provided, `params.threshold` is `None`, and the code falls through to the `None => summary` arm, returning the unmodified `summary` object from `AdvisoryService::aggregate_severities`.

This preserves backward compatibility: clients that do not supply the `threshold` parameter continue to receive the same response as before the change.

## Evidence

From the PR diff in `get.rs`, lines 41-56:
```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

The `None` arm returns `summary` unchanged, which is the same value that was previously returned directly via `Ok(Json(summary))` in the original code.
