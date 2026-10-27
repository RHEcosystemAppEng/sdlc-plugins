## Repository
trustify-backend

## Target Branch
main

## Description
Add an `advisory_severity_summary` method to `SbomService` that aggregates advisory severity counts for a given SBOM ID. The method queries the `sbom_advisory` join table, joins with the `advisory` entity to access the severity field, deduplicates by advisory ID, groups by severity level, and returns an `AdvisorySeveritySummary`. Returns a 404-compatible error if the SBOM ID does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `advisory_severity_summary` method to `SbomService` that accepts an SBOM ID, queries the database, and returns `Result<AdvisorySeveritySummary, AppError>`

## Implementation Notes
Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService` methods for fetch, list, ingest). The method should:

1. First verify the SBOM exists by querying the `sbom` entity (`entity/src/sbom.rs`). If not found, return an `AppError` 404 error following the pattern in `common/src/error.rs`.
2. Query the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) joined with the `advisory` entity (`entity/src/advisory.rs`) to access the `severity` field from `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`).
3. Use SeaORM's `select`, `join`, `group_by`, and `count` to aggregate severity counts.
4. Deduplicate by advisory ID before counting (use `DISTINCT` in the query or group by advisory ID).
5. Use shared query helpers from `common/src/db/query.rs` where applicable.

Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for all error paths.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service file scope.

Per CONVENTIONS.md §Module Pattern: follow the `model/ + service/ + endpoints/` structure for the sbom domain module.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust module file scope.

## Reuse Candidates
- `common/src/db/query.rs::Query` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — standard error enum with IntoResponse implementation
- `entity/src/sbom_advisory.rs` — existing SBOM-Advisory join table entity

## Acceptance Criteria
- [ ] `SbomService` has an `advisory_severity_summary` method that returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Method counts unique advisories per severity level (critical, high, medium, low)
- [ ] Method returns 404 error when SBOM ID does not exist
- [ ] Method deduplicates advisories by advisory ID before counting
- [ ] `total` field equals the sum of all severity counts
- [ ] Code compiles without errors

## Test Requirements
- [ ] Unit test verifying correct aggregation with multiple advisories at different severities
- [ ] Unit test verifying 404 response for nonexistent SBOM ID
- [ ] Unit test verifying deduplication of advisories (same advisory linked multiple times)

## Dependencies
- Depends on: Task 1 — Advisory severity summary model
