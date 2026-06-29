# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

This criterion requires that when no `threshold` query parameter is provided, the endpoint returns all severity counts, preserving backward compatibility with the existing behavior.

### Code Inspection

The `SummaryParams` struct defines `threshold` as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

The filtering logic uses a `match` on `params.threshold`:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

When `threshold` is `None` (no query parameter provided), the `None` match arm returns the original `summary` unchanged. This correctly preserves all four severity counts and the total in the response.

### Evidence

- The `Option<String>` type allows the parameter to be absent
- The `None => summary` arm passes through the unmodified aggregation result
- No other code path modifies the response when threshold is absent

## Conclusion

This criterion PASSES. The backward compatibility is preserved -- when no threshold parameter is specified, the original summary with all severity counts is returned unmodified.
