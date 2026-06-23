## Repository
trustify-backend

## Target Branch
main

## Description
Add a severity aggregation method to `SbomService` that queries the database to count unique advisories by severity level for a given SBOM ID. This method joins the `sbom_advisory` join table with the `advisory` table, groups by severity, deduplicates by advisory ID, and returns an `AdvisorySeveritySummary`. It must return a 404-equivalent error if the SBOM does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `async fn advisory_severity_summary(&self, sbom_id: Id) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
- Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService: fetch, list, ingest`) for method signatures, error handling, and database access patterns.
- Use SeaORM query builder to join `entity::sbom_advisory` with `entity::advisory` on the advisory ID foreign key. Group by the severity column from the `advisory` entity and count distinct advisory IDs per severity level.
- Reference `entity/sbom_advisory.rs` for the SBOM-Advisory join table schema and column names.
- Reference `entity/advisory.rs` for the advisory entity schema, specifically the severity column.
- Before returning the summary, verify the SBOM exists by querying `entity::sbom`. If not found, return an `AppError` 404 error following the pattern in `common/src/error.rs` (the `AppError` enum with `.context()` wrapping).
- Use `common/src/db/query.rs` query builder helpers if applicable for constructing the aggregation query.
- Deduplicate advisories by advisory ID before counting — if the same advisory is linked to an SBOM multiple times, count it only once.
- The `total` field must equal `critical + high + medium + low`.
- Per docs/constraints.md §5.2: inspect `sbom.rs` service file and entity files before writing the query.
- Per docs/constraints.md §5.4: reuse existing query helpers from `common/src/db/query.rs` rather than duplicating filtering logic.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with database access patterns and error handling conventions
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference for advisory-related query patterns
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error enum for 404 and other error responses
- `entity/sbom_advisory.rs` — SBOM-Advisory join table entity
- `entity/advisory.rs` — advisory entity with severity column

## Acceptance Criteria
- [ ] `SbomService` has an `advisory_severity_summary` method that accepts an SBOM ID and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Method queries the database using the `sbom_advisory` join table and `advisory` table
- [ ] Method deduplicates advisories by advisory ID before counting
- [ ] Method returns correct counts for each severity level (critical, high, medium, low)
- [ ] Method returns `total` as the sum of all severity counts
- [ ] Method returns a 404 error when the SBOM ID does not exist
- [ ] Project compiles successfully with `cargo check`

## Test Requirements
- [ ] Unit test or integration test verifying correct severity counts for an SBOM with known advisory data
- [ ] Test verifying deduplication: same advisory linked twice returns count of 1
- [ ] Test verifying 404 error for a non-existent SBOM ID
- [ ] Test verifying an SBOM with zero advisories returns all-zero counts

## Dependencies
- Depends on: Task 1 — Advisory severity summary model

[sdlc-workflow] Description digest: sha256-md:e97004c3f4af83fad6a62b21acbc7c7f7504aa8eb9147e49bf869989e0af5393
