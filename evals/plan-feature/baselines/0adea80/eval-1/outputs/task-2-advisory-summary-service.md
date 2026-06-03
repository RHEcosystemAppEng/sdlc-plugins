# Task 2 — Add advisory severity aggregation service method

## Repository
trustify-backend

## Target Branch
main

## Description
Add an `advisory_summary` method to `SbomService` that queries the database to compute aggregated severity counts for all advisories linked to a given SBOM. The method must join the `sbom_advisory` table with the `advisory` table, deduplicate by advisory ID, group by severity level, and return an `AdvisorySeveritySummary` struct. It must return a 404-compatible error if the SBOM ID does not exist.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `advisory_summary` method to `SbomService`

## Implementation Notes
- Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService` methods like `fetch` and `list`). These methods accept a database connection/transaction parameter and return `Result<T, AppError>`.
- The query should:
  1. First verify the SBOM exists by querying the `sbom` entity. If not found, return an `AppError` 404 error consistent with existing SBOM endpoint behavior (see `modules/fundamental/src/sbom/endpoints/get.rs` for the 404 pattern).
  2. Query the `sbom_advisory` entity (`entity/src/sbom_advisory.rs`) joining to the `advisory` entity (`entity/src/advisory.rs`) to get advisory severity values.
  3. Use `DISTINCT` on advisory ID to deduplicate (requirement: count only unique advisories).
  4. Use a `GROUP BY severity` with `COUNT(*)` to aggregate counts per severity level, or alternatively fetch distinct advisory severities and count in Rust.
  5. Map the grouped results into the `AdvisorySeveritySummary` struct.
- Use SeaORM query builder patterns consistent with existing service code. Reference `common/src/db/query.rs` for shared query helpers if applicable.
- The method signature should be approximately: `pub async fn advisory_summary(&self, sbom_id: <IdType>, db: &impl ConnectionTrait) -> Result<AdvisorySeveritySummary, AppError>`
- Per docs/constraints.md Section 5 (Code Change Rules): changes must be scoped to the files listed; code must not duplicate existing functionality; implementation must follow referenced patterns.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct and method patterns (fetch, list, ingest) to follow for the new method
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — demonstrates querying advisory-related entities and may show severity field access patterns
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting
- `common/src/error.rs::AppError` — error enum with 404 and context wrapping patterns
- `entity/src/sbom_advisory.rs` — the join table entity between SBOMs and advisories

## Acceptance Criteria
- [ ] `SbomService` has an `advisory_summary` method that returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Method returns 404 error when SBOM ID does not exist
- [ ] Method deduplicates advisories by advisory ID before counting
- [ ] Method correctly aggregates counts for critical, high, medium, and low severity levels
- [ ] Method computes the `total` field as the sum of all severity counts
- [ ] Method compiles and integrates with existing `SbomService`

## Test Requirements
- [ ] Unit or integration test: returns correct severity counts for an SBOM with known advisories at each severity level
- [ ] Unit or integration test: returns all-zero counts for an SBOM with no linked advisories
- [ ] Unit or integration test: returns 404 error for a non-existent SBOM ID
- [ ] Unit or integration test: correctly deduplicates advisories (same advisory linked to SBOM multiple times is counted once)

## Verification Commands
- `cargo build -p trustify-module-fundamental` — should compile without errors
- `cargo test -p trustify-module-fundamental` — service tests should pass

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary response model
