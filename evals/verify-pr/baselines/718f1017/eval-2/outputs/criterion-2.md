## Criterion 2

**Text**: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict**: PASS

**Evidence**: In `modules/fundamental/src/advisory/endpoints/get.rs`, the `SummaryParams` struct declares `threshold` as `Option<String>`, meaning it is not required. The match expression at lines 41-56 handles the `None` case explicitly:

```rust
None => summary,
```

When no threshold query parameter is provided, `params.threshold` is `None`, and the original unmodified `summary` is returned directly. This preserves the existing behavior -- all severity counts (critical, high, medium, low) are returned unchanged. Backward compatibility is maintained.
