# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

This criterion requires that when no `threshold` query parameter is provided, the endpoint returns all severity counts unchanged, preserving backward compatibility.

### Code Inspection

The handler in `modules/fundamental/src/advisory/endpoints/get.rs` handles the `None` case for the threshold parameter:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

When `params.threshold` is `None`, the code returns the original `summary` struct without any modification. This preserves all severity counts (critical, high, medium, low, and total) exactly as they were before the threshold feature was added.

### Backward Compatibility Confirmed

- The `SummaryParams` struct uses `Option<String>` for the threshold field, making it optional
- Existing clients that do not send a `threshold` parameter will receive the full, unmodified summary
- No structural changes to the response format for the no-threshold case

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `None => summary` branch returns the unmodified aggregation result
- The `Query(params)` extraction with `Option<String>` makes the parameter optional
