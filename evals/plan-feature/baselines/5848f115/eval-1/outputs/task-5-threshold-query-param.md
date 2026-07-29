## Repository
trustify-backend

## Target Branch
main

## Description
Add support for the optional `?threshold=critical` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the endpoint filters severity counts to include only levels at or above the specified threshold (e.g., `?threshold=high` returns counts for critical and high only, with medium and low as zero). This is a non-MVP enhancement that enables alerting integrations to quickly check if any advisories above a given severity level affect an SBOM.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add query parameter extraction and threshold filtering logic
- `modules/fundamental/src/sbom/service/sbom.rs` — add optional threshold parameter to the aggregation method (or add a filtering step post-aggregation)

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary?threshold={severity}` — MODIFY: add optional `threshold` query parameter; accepted values: `critical`, `high`, `medium`, `low`; when set, counts for severity levels below the threshold are returned as zero

## Implementation Notes
- The threshold severity hierarchy is: Critical > High > Medium > Low. When `?threshold=high`, return counts for Critical and High only; Medium and Low should be 0 in the response.
- The `total` field should reflect only the filtered counts (sum of non-zeroed severity levels).
- Implement the filtering either:
  - At the service layer: modify the aggregation query to include a `WHERE severity >= threshold` condition, or
  - At the endpoint layer: call the existing aggregation method and zero out counts below the threshold before returning. This approach avoids changing the service method signature and keeps the filtering as a presentation concern.
- The endpoint handler should extract the `threshold` parameter from the query string using Axum's query parameter extraction (`axum::extract::Query`).
- Invalid threshold values (not one of critical/high/medium/low) should return a 400 Bad Request with a descriptive error message.
- Per Key Conventions: error handling — all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — the existing endpoint handler from Task 2; extend with query parameter extraction
- `common/src/db/query.rs` — shared query builder helpers; may be useful if implementing threshold at the query level

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only critical count (high, medium, low are 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns critical and high counts (medium, low are 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns critical, high, and medium counts (low is 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (equivalent to no threshold)
- [ ] `total` reflects the sum of non-zeroed counts
- [ ] Omitting the `?threshold` parameter returns all counts (backward compatible with Task 2)
- [ ] Invalid threshold value returns 400 Bad Request

## Test Requirements
- [ ] Integration test: `?threshold=critical` with SBOM having advisories at all levels returns only critical count
- [ ] Integration test: `?threshold=high` returns critical + high counts, medium and low are 0
- [ ] Integration test: no threshold parameter returns all counts (backward compatibility)
- [ ] Integration test: invalid threshold value returns 400 status
- [ ] Unit test: threshold filtering logic correctly zeroes out counts below the threshold

## Verification Commands
- `cargo build -p fundamental` — compiles without errors
- `cargo test --test api -- sbom_advisory_summary` — all integration tests pass including threshold tests

## Dependencies
- Depends on: Task 2 — Add advisory-summary endpoint with caching
