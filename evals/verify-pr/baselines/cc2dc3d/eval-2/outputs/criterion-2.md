## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict: PASS**

### Analysis

The code handles the `None` case for `params.threshold` by returning the original `summary` unmodified:

```rust
None => summary,
```

This preserves backward compatibility: when no `threshold` query parameter is provided, the endpoint returns the full aggregated summary with all four severity counts (critical, high, medium, low) exactly as it did before.

The `SummaryParams` struct defines `threshold` as `Option<String>`, so omitting the parameter results in `None`, which triggers this branch.

### Evidence

Lines 41-56 of the diff in `get.rs`:
```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

The original endpoint returned `Ok(Json(summary))`. The new code returns `Ok(Json(filtered))`, and when threshold is `None`, `filtered` is assigned the unmodified `summary`. The behavior is identical.
