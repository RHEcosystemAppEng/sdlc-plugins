# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The `None` branch of the match statement preserves backward compatibility by returning the original summary unchanged:

```rust
None => summary,
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the handler returns the unmodified `AdvisorySummary` from `AdvisoryService::aggregate_severities()`. This includes all four severity counts (critical, high, medium, low) and the total, exactly as before the change.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 55-56 in the diff
- The `SummaryParams` struct declares `threshold: Option<String>`, so it defaults to `None` when omitted from the query string
- The `None` arm returns the original `summary` without modification
