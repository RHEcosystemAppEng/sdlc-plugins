# Criterion 2 — PASS

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## What was checked
- `SummaryParams { threshold: Option<String> }` extracted with `Query(params): Query<SummaryParams>` in `modules/fundamental/src/advisory/endpoints/get.rs`.
- The `None => summary` arm of the `match &params.threshold` block.

## What was found
- `threshold` is an `Option<String>`, so when the query string has no `threshold`, serde deserializes it to `None` and the `Query` extractor succeeds. Callers that send no parameters are not rejected.
- In the `None` arm, the `AdvisorySummary` from `AdvisoryService::aggregate_severities` is returned unchanged (`None => summary`, then `Ok(Json(filtered))`). That is the same as the old `Ok(Json(summary))`.
- The diff does not change the response struct (`AdvisorySummary`), so the JSON shape stays the same for existing callers.

## Caveats
- No test was added for this case. The Test Requirement "Test no threshold returns all four severity counts" is not met, because `tests/api/advisory_summary.rs` was not created. This verdict comes from static analysis of the handler only.

**Verdict: PASS**
