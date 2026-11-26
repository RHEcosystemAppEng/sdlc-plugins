# Task 4 — Support optional `threshold` query parameter on advisory-summary (non-MVP)

**Summary:** TC-9001: Add optional ?threshold= severity filter to GET /api/v2/sbom/{id}/advisory-summary
**Issue type:** Task
**Labels:** ai-generated-jira
**Priority:** Major (inherited from TC-9001)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9001)

---

## Repository
trustify-backend

## Target Branch
main

## Description
Add an optional `?threshold=<severity>` query parameter to `GET /api/v2/sbom/{id}/advisory-summary`. When it is set, only counts at or above the given severity are returned. For example, `?threshold=critical` returns only the critical count. This supports alerting integrations that poll for critical advisories (UC-2).

This requirement is marked **non-MVP** in TC-9001. It is planned as a separate, independently mergeable task so the MVP endpoint (Tasks 1–3) can ship without it.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — accept an optional `threshold` query parameter (Axum `Query` extractor), validate it, and apply it to the response
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — make bucket fields optional in serialization (`#[serde(skip_serializing_if = "Option::is_none")]`) so buckets below the threshold are omitted, or add a filtering helper
- `modules/fundamental/src/sbom/endpoints/mod.rs` — make sure the cache key includes the query string, so thresholded and unthresholded responses are cached separately
- `tests/api/sbom.rs` — integration tests for the threshold parameter

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={critical|high|medium|low}` — MODIFY: new optional query param. When present, the response includes only the severity fields at or above the threshold, and `total` equals the sum of the included buckets. Without the param the response is unchanged. An invalid value returns `400`.

## Implementation Notes
- Severity ordering: `critical > high > medium > low`. Reuse the severity type from `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` and give it an `Ord`/rank helper if it doesn't already have one. Don't hard-code string comparisons.
- Filtering: apply the threshold to the already-computed (and cached) summary from `SbomService::advisory_severity_summary` (Task 1). No new SQL is needed. This keeps the threshold path within the same p95 budget.
- **Assumed semantics (confirm on TC-9001):** the feature text says "filter counts above a severity", while UC-2 says "only critical count is returned". This plan reads that as *at or above* the threshold, with lower buckets omitted from the JSON. If stakeholders want lower buckets zeroed instead of omitted, only the serialization changes.
- Validation: parse with a serde enum (`rename_all = "lowercase"`). An unknown value is rejected through `AppError` with a 400, following the existing bad-request mapping in `common/src/error.rs`.
- Cache: the Task 2 cache is keyed by SBOM ID. Either cache only the unfiltered summary and filter after the cache lookup (preferred, because Task 3's invalidation then still covers it), or add the threshold to the key. The preferred approach keeps invalidation unchanged.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` and map an invalid threshold to a 400 with `.context()`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler `.rs` scope.
- Per CONVENTIONS.md §Query helpers: if `common/src/db/query.rs` already parses filter or enum query parameters, reuse that parsing for `threshold`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint query-parameter scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/sbom.rs` using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/sbom.rs` matching the convention's `tests/api/` integration-test scope.
- Constraints (docs/constraints.md): §5.1, §5.2, §5.4 (reuse the severity type and summary computation), §5.9–5.13 (consider parameterized tests across the four threshold values if sibling tests use them, and add doc comments), §2.1–2.3, §3.1–3.3.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity type and values
- `common/src/db/query.rs` — shared query/filter parameter parsing helpers
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::advisory_severity_summary` — computed summary to filter (Task 1)

## Acceptance Criteria
- [ ] `?threshold=critical` returns only `critical` (and `total` = critical count)
- [ ] `?threshold=high` returns `critical` and `high`, `?threshold=medium` returns critical/high/medium, and `?threshold=low` returns all four
- [ ] With no `threshold` param, the response is identical to the Task 2 behaviour (backward compatible)
- [ ] An invalid threshold value (for example `?threshold=foo`) returns 400
- [ ] A non-existent SBOM with a threshold still returns 404
- [ ] Thresholded responses never serve a cached response for a different threshold

## Test Requirements
- [ ] Integration test for each threshold value asserting the included fields and `total`
- [ ] Integration test: no threshold returns the full response (regression)
- [ ] Integration test: invalid threshold returns 400
- [ ] Integration test: unknown SBOM with threshold returns 404

## Verification Commands
- `curl -s "http://localhost:8080/api/v2/sbom/<id>/advisory-summary?threshold=critical"` — JSON with only `critical` and `total`
- `curl -s -o /dev/null -w '%{http_code}' "http://localhost:8080/api/v2/sbom/<id>/advisory-summary?threshold=foo"` — `400`

## Documentation Updates
- `README.md` — if it lists endpoint parameters, mention the optional `threshold` parameter. The full API reference is covered by Task 5.

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 404 handling and 5-minute caching
