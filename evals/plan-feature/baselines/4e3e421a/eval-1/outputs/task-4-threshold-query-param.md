## Repository
trustify-backend

## Target Branch
main

## Description
Add an optional `threshold` query parameter to `GET /api/v2/sbom/{id}/advisory-summary` (TC-9001, non-MVP requirement; supports UC-2 alerting integration). When `?threshold=<severity>` is supplied, only counts at or above that severity are returned. Example from the feature: `?threshold=critical` returns only the critical count. This task is non-MVP and can be scheduled after the MVP tasks ship.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — accept an optional `threshold` query parameter, validate it, and filter the response
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — make below-threshold fields omittable in serialization (e.g., `Option<u64>` with `skip_serializing_if`) or add a filtered response variant
- `modules/fundamental/src/sbom/endpoints/mod.rs` — ensure the cache key includes the `threshold` query value
- `tests/api/sbom.rs` — add integration tests for the threshold parameter

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={critical|high|medium|low}` — MODIFY: optional query param; response includes only severities at or above the threshold, and `total` reflects only the included severities

## Implementation Notes
- Parse the param with Axum's `Query<T>` extractor, using the same pattern as existing list endpoints (`modules/fundamental/src/sbom/endpoints/list.rs`) for query parsing.
- Reuse the severity type from `modules/fundamental/src/advisory/model/summary.rs` (`AdvisorySummary.severity`) for parsing and ordering. Do not create a parallel string list.
- Invalid threshold values (e.g., `?threshold=urgent`) must return 400 via `AppError`. They must not be ignored, because silently returning unfiltered counts would mislead an alerting integration.
- Without the param, the response must be byte-for-byte identical to Task 2's response (backward compatible).
- Semantics to confirm with the feature owner before implementing: the requirement says "filter counts above a severity" while UC-2 shows `threshold=critical` returning the critical count, so the intended meaning is "at or above". Record the confirmed semantics on the Jira task.
- Constraints (docs/constraints.md): §2 Conventional Commits with Jira footer and `Assisted-by: Claude Code` trailer; §3 PR with `--base main`; §5 scope to listed files and keep parity with sibling query handling.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing query-parameter extraction pattern
- `common/src/db/query.rs` — shared filtering helpers
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity type/ordering

## Acceptance Criteria
- [ ] `?threshold=critical` returns only the `critical` count (and a `total` equal to it)
- [ ] `?threshold=high` returns `critical` and `high` counts only
- [ ] No threshold param returns the full MVP response unchanged
- [ ] An invalid threshold value returns 400, not unfiltered data
- [ ] Cached responses are keyed by threshold value (no cross-threshold cache bleed)

## Test Requirements
- [ ] Integration test for each valid threshold value asserting the included and excluded fields
- [ ] Integration test: invalid threshold returns `StatusCode::BAD_REQUEST`
- [ ] Integration test: request without threshold followed by request with `threshold=critical` on the same SBOM returns different, correct bodies (cache key correctness)

## Verification Commands
- `cargo test --test api sbom` — passes
- `curl -s 'http://localhost:8080/api/v2/sbom/<id>/advisory-summary?threshold=critical'` — returns only `critical` (and `total`)

## Documentation Updates
- REST API reference — document the `threshold` parameter (covered by Task 5 if delivered in the same release)

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
