## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

### Verdict: PASS

### What was checked

The PR diff was inspected for the code path when no `threshold` query parameter is provided. The expected behavior is that all four severity counts (critical, high, medium, low) are returned unchanged, preserving backward compatibility with existing clients.

### Evidence

In `modules/fundamental/src/advisory/endpoints/get.rs`, the `threshold` parameter is declared as `Option<String>` in the `SummaryParams` struct:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

The filtering logic handles the `None` case explicitly:

```rust
let filtered = match &params.threshold {
    Some(threshold) => { /* filtering logic */ }
    None => summary,
};
```

When `threshold` is not provided (`None`), the original `summary` is returned as-is without any modification. This preserves the existing response format and all severity counts.

### Conclusion

Backward compatibility is maintained. Requests without a `threshold` parameter continue to receive the full, unfiltered advisory summary.
