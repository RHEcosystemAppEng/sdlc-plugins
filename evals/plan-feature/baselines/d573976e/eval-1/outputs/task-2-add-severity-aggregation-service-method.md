# Task 2 — Add severity aggregation query to SbomService

## Repository
trustify-backend

## Target Branch
main

## Description
Add a method to `SbomService` that queries the database to aggregate advisory severity counts for a given SBOM ID. The method must join the `sbom_advisory` table with the `advisory` table, deduplicate by advisory ID, group by severity level, and return an `AdvisorySeveritySummary` with the counts. It must return a 404-compatible error if the SBOM ID does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `advisory_severity_summary(&self, sbom_id: Id) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
- Follow the existing service method patterns in `SbomService` (`modules/fundamental/src/sbom/service/sbom.rs`) which contains `fetch`, `list`, and `ingest` methods
- Use SeaORM query builder to construct the aggregation query joining `sbom_advisory` (entity in `entity/src/sbom_advisory.rs`) with `advisory` (entity in `entity/src/advisory.rs`)
- Deduplicate advisories by advisory ID before counting — use `DISTINCT` or equivalent SeaORM operation to avoid counting the same advisory multiple times
- Group by the severity field from the `advisory` entity (`entity/src/advisory.rs`)
- Reference `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` to understand how severity values are represented (the severity field values determine the grouping buckets: Critical, High, Medium, Low)
- Use `AppError` from `common/src/error.rs` for error handling — return a 404 error when the SBOM ID does not exist, consistent with the existing SBOM fetch endpoint behavior
- Use shared query helpers from `common/src/db/query.rs` if applicable for filtering
- Performance: the query must achieve p95 < 200ms for SBOMs with up to 500 advisories — use efficient SQL aggregation (COUNT + GROUP BY), not in-memory counting
- No new database tables — use the existing `sbom_advisory` join table

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list methods showing the query pattern, error handling, and database connection usage
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error enum with `IntoResponse` implementation for consistent HTTP error responses
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity definition
- `entity/src/advisory.rs` — Advisory entity with severity field

## Acceptance Criteria
- [ ] `SbomService` has an `advisory_severity_summary` method that returns `AdvisorySeveritySummary`
- [ ] Method deduplicates advisories by advisory ID before counting
- [ ] Method returns correct counts grouped by severity level (critical, high, medium, low)
- [ ] Method returns 404 error when SBOM ID does not exist
- [ ] Total field equals the sum of all severity counts

## Test Requirements
- [ ] Test that the service method returns correct severity counts for an SBOM with advisories at multiple severity levels
- [ ] Test that advisories linked multiple times to the same SBOM are deduplicated (counted only once)
- [ ] Test that the method returns a 404-compatible error for a non-existent SBOM ID
- [ ] Test that an SBOM with zero advisories returns all-zero counts

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model
