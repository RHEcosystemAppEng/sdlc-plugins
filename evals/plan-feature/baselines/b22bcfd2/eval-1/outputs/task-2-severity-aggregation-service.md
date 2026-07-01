## Repository
trustify-backend

## Target Branch
main

## Description
Add a `get_advisory_severity_summary` method to `SbomService` that queries the database for all advisories linked to a given SBOM, deduplicates by advisory ID, groups by severity level, and returns an `AdvisorySeveritySummary` with the counts. This method provides the core business logic for the advisory-summary endpoint, keeping computation server-side to avoid client-side multi-page fetching.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_severity_summary` method to `SbomService`

## Implementation Notes
Add the method to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`, following the pattern of existing service methods (fetch, list, ingest) that accept a database connection and return `Result<T, AppError>`.

The query should:
1. Verify the SBOM exists by querying the `entity::sbom` entity — return `AppError::NotFound` (from `common/src/error.rs`) if the SBOM ID does not exist, consistent with existing SBOM endpoints
2. Join `entity::sbom_advisory` (from `entity/src/sbom_advisory.rs`) with `entity::advisory` (from `entity/src/advisory.rs`) on the advisory ID
3. Filter by the given SBOM ID
4. Select distinct advisory IDs to deduplicate (requirement: count only unique advisories)
5. Group by severity and count
6. Map the severity string values to the corresponding fields in `AdvisorySeveritySummary`

Use SeaORM query builder patterns consistent with existing queries in `common/src/db/query.rs`. The severity field comes from `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs`.

Error handling: wrap database errors with `.context()` per the project convention in `common/src/error.rs` (AppError enum, implements IntoResponse).

## Reuse Candidates
- `common/src/db/query.rs::query` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error enum for consistent error responses
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for the aggregation query
- `entity/src/advisory.rs` — Advisory entity containing the severity field

## Acceptance Criteria
- [ ] `SbomService::get_advisory_severity_summary(sbom_id)` returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Returns 404 error when SBOM ID does not exist
- [ ] Counts are deduplicated by advisory ID (same advisory linked multiple times counts once)
- [ ] All four severity levels (critical, high, medium, low) are counted correctly
- [ ] Total field equals the sum of all severity counts

## Test Requirements
- [ ] Unit test with mock database verifying correct severity grouping and counting
- [ ] Unit test verifying 404 is returned for non-existent SBOM ID
- [ ] Unit test verifying deduplication: same advisory linked twice to same SBOM counts as 1

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model

## additional_fields
- priority: Major
- fixVersions: RHTPA 1.5.0