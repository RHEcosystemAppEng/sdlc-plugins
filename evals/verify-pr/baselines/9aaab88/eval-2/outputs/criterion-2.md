# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` handles the `None` case for the threshold parameter:

```rust
None => summary,
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the code returns the original `summary` object unmodified. This preserves the original behavior -- all severity counts (critical, high, medium, low) are returned along with the existing total.

The `SummaryParams` struct uses `Option<String>` for the threshold field, which means Axum's `Query` extractor will parse the absence of the parameter as `None` without error.

## Conclusion

**PASS** -- The backward-compatible behavior is correctly preserved. When no threshold is provided, the full summary is returned unchanged.
