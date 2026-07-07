## Repository
trustify-backend

## Target Branch
main

## Description
Add an aggregation method to `AdvisoryService` that queries the `sbom_advisory` join table, deduplicates advisories by advisory ID, groups them by severity level, and returns an `AdvisorySeveritySummary`. This service method is the core business logic for the advisory summary endpoint and must handle the case where the SBOM does not exist by returning an appropriate error.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — add `get_severity_summary_for_sbom(sbom_id)` method to `AdvisoryService`

## Implementation Notes
The new method should query `entity::sbom_advisory` joined with `entity::advisory` to fetch advisories linked to the given SBOM. Deduplicate by advisory ID before counting. Use the `severity` field from `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` as the reference for severity level extraction. Return `Result<AdvisorySeveritySummary, AppError>` using the error pattern from `common/src/error.rs`. Check SBOM existence first using the pattern in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`), returning 404 via `AppError` if the SBOM does not exist. Use query builder helpers from `common/src/db/query.rs` for constructing the database query.
Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` for error propagation. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust service scope.
Per CONVENTIONS.md §Module pattern: place the service logic in service/ following the model/ + service/ + endpoints/ module structure. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust module scope.

## Acceptance Criteria
- [ ] `AdvisoryService` has a new method `get_severity_summary_for_sbom` that accepts an SBOM ID
- [ ] Method returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Advisories are deduplicated by advisory ID before counting
- [ ] Severity counts are correctly grouped into critical, high, medium, low categories
- [ ] Total count equals the sum of all severity categories
- [ ] Returns 404 error when SBOM ID does not exist
- [ ] No new database tables are created

## Test Requirements
- [ ] Unit test verifying correct severity aggregation with known test data
- [ ] Unit test verifying deduplication of advisories with the same advisory ID
- [ ] Unit test verifying 404 error for non-existent SBOM ID

## Dependencies
- Depends on: Task 1 — Advisory severity summary model
