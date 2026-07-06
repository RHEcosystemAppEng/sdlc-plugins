## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict: PASS**

### Analysis

This criterion requires that omitting the `threshold` query parameter returns the full, unfiltered advisory summary with all severity counts, preserving backward compatibility with the existing API behavior.

### Code Inspection

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` handles the absence of a threshold via pattern matching:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

When `params.threshold` is `None` (no query parameter provided), the code returns the original `summary` object unchanged. This preserves the existing response format and all severity counts.

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`
- **Branch:** `None => summary` correctly returns the unmodified aggregation result
- **Backward compatibility:** The `SummaryParams` struct uses `Option<String>` for `threshold`, making it optional in the query string. Requests without the parameter work exactly as they did before this change.
