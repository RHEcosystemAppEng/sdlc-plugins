## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Result: PASS**

### Evidence

The code in `get.rs` handles the `None` case for the threshold parameter:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the original `summary` object (containing all severity counts from the aggregation query) is returned unchanged. This preserves the existing response format and all severity data.

The `SummaryParams` struct uses `Option<String>` for the threshold field:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

This means the parameter is optional in the query string, maintaining backward compatibility.

### Conclusion

This criterion passes. The endpoint returns all severity counts when no threshold parameter is specified, preserving backward compatibility.
