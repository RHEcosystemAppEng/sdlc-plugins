# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Reasoning

The `None` branch of the threshold match in `modules/fundamental/src/advisory/endpoints/get.rs` returns the original `summary` unchanged:

```rust
None => summary,
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the unmodified `AdvisorySummary` is returned directly. This preserves the existing behavior and maintains backward compatibility. The existing SBOM fetch and severity aggregation logic is untouched, and the response format for the no-threshold case is identical to the pre-change behavior.
