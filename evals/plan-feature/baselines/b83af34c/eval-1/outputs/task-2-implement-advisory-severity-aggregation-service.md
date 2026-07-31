## Repository
trustify-backend

## Target Branch
main

## Priority
Major

## Fix Versions
RHTPA 1.5.0

## Description
Add a service method to `SbomService` that queries the database to aggregate advisory severity counts for a given SBOM. The method joins the `sbom_advisory` table with the `advisory` table, deduplicates by advisory ID, groups by severity level, and returns an `AdvisorySeveritySummary`. It must return a 404 error if the SBOM does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_summary` method to `SbomService`

## Implementation Notes
Add a method `pub async fn get_advisory_summary(&self, sbom_id: Id) -> Result<AdvisorySeveritySummary, AppError>` to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`. First verify the SBOM exists by calling the existing `get` method (or equivalent query); return `AppError::NotFound` if absent. Then query the `sbom_advisory` entity from `entity/src/sbom_advisory.rs` joined with `advisory` from `entity/src/advisory.rs`. Use `SELECT DISTINCT advisory_id` to deduplicate, then `GROUP BY severity` to count per level. Map the resulting rows into an `AdvisorySeveritySummary` struct, computing `total` as the sum of all levels.

Follow the existing service patterns in `modules/fundamental/src/sbom/service/sbom.rs` for database access and error handling. Use `common/src/db/query.rs` helpers if applicable for building the aggregation query.

Per CONVENTIONS.md §Framework: use SeaORM for the aggregation query against PostgreSQL. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust syntax scope.

Per CONVENTIONS.md §Module pattern: add the service method within the existing `service/` subdirectory of the `sbom` module. Applies: convention has no file-type restriction (broadly applicable).

Per CONVENTIONS.md §Error handling: return `Result<AdvisorySeveritySummary, AppError>` and use `.context()` wrapping on database errors. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust syntax scope.

Per CONVENTIONS.md §Query helpers: consider reusing shared filtering and pagination helpers from `common/src/db/query.rs` for building the aggregation query. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Caching: the service method itself does not handle caching (that is the endpoint layer's responsibility), but ensure the return type is cache-friendly. Applies: convention has no file-type restriction (broadly applicable).

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::get` — existing SBOM existence check method
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for the aggregation query
- `entity/src/advisory.rs` — Advisory entity with severity field
- `common/src/db/query.rs` — shared query builder helpers for filtering
- `common/src/error.rs::AppError` — error type for 404 handling

## Acceptance Criteria
- [ ] `SbomService::get_advisory_summary` method exists and compiles
- [ ] Method returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Returns correct counts grouped by severity (critical, high, medium, low) with total
- [ ] Deduplicates advisories by advisory ID before counting
- [ ] Returns 404 (`AppError::NotFound` or equivalent) when SBOM ID does not exist
- [ ] Uses `.context()` wrapping on database errors

## Test Requirements
- [ ] Unit test: verify correct severity counts with known test data (e.g., 2 critical, 3 high, 1 medium, 0 low)
- [ ] Unit test: verify deduplication — same advisory linked twice to an SBOM counts only once
- [ ] Unit test: verify 404 error for nonexistent SBOM ID

## Dependencies
- Depends on: Task 1 — Create advisory severity summary model
