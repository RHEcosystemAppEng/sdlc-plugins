# Task 1 — Add advisory severity summary model, service method, and REST endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add a new `GET /api/v2/sbom/{id}/advisory-summary` endpoint that returns aggregated severity counts (critical, high, medium, low, total) for advisories linked to a given SBOM. This eliminates client-side advisory counting and supports dashboard severity widgets with sub-200ms response times. The endpoint uses the existing `sbom_advisory` join table to aggregate counts, deduplicating by advisory ID, and leverages `tower-http` caching middleware for a 5-minute cache TTL. It returns 404 when the SBOM ID does not exist, consistent with existing SBOM endpoints. An optional `?threshold` query parameter filters counts to only include severities at or above the specified level (non-MVP but included for alerting integration use cases).

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — New struct `AdvisorySeveritySummary` with fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`. Derives `Serialize`, `Deserialize`, `Debug`, `Clone`.
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — New endpoint handler for `GET /api/v2/sbom/{id}/advisory-summary` with optional `threshold` query parameter.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` to expose the new model.
- `modules/fundamental/src/sbom/service/sbom.rs` — Add a `get_advisory_severity_summary` method to `SbomService` that queries the `sbom_advisory` join table, joins to the `advisory` table for severity, groups by severity level, deduplicates by advisory ID, and returns an `AdvisorySeveritySummary`. Add threshold filtering logic when the threshold parameter is provided.
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the new `advisory_summary` route under `/api/v2/sbom/{id}/advisory-summary` with 5-minute cache configuration via `tower-http` caching middleware.

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: Returns `{ critical: N, high: N, medium: N, low: N, total: N }`. Accepts optional `?threshold=critical|high|medium|low` query parameter to filter counts to only include severities at or above the specified level. Returns 404 if the SBOM ID does not exist.

## Implementation Notes
- Follow the existing endpoint pattern established in `modules/fundamental/src/sbom/endpoints/get.rs` for SBOM ID path parameter extraction, error handling, and 404 responses. The existing handler uses `Result<T, AppError>` with `.context()` wrapping — replicate this pattern.
- The severity field is defined on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` — use the same severity representation (likely a string enum or enum type) for consistency.
- The `sbom_advisory` join table entity is defined in `entity/src/sbom_advisory.rs` — use this for the aggregation query joining SBOM to advisory records.
- The advisory entity with severity is in `entity/src/advisory.rs` — join through `sbom_advisory` to `advisory` to access the severity field.
- Use SeaORM's query builder (likely `Select` with `.group_by()` and `.count()`) to perform the aggregation at the database level rather than fetching all records and counting in Rust. Reference the query helpers in `common/src/db/query.rs` for any shared filtering patterns.
- For the 404 check, first verify the SBOM exists (query the `sbom` entity) before running the aggregation. Follow the pattern in the existing `get.rs` endpoint.
- Apply 5-minute caching using `tower-http` cache middleware on the route builder, consistent with existing cache configuration patterns in the endpoint route builders.
- For the `threshold` query parameter, define a `Threshold` enum (Critical, High, Medium, Low) that maps to severity levels. When present, filter the aggregation query to only count advisories at or above the threshold severity. Use `serde` deserialization for the query parameter.
- Ensure deduplication by advisory ID in the aggregation query — use `DISTINCT` or `GROUP BY advisory.id` before grouping by severity to avoid double-counting advisories linked to the same SBOM through multiple paths.
- All handlers return `Result<T, AppError>` per `common/src/error.rs`.

## Reuse Candidates
- `common/src/error.rs::AppError` — error type for endpoint handlers, implements `IntoResponse`
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination patterns
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET endpoint pattern for SBOM by ID, demonstrates path parameter extraction, 404 handling, and response structure
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition, reference for severity type/enum
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity needed for the aggregation query

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` returns a JSON response with `critical`, `high`, `medium`, `low`, and `total` fields as integer counts
- [ ] Advisory counts are deduplicated by advisory ID (no double-counting)
- [ ] Endpoint returns HTTP 404 when the SBOM ID does not exist
- [ ] Response is cached for 5 minutes using `tower-http` caching middleware
- [ ] Optional `?threshold=critical` query parameter filters counts to only include severities at or above the specified level
- [ ] Response time meets p95 < 200ms target for SBOMs with up to 500 advisories (aggregation performed at database level)

## Test Requirements
- [ ] Unit test for `AdvisorySeveritySummary` serialization to verify JSON field names and types
- [ ] Unit test for threshold filtering logic to verify correct severity cutoff behavior
- [ ] Verify `get_advisory_severity_summary` service method returns correct counts for a known dataset (covered in Task 3 integration tests)

## Dependencies
None
