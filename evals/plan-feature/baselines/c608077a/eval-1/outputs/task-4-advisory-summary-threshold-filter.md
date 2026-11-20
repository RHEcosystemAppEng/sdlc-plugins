## Repository
trustify-backend

## Target Branch
main

## Description
Add the optional `?threshold=<severity>` query parameter to `GET /api/v2/sbom/{id}/advisory-summary` (TC-9001, non-MVP; UC-2 alerting integration). When a threshold is supplied, only counts at or above that severity are returned. For example, `?threshold=critical` returns only the critical count, so an integration can alert when `critical > 0`.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — parse and validate the optional `threshold` query parameter
- `modules/fundamental/src/sbom/service/sbom.rs` — apply the threshold to the aggregation result
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — make below-threshold severity fields optional and skip them in serialization (`#[serde(skip_serializing_if = "Option::is_none")]`)
- `tests/api/sbom.rs` — integration tests for threshold behavior

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={critical|high|medium|low}` — MODIFY: new optional query parameter; when present, the response includes only severities at or above the threshold (plus `total` of those included); absent → unchanged MVP response; invalid value → 400

## Implementation Notes
- Use an Axum `Query<...>` extractor with a serde enum for severity so invalid values are rejected with 400 through `AppError` (`common/src/error.rs`).
- Without `threshold`, the response must stay byte-for-byte the MVP response, so existing consumers are unaffected.
- The cache key must include the threshold value (or the filter must be applied after the cached unfiltered result), so `?threshold=critical` and the unfiltered response never collide in the Task 2 cache.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler (`.rs`) scope. Example: `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Query helpers: reuse the shared filtering helpers in `common/src/db/query.rs` if the threshold is pushed into SQL. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's database query (`.rs` service) scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/sbom.rs` matching the convention's `tests/api/*.rs` scope.
- Constraints (docs/constraints.md): §2 commits use Conventional Commits, reference the Jira task ID in the footer, and include an `Assisted-by:` trailer; §3 branch is named after the task ID and the PR is opened with `--base main` with its link posted to Jira; §5 keep changes to the listed files, inspect code before modifying, reuse existing helpers rather than duplicating logic.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering helpers
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity value set to derive the threshold enum ordering from

## Acceptance Criteria
- [ ] `?threshold=critical` returns only the critical count
- [ ] `?threshold=high` returns the critical and high counts; `medium` and `low` work the same way
- [ ] No `threshold` returns the unchanged MVP response
- [ ] An invalid `threshold` value returns 400
- [ ] Filtered and unfiltered responses are cached independently (no cross-contamination)

## Test Requirements
- [ ] Integration test for each threshold value against a seeded mixed-severity SBOM
- [ ] Integration test: invalid threshold returns 400
- [ ] Integration test: requesting the unfiltered response after a filtered one returns the full response (cache key correctness)
- [ ] Integration test: unknown SBOM with a threshold still returns 404

## Verification Commands
- `curl -s "http://localhost:8080/api/v2/sbom/<id>/advisory-summary?threshold=critical"` — returns only the critical count

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
