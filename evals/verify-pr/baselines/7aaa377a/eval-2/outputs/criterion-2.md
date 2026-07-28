# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The diff correctly handles the case where no `threshold` query parameter is provided. The `SummaryParams` struct declares `threshold` as `Option<String>`, and the match arm for `None` returns the unmodified summary directly.

## Evidence

From the diff in `modules/fundamental/src/advisory/endpoints/get.rs`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

And the match expression:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

When no `threshold` parameter is provided, `params.threshold` is `None`, and the code returns the original `summary` unchanged. This preserves backward compatibility -- the endpoint returns all severity counts exactly as it did before this change.

## Conclusion

This criterion is satisfied. The `None` branch returns the unmodified summary, preserving full backward compatibility for requests without a threshold parameter.
