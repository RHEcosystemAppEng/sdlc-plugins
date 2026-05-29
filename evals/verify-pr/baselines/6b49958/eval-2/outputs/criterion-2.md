# Criterion 2: Backward compatibility without threshold parameter

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict: PASS**

## Analysis

The PR diff shows that the `threshold` parameter is defined as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

When no threshold is provided, `params.threshold` is `None`, and the code falls through to the `None` arm of the match:

```rust
None => summary,
```

This returns the unmodified `summary` object with all severity counts, which preserves backward compatibility.

**Evidence:**
- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `SummaryParams` struct uses `Option<String>` for the threshold field
- The `None` branch of the match returns the original unfiltered summary

**Conclusion:** This criterion PASSES. The endpoint behaves identically to the original when no threshold parameter is provided.
