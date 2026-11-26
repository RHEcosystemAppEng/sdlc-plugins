## Repository
trustify-backend

## Target Branch
main

## Description
Add an optional `?threshold=<severity>` query parameter to `GET /api/v2/sbom/{id}/advisory-summary` so alerting integrations can request only counts at or above a given severity (TC-9001, non-MVP requirement; UC-2). Example: `?threshold=critical` returns only the critical count. Accepted values: `critical`, `high`, `medium`, `low`. Without the parameter, behavior is unchanged.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — accept and validate an optional `threshold` query parameter
- `modules/fundamental/src/sbom/service/sbom.rs` — apply the threshold to the aggregation result (or the query)
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — make below-threshold fields optional / skipped on serialization
- `tests/api/sbom.rs` — integration tests for threshold behavior

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={critical|high|medium|low}` — MODIFY: optional query parameter; response includes only severities at or above the threshold and `total` is the sum of included severities; invalid values return 400

## Implementation Notes
- Response shape when filtered (clarification recorded in the impact map): UC-2 states "only critical count is returned" for `threshold=critical`. Implement by omitting below-threshold keys (`#[serde(skip_serializing_if = "Option::is_none")]`) and computing `total` as the sum of the returned severities. Unfiltered responses keep all five fields, so existing consumers are unaffected.
- Parse the parameter with Axum's `Query<T>` extractor into a severity enum; reuse the severity representation from `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary.severity`) and the ordering Critical > High > Medium > Low. Reject unknown values with a 400 `AppError` from `common/src/error.rs` rather than ignoring them (ignoring would make an alerting integration with a typo silently see unfiltered data).
- The 5-minute cache key configured in Task 2 must include the query string so filtered and unfiltered responses do not collide; Task 3's invalidation must clear all variants for the SBOM.
- Follow the query-parameter parsing pattern used by `modules/fundamental/src/sbom/endpoints/list.rs` and shared filtering in `common/src/db/query.rs`.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` and map invalid thresholds to a bad-request variant with `.context()`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler (`.rs`) scope.
- Per CONVENTIONS.md §Query helpers: reuse filtering helpers from `common/src/db/query.rs` if filtering is pushed into SQL. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's database query (`.rs`) scope.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/sbom.rs` using `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/sbom.rs` matching the convention's `tests/api/` integration test scope.
- Constraints (docs/constraints.md): Conventional Commits with Jira ID footer and `Assisted-by:` trailer (§2.1–2.3); PR with `--base main`, link posted on Jira (§3.2, §3.3); scope to listed files and keep backward compatibility (§5.1–5.8).

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity field/representation to reuse for the threshold enum
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing query-parameter extraction pattern
- `common/src/db/query.rs` — shared filtering helpers

## Acceptance Criteria
- [ ] `?threshold=critical` returns only the `critical` count and a `total` equal to it
- [ ] `?threshold=high` returns `critical` and `high` counts with `total` = critical + high (and likewise for `medium` and `low`)
- [ ] Omitting `threshold` returns the full `{ critical, high, medium, low, total }` response unchanged
- [ ] An invalid threshold value returns 400 (not unfiltered data)
- [ ] Unknown SBOM ID with a valid threshold still returns 404
- [ ] Filtered and unfiltered responses are cached under distinct keys

## Test Requirements
- [ ] Parameterized integration test covering each threshold value against an SBOM with advisories in every severity
- [ ] Integration test: no threshold returns all fields (backward compatibility)
- [ ] Integration test: `?threshold=bogus` returns 400
- [ ] Integration test: unfiltered then filtered request within the TTL returns different, correct bodies (no cache collision)

## Verification Commands
- `cargo test --test api sbom` — threshold tests pass
- `curl -s 'http://localhost:8080/api/v2/sbom/<id>/advisory-summary?threshold=critical'` — returns `{"critical":N,"total":N}`

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
