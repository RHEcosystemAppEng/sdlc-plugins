# Criterion 2 — PASS

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## What was checked

- How `threshold` is declared and what happens when it is absent.
- Whether the response type or the aggregation changed.

## Findings

- `SummaryParams.threshold` is `Option<String>`. Axum's `Query` extractor deserializes a missing parameter to `None`, so existing requests without the parameter still work.
- The `None => summary` arm returns the result of `aggregate_severities` unchanged: critical, high, medium, low and total, as before.
- `aggregate_severities` in `advisory.rs` was not changed (that hunk is context only).
- The response type is still `Json<AdvisorySummary>`.

## Caveat

No test was added for the no-threshold case, which the Test Requirements ask for. The code path itself is backward compatible.

## Verdict

PASS
