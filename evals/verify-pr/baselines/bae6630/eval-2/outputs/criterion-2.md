## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

### Result: PASS

### Evidence

In `modules/fundamental/src/advisory/endpoints/get.rs`, the `None` arm of the match statement returns the original summary unmodified:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the original `summary` object (containing all four severity counts and the total) is returned directly. This preserves backward compatibility.

The `SummaryParams` struct uses `Option<String>` for the threshold field:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

This means the parameter is optional and defaults to `None` when not provided in the query string.

### Conclusion

The backward-compatible behavior is correctly preserved. Requests without the `threshold` parameter receive the full, unfiltered advisory summary.
