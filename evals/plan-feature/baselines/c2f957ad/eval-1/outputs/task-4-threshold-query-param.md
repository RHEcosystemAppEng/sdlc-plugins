## Repository
trustify-backend

## Target Branch
main

## Description
Add an optional `?threshold=<severity>` query parameter to `GET /api/v2/sbom/{id}/advisory-summary` for alerting integrations (TC-9001, UC-2, non-MVP). When present, only severities at or above the threshold are counted. For example, `?threshold=critical` returns only the critical count, so a poller can alert when `critical > 0`.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — parse and validate the optional `threshold` query parameter and pass it to the service
- `modules/fundamental/src/sbom/service/sbom.rs` — accept an optional minimum severity in `advisory_severity_summary` and restrict counting to severities at or above it
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — make the below-threshold fields optional (`Option<u64>`, skipped when `None`) so filtered responses omit them
- `modules/fundamental/src/sbom/endpoints/mod.rs` — include `threshold` in the cache key for the route
- `tests/api/sbom.rs` — integration tests for threshold filtering

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={critical|high|medium|low}` — MODIFY: new optional query parameter. When set, severities below the threshold are omitted from the response and `total` is the sum of the included severities. Without the parameter, the response is unchanged. An invalid value returns 400.

## Implementation Notes
- Interpretation recorded in the plan: "filter counts above a severity" means at-or-above (inclusive), so `threshold=critical` returns `{ critical: N, total: N }`, matching UC-2 ("only critical count is returned"). `threshold=low` is equivalent to no threshold.
- Parse with Axum's `Query<T>` extractor using a `serde`-deserializable severity enum (case-insensitive). Unknown values must return 400 via `AppError`, not be ignored. Silently ignoring a typo would return unfiltered counts to an alerting system.
- Keep the unfiltered response shape byte-for-byte identical to Task 2's output (all five fields present) so existing consumers are unaffected.
- The cache key must include the normalized threshold value so that filtered and unfiltered responses never collide. Task 3's invalidation must clear all threshold variants for the SBOM. Verify the invalidation function from Task 2 handles this (e.g., prefix-keyed invalidation).
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>`, mapping invalid `threshold` values to a 400 error variant. Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler (`.rs`) scope.
- Per CONVENTIONS.md §Query helpers: use `common/src/db/query.rs` filtering helpers for the severity predicate where applicable. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's database query (`.rs`) scope.
- Per CONVENTIONS.md §Caching: cache configuration stays in the endpoint route builder. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint route builder scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` use a real PostgreSQL test database and `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/sbom.rs` matching the convention's `tests/api/` scope.
- Constraints (docs/constraints.md): §2 commits use Conventional Commits, reference the Jira task in the footer, and include an `Assisted-by:` trailer; §3 PR branch named after the Jira task ID, `gh pr create --base main`, PR link posted on the Jira task; §5 keep changes scoped to the listed files, inspect code before modifying it, and reuse existing helpers.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering helpers used by existing list endpoints' query parameters
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing query-parameter extraction pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity representation to reuse for the threshold enum and ordering

## Acceptance Criteria
- [ ] `?threshold=critical` returns only `critical` and `total` (equal to critical)
- [ ] `?threshold=high` returns `critical`, `high`, and `total` = critical + high
- [ ] Omitting `threshold` returns the unchanged Task 2 response
- [ ] Invalid `threshold` value returns 400 (fail-closed, not unfiltered counts)
- [ ] Unknown SBOM ID still returns 404 when `threshold` is supplied
- [ ] Filtered and unfiltered responses are cached under distinct keys and both are invalidated on ingestion

## Test Requirements
- [ ] Integration test (parameterized if sibling tests use parameterization): each threshold value returns the expected subset of fields and total
- [ ] Integration test: `?threshold=bogus` returns 400
- [ ] Integration test: no threshold returns all five fields
- [ ] Integration test: cached `?threshold=critical` response is refreshed after advisory ingestion

## Verification Commands
- `curl -s 'http://localhost:8080/api/v2/sbom/<id>/advisory-summary?threshold=critical'` — returns `{"critical":N,"total":N}`
- `curl -s -o /dev/null -w '%{http_code}' 'http://localhost:8080/api/v2/sbom/<id>/advisory-summary?threshold=bogus'` — prints `400`

## Documentation Updates
- `README.md` — if endpoints are listed there, note the optional `threshold` parameter

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
