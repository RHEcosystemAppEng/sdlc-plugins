# Criterion 2 — PASS

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## What was checked
The `None` arm of the new `match` in `advisory_summary` (`modules/fundamental/src/advisory/endpoints/get.rs`), plus the new `Query<SummaryParams>` extractor.

## What was found
- `SummaryParams.threshold` is `Option<String>`. Axum's `Query` extractor deserializes a missing parameter as `None`, so requests with no query string still succeed.
- `None => summary` returns the `AdvisorySummary` from `aggregate_severities` unchanged: critical, high, medium, low and total.
- The response struct and aggregation service are unchanged, so the response shape is identical to before the PR.

Caveat: no test was added for this case, although the Test Requirements list "no threshold returns all four severity counts". This counts against test coverage, not against this criterion. Backward compatibility holds from static inspection of the code.

**Verdict: PASS.**
