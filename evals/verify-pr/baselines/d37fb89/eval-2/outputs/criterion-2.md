# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Reasoning

The diff handles the no-threshold case in the `None` branch of the match expression:

```rust
None => summary,
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the original `summary` is returned unchanged. This preserves full backward compatibility -- the response includes all severity counts (critical, high, medium, low) exactly as returned by `AdvisoryService::aggregate_severities()`.

The `SummaryParams` struct uses `Option<String>` for the `threshold` field, which correctly makes it optional in the query string.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `SummaryParams` struct: `pub threshold: Option<String>` -- optional field
- The `None` branch: `None => summary` -- returns unfiltered result
- No structural changes to the `AdvisorySummary` type that would break the existing response format (other than the missing `threshold_applied` field, which is a separate criterion)
