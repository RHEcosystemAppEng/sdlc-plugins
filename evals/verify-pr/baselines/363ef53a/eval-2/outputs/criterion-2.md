# Criterion 2: Backward compatibility without threshold parameter

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict:** PASS

## Analysis

The PR adds an optional `threshold` field to the `SummaryParams` struct:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

The `Option<String>` type ensures the parameter is optional. When no `threshold` query parameter is provided, `params.threshold` will be `None`.

The filtering logic handles this case explicitly:

```rust
let filtered = match &params.threshold {
    Some(threshold) => { /* filtering logic */ }
    None => summary,
};
```

When `params.threshold` is `None`, the original unfiltered `summary` is returned directly with no modifications. This preserves backward compatibility -- all four severity counts (critical, high, medium, low) plus the total are returned unchanged.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `SummaryParams.threshold` field is `Option<String>` (optional)
- The `None` branch returns the original `summary` unmodified
- No changes to the `AdvisorySummary` struct itself that would break existing responses (the struct is unchanged in `advisory.rs`)
