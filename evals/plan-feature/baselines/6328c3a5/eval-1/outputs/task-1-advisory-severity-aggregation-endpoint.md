## Repository
trustify-backend

## Target Branch
main

## Description
Add a new advisory severity aggregation model, service method, and endpoint to provide server-side severity counts for advisories linked to a given SBOM. This eliminates the need for frontend clients to fetch and count individual advisories client-side, reducing dashboard load times from ~2s to <200ms.

The implementation follows the established module pattern (model/ + service/ + endpoints/) within the SBOM module and adds a new `GET /api/v2/sbom/{id}/advisory-summary` endpoint that returns deduplicated severity counts with 5-minute response caching.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` response struct with fields: `critical`, `high`, `medium`, `low`, `total`
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` with 5-minute cache configuration

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — export the new `advisory_summary` module
- `modules/fundamental/src/sbom/service/sbom.rs` — add `aggregate_advisory_severity` method that queries the `sbom_advisory` join table, deduplicates by advisory ID, and groups counts by severity level
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new `/api/v2/sbom/{id}/advisory-summary` route

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` with deduplicated advisory counts by severity level. Returns 404 if the SBOM ID does not exist. Response is cached for 5 minutes.

## Implementation Notes
- Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ structure within the SBOM module. See `modules/fundamental/src/sbom/endpoints/get.rs` for the established endpoint pattern.
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's model/ directory scope.
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` from the handler and use `.context()` for error wrapping. See `modules/fundamental/src/sbom/endpoints/get.rs` for the error handling pattern.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` handler scope.
- Per CONVENTIONS.md §Endpoint Registration: register the new route in `modules/fundamental/src/sbom/endpoints/mod.rs`. See existing routes in that file for the registration pattern. The `server/main.rs` mounts all modules.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `endpoints/mod.rs` scope.
- Per CONVENTIONS.md §Caching: configure 5-minute cache using `tower-http` caching middleware in the endpoint route builder. See existing endpoint route builders for the caching configuration pattern.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's endpoint route builder scope.
- Per CONVENTIONS.md §Framework: use Axum for HTTP routing and SeaORM for database queries against the `sbom_advisory` join table.
  Applies: convention has no file-type restriction (broadly applicable).
- The aggregation query should join `sbom_advisory` with `advisory` to get severity levels, use `GROUP BY severity` with `COUNT(DISTINCT advisory_id)` to deduplicate, and verify the SBOM exists before aggregating (return 404 via `AppError` if not found).
- Derive `serde::Serialize` on `AdvisorySeveritySummary` for JSON response serialization.

## Reuse Candidates
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for building the aggregation query
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct includes the severity field definition to reference for severity level values
- `common/src/error.rs` — `AppError` enum for 404 and error responses
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM GET endpoint demonstrating the handler pattern, error handling, and response serialization

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns `{ critical: N, high: N, medium: N, low: N, total: N }` with correct severity counts
- [ ] Advisory counts are deduplicated by advisory ID (each advisory counted once regardless of how many times it links to the SBOM)
- [ ] Endpoint returns 404 with appropriate error response when the SBOM ID does not exist
- [ ] Response is cached for 5 minutes using tower-http caching middleware
- [ ] Response time is p95 < 200ms for SBOMs with up to 500 advisories
- [ ] New route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] No new database tables are created — only existing `sbom_advisory` and `advisory` tables are queried

## Test Requirements
- [ ] Unit test for `aggregate_advisory_severity` service method with known advisory-SBOM relationships
- [ ] Test that duplicate advisory-SBOM links produce deduplicated counts
- [ ] Test that a nonexistent SBOM ID returns 404
- [ ] Test that severity counts are correctly categorized (critical, high, medium, low)
- [ ] Test that `total` equals the sum of all severity counts

## Verification Commands
- `cargo test --package tests -- advisory_summary` — run integration tests for the new endpoint
- `cargo build --workspace` — verify the project compiles with the new module

## Documentation Updates
- REST API reference — add the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint with path parameters, response shape, and error codes

## Dependencies
- None (first task in the chain)
