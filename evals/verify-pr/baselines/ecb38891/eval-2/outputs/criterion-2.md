# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Reasoning

The PR correctly handles the case when no threshold parameter is provided, preserving backward compatibility.

### Code Under Review

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

### Analysis

The `SummaryParams` struct defines `threshold` as `Option<String>`:

```rust
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

When no `threshold` query parameter is provided, the `params.threshold` field is `None`, and the `match` arm `None => summary` returns the unmodified `summary` object from `AdvisoryService::aggregate_severities()`. This preserves the exact behavior of the original endpoint (which previously returned `Ok(Json(summary))` directly).

The backward compatibility requirement is satisfied.
