# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Reasoning

When the `threshold` query parameter is not provided, the `params.threshold` field is `None` (since it is defined as `Option<String>` in the `SummaryParams` struct). The code handles this correctly:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

When `params.threshold` is `None`, the code falls through to the `None =>` arm and returns the original `summary` object unmodified. This preserves all four severity counts (critical, high, medium, low) and the total, maintaining full backward compatibility with the existing endpoint behavior.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `None => summary` branch returns the unfiltered aggregation result
- The `SummaryParams` struct uses `Option<String>` for the threshold field, making it truly optional
- No default threshold is applied when the parameter is absent
