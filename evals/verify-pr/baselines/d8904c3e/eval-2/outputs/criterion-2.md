# Criterion 2: Backward compatibility without threshold

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict:** PASS

## Analysis

In `modules/fundamental/src/advisory/endpoints/get.rs`, the `SummaryParams` struct declares `threshold` as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

When no `threshold` query parameter is provided, `params.threshold` will be `None`. The filtering logic handles this case in the `None` arm of the match:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

When `params.threshold` is `None`, the original unfiltered `summary` is returned directly with no modifications. This preserves backward compatibility -- existing clients calling the endpoint without a `threshold` parameter receive the same response as before the change.

The `SummaryParams` struct uses `Option<String>` for the threshold field, and Axum's `Query` extractor will deserialize a missing query parameter as `None`, which is the standard pattern. The `None` branch simply passes through the original summary unchanged.

**Conclusion:** This criterion is satisfied. The endpoint without a threshold parameter returns all severity counts, maintaining backward compatibility.
