# Task 2 — Add advisory severity aggregation query to SbomService

## Repository
trustify-backend

## Target Branch
main

## Description
Implement a service method on `SbomService` that queries the existing `sbom_advisory` join table joined with the `advisory` table to produce deduplicated severity counts for a given SBOM ID. The method must return an `AdvisorySeveritySummary` struct with counts grouped by severity level (Critical, High, Medium, Low). It must also support an optional severity threshold parameter that filters counts to only include severities at or above the specified level.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_summary(&self, sbom_id: Id, threshold: Option<Severity>) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
- Follow the query patterns established in `modules/fundamental/src/sbom/service/sbom.rs` for the existing `fetch` and `list` methods. These methods use SeaORM query builders and return `Result<T, AppError>` with `.context()` error wrapping.
- Use the `sbom_advisory` entity (`entity/src/sbom_advisory.rs`) as the primary join table. Join to the `advisory` entity (`entity/src/advisory.rs`) to access the severity field.
- **Deduplication**: Use `DISTINCT` on the advisory ID column before grouping by severity to ensure each advisory is counted only once, even if multiple join records exist.
- **Severity grouping**: Use a SQL `GROUP BY` on the severity column with `COUNT(*)` to produce per-severity counts. Map the database severity values to the `AdvisorySeveritySummary` fields.
- **Threshold filtering**: When the `threshold` parameter is provided, add a `WHERE` clause that filters advisories to only those at or above the specified severity level. Severity ordering: Critical > High > Medium > Low.
- **SBOM existence check**: Before querying advisories, verify the SBOM ID exists using the existing `fetch` method. Return `AppError::NotFound` (404) if the SBOM does not exist, consistent with `GET /api/v2/sbom/{id}` behavior.
- **Performance**: The query should execute against existing indexes on the `sbom_advisory` join table. No new database tables or indexes are required per the NFRs. Target p95 < 200ms for SBOMs with up to 500 advisories.
- Use shared query helpers from `common/src/db/query.rs` if applicable for building the aggregation query.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct where the new method will be added; follow its error handling and query patterns
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference for querying advisory entities and accessing severity fields
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error enum with `NotFound` variant for 404 responses
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity definition
- `entity/src/advisory.rs` — Advisory entity with severity field

## Acceptance Criteria
- [ ] `SbomService::get_advisory_summary` method exists and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Advisories are deduplicated by advisory ID before counting
- [ ] Counts are correctly grouped by severity level (Critical, High, Medium, Low)
- [ ] `total` field equals the sum of all severity counts
- [ ] Returns `AppError::NotFound` (404) when SBOM ID does not exist
- [ ] Optional `threshold` parameter correctly filters to severities at or above the threshold
- [ ] Method works correctly for SBOMs with zero advisories (returns all zeros)

## Test Requirements
- [ ] Test that aggregation correctly counts advisories by severity with deduplication
- [ ] Test that non-existent SBOM ID returns NotFound error
- [ ] Test threshold filtering: `threshold=critical` returns only critical count, others zero
- [ ] Test threshold filtering: `threshold=high` returns critical and high counts, medium and low zero
- [ ] Test SBOM with no advisories returns all-zero summary
- [ ] Test that duplicate advisory links (same advisory linked multiple times) are counted only once

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model
