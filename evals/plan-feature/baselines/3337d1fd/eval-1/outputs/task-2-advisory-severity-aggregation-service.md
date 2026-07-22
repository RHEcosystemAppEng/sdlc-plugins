## Repository
trustify-backend

## Target Branch
main

## Description
Implement the advisory severity aggregation query in `SbomService` that counts unique advisories by severity level for a given SBOM. This service method performs the database aggregation that powers the advisory-summary endpoint, deduplicating advisories by ID and grouping counts by severity.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `advisory_summary` method to `SbomService`

## Implementation Notes
Add a method `pub async fn advisory_summary(&self, sbom_id: Id, db: &impl ConnectionTrait) -> Result<AdvisorySeveritySummary, AppError>` to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`. First verify the SBOM exists by querying the `sbom` entity from `entity/src/sbom.rs`; return 404 via `AppError` if not found, consistent with existing SBOM endpoints like those in `modules/fundamental/src/sbom/endpoints/get.rs`. Join the `sbom_advisory` entity from `entity/src/sbom_advisory.rs` with the `advisory` entity from `entity/src/advisory.rs` to access the severity field from `AdvisorySummary` (defined in `modules/fundamental/src/advisory/model/summary.rs`). Use SeaORM `select` with `group_by` on severity and `count` on distinct advisory IDs. Use error handling with `.context()` wrapping as specified by the error handling convention in `common/src/error.rs`.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering
- `common/src/error.rs::AppError` — Error type for 404 and internal error responses
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for the aggregation query
- `entity/src/advisory.rs` — Advisory entity containing the severity field

## Acceptance Criteria
- [ ] `SbomService::advisory_summary` returns correct severity counts for a given SBOM ID
- [ ] Advisory counts are deduplicated by advisory ID
- [ ] Returns 404 AppError when SBOM ID does not exist
- [ ] Returns zero counts for all severities when SBOM has no linked advisories
- [ ] Code compiles without warnings

## Test Requirements
- [ ] Unit test: advisory_summary returns correct counts for SBOM with mixed-severity advisories
- [ ] Unit test: advisory_summary returns 404 for nonexistent SBOM ID
- [ ] Unit test: advisory_summary returns all zeros for SBOM with no advisories
- [ ] Unit test: advisory_summary deduplicates advisories linked multiple times

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental` — all tests pass

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model