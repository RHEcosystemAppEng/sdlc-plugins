# Criterion 2: Without threshold returns all severity counts (backward compatible)

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict:** PASS

## Analysis

The PR adds the `SummaryParams` struct with `threshold: Option<String>`, making the parameter optional. When no `threshold` query parameter is provided, `params.threshold` is `None`.

The filtering logic uses a `match` expression:
```rust
let filtered = match &params.threshold {
    Some(threshold) => { /* filtering logic */ }
    None => summary,
};
```

When `params.threshold` is `None`, the code falls through to the `None => summary` arm, returning the unmodified `summary` directly. This preserves the original behavior -- all severity counts (critical, high, medium, low) are returned unchanged.

## Conclusion

The backward compatibility path is correctly implemented. When no threshold is provided, the endpoint returns the full unfiltered summary exactly as it did before the change.
