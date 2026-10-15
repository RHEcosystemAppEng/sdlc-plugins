## Repository
trustify-backend

## Target Branch
main

## Description
Add a new REST API endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated vulnerability advisory severity counts for a given SBOM. This is the core MVP deliverable for TC-9001, providing server-side severity aggregation to replace client-side counting.

The endpoint returns a JSON response with counts of unique advisories at each severity level (critical, high, medium, low) plus a total count. It returns 404 if the SBOM ID does not exist, consistent with existing SBOM endpoints. The response is cached for 5 minutes using the existing tower-http caching middleware.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — AdvisorySeveritySummary response struct with fields: critical, high, medium, low, total (all u64)
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Endpoint handler for GET /api/v2/sbom/{id}/advisory-summary with 5-minute cache and 404 handling

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add pub mod advisory_summary and re-export AdvisorySeveritySummary
- `modules/fundamental/src/sbom/service/sbom.rs` — Add advisory_severity_summary method to SbomService that queries sbom_advisory joined with advisory, groups by severity, deduplicates by advisory ID
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the /api/v2/sbom/{id}/advisory-summary route
- `tests/api/sbom.rs` — Add integration tests for the advisory-summary endpoint

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ critical: N, high: N, medium: N, low: N, total: N }` with 5-minute cache, 404 if SBOM not found

## Implementation Notes
Follow the established module pattern (model/ + service/ + endpoints/) used by existing SBOM endpoints. Reference the existing endpoint structure in `modules/fundamental/src/sbom/endpoints/get.rs` for the handler pattern and 404 error handling via `AppError`.

Per CONVENTIONS.md: all handlers must return `Result<T, AppError>` with `.context()` wrapping for error propagation.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md: endpoint registration follows the pattern in each module's `endpoints/mod.rs`; new routes are registered there.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint registration scope.

Per CONVENTIONS.md: caching uses `tower-http` caching middleware configured in endpoint route builders.
Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md: integration tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` pattern against a real PostgreSQL test database.
Applies: task modifies `tests/api/sbom.rs` matching the convention's `.rs` test file scope.

**Service method implementation guidance:**
- Query `sbom_advisory` join table filtered by the given SBOM ID
- Join with `advisory` table to get severity field from `AdvisorySummary`
- Deduplicate by advisory ID before counting (use `SELECT DISTINCT advisory_id, severity`)
- Group by severity and count
- Return `AdvisorySeveritySummary` with counts per severity level
- Use `common/src/db/query.rs` helpers for query building where applicable

**Caching guidance:**
- Apply 5-minute cache TTL using tower-http `CacheControl` or equivalent middleware on the route builder
- See existing endpoint route builders for the caching pattern

**404 handling:**
- Check SBOM existence before querying advisories
- Return `AppError::NotFound` (or equivalent from `common/src/error.rs`) if SBOM ID does not exist

## Reuse Candidates
- `common/src/error.rs::AppError` — Error enum that implements IntoResponse; use for 404 and other error responses
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination; reuse for building the aggregation query
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service with fetch/list/ingest methods; add the new aggregation method here
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the severity field definition; reference for severity enum values
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; use for the aggregation query
- `modules/fundamental/src/sbom/endpoints/get.rs` — Existing SBOM get endpoint; follow the same handler pattern for error handling and response structure

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns `{ critical: N, high: N, medium: N, low: N, total: N }` with correct counts
- [ ] Advisory counts are deduplicated by advisory ID (duplicate advisory-SBOM links do not inflate counts)
- [ ] Endpoint returns 404 with appropriate error body when SBOM ID does not exist
- [ ] Response is cached for 5 minutes (subsequent requests within 5 minutes return cached response)
- [ ] Response time p95 < 200ms for SBOMs with up to 500 advisories
- [ ] No new database tables are created — uses existing `sbom_advisory` and `advisory` tables

## Test Requirements
- [ ] Integration test: valid SBOM ID returns 200 with correct severity counts
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: advisories with duplicate SBOM links are counted only once
- [ ] Integration test: SBOM with zero advisories returns all counts as 0
- [ ] Integration test: verify response cache headers indicate 5-minute TTL

## Verification Commands
- `cargo test --test api sbom::advisory_summary` — Run advisory-summary integration tests, expect all pass
- `cargo build` — Verify the project compiles without errors

## Dependencies
- None (this is the foundational task)
