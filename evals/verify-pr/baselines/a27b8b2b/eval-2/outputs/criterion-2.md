## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict: PASS**

### Analysis

The PR correctly handles the case when no threshold parameter is provided. The `SummaryParams` struct defines `threshold` as `Option<String>`, and the handler uses a `match` expression on `params.threshold`:

```rust
None => summary,
```

When no threshold query parameter is supplied, the `None` arm returns the original `summary` object unchanged. This preserves full backward compatibility -- all four severity counts (critical, high, medium, low) and the existing total are returned as-is.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `None` match arm passes through the unmodified `summary` struct
- No transformation is applied when the threshold parameter is absent
