# Task 1 -- Add AdvisorySeveritySummary model and service method

## Repository
trustify-backend

## Target Branch
main

## Description
Add a new `AdvisorySeveritySummary` model struct and a corresponding service method on
`SbomService` that aggregates advisory severity counts for a given SBOM. The service
method queries the `sbom_advisory` join table, joins the `advisory` table to access
the severity field, deduplicates by advisory ID, groups by severity level, and returns
counts for critical, high, medium, low, and total. This provides the data layer for
the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- re-export the new summary model
- `modules/fundamental/src/sbom/service/sbom.rs` -- add `advisory_severity_summary` method to `SbomService`

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_severity_summary.rs` -- new `AdvisorySeveritySummary` struct

## Implementation Notes
- Follow the existing model pattern established by `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` and `SbomDetails` in `modules/fundamental/src/sbom/model/details.rs`. The new struct should derive the same traits (e.g., `Serialize`, `Deserialize`, `Debug`, `Clone`).
- The `AdvisorySeveritySummary` struct should have fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`.
- The service method should follow the pattern of existing methods in `SbomService` (`modules/fundamental/src/sbom/service/sbom.rs`): accept a database connection, return `Result<T, AppError>`, and use `.context()` for error wrapping per the codebase error handling convention.
- Use the `sbom_advisory` entity (`entity/src/sbom_advisory.rs`) to join SBOMs to advisories, and the `advisory` entity (`entity/src/advisory.rs`) to access the severity field.
- Deduplicate by advisory ID before counting -- use `SELECT DISTINCT advisory_id` or equivalent SeaORM query to ensure the same advisory linked multiple times is only counted once.
- Use SeaORM query builder helpers from `common/src/db/query.rs` where applicable.
- The method should return a 404-appropriate error (via `AppError`) if the SBOM ID does not exist -- verify SBOM existence before running the aggregation query, consistent with the pattern used by the existing `GET /api/v2/sbom/{id}` endpoint in `modules/fundamental/src/sbom/endpoints/get.rs`.

## Reuse Candidates
- `common/src/error.rs::AppError` -- error enum with `IntoResponse` implementation; use for not-found and internal errors
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination; reuse for building the aggregation query
- `entity/src/sbom_advisory.rs` -- existing SBOM-Advisory join table entity; use as the primary query source
- `entity/src/advisory.rs` -- advisory entity with severity field; join to access severity values

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical`, `high`, `medium`, `low`, `total`
- [ ] `SbomService` has an `advisory_severity_summary` method that returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] The method deduplicates advisories by ID before counting
- [ ] The method returns an appropriate error when the SBOM ID does not exist

## Test Requirements
- [ ] Unit test verifying the `AdvisorySeveritySummary` struct serializes correctly to JSON with the expected field names
- [ ] Service-level test verifying correct aggregation counts with a known dataset (multiple advisories at different severity levels)
- [ ] Service-level test verifying deduplication (same advisory linked twice to the same SBOM produces count of 1, not 2)
- [ ] Service-level test verifying error is returned for a non-existent SBOM ID
