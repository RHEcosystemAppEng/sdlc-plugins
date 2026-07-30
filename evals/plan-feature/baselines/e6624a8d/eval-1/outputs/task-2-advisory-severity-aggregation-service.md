## Repository
trustify-backend

## Target Branch
main

## Description
Add an advisory severity aggregation method to `SbomService` that queries the `sbom_advisory` join table to count unique advisories by severity level for a given SBOM ID. This method performs the server-side aggregation that replaces the current client-side counting approach, reducing multiple paginated API calls to a single database query.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_severity_summary(&self, sbom_id: Id) -> Result<AdvisorySeveritySummary, AppError>` method to SbomService

## Implementation Notes
- Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService: fetch, list, ingest) for method signature, error handling, and database access.
- Use SeaORM query builder to join `sbom_advisory` with `advisory` entity tables. Reference `entity/src/sbom_advisory.rs` for the join table schema and `entity/src/advisory.rs` for the advisory entity (which contains the severity field).
- Deduplicate by advisory ID as specified in the requirements — use `DISTINCT` or `GROUP BY` on the advisory ID column before counting by severity.
- Use the shared query helpers from `common/src/db/query.rs` where applicable for filtering.
- Return `AppError` with `.context()` wrapping for error handling, consistent with existing service methods.
- Per CONVENTIONS.md: all service methods return `Result<T, AppError>` with `.context()` wrapping for error propagation.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` service file scope.
- Per CONVENTIONS.md: use SeaORM for all database queries — do not use raw SQL.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` service file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with database access patterns, connection handling, and error wrapping to follow
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity definition
- `entity/src/advisory.rs` — Advisory entity with severity field

## Acceptance Criteria
- [ ] `SbomService` has a `get_advisory_severity_summary` method that returns `AdvisorySeveritySummary`
- [ ] The method counts unique advisories (deduplicated by advisory ID) grouped by severity level
- [ ] The method returns an error if the SBOM ID does not exist
- [ ] Severity counts are accurate for SBOMs with multiple advisories at the same severity level

## Test Requirements
- [ ] Unit test: verify severity counts are correct for an SBOM with advisories at each severity level
- [ ] Unit test: verify deduplication — same advisory linked twice returns count of 1
- [ ] Unit test: verify error is returned for a non-existent SBOM ID

## Dependencies
- Depends on: Task 1 — Add advisory severity summary response model
