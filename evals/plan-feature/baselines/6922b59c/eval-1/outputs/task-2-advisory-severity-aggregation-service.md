## Repository
trustify-backend

## Target Branch
main

## Description
Add a severity aggregation method to `SbomService` that queries the `sbom_advisory` join table to count unique advisories per severity level for a given SBOM ID. The method deduplicates advisories by advisory ID (as required by the feature specification) and returns an `AdvisorySeveritySummary`. It must return a 404-equivalent error if the SBOM ID does not exist, consistent with existing SBOM service methods.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `async fn advisory_severity_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
The aggregation query should join `sbom_advisory` with `advisory` to access the severity field on `AdvisorySummary`. Use `GROUP BY severity` with `COUNT(DISTINCT advisory_id)` to deduplicate and count in a single database query rather than fetching all advisories and counting in Rust. This keeps the operation under the p95 < 200ms target for SBOMs with up to 500 advisories.

Before aggregating, verify the SBOM exists by calling the existing `SbomService::fetch` method (or equivalent). If the SBOM is not found, return `AppError::NotFound` to produce a 404 response.

Use `common/src/db/query.rs` helpers for building the query if applicable, and wrap database errors with `.context("advisory severity aggregation")` per the project error handling pattern.

Per CONVENTIONS.md §Error Handling: return `Result<AdvisorySeveritySummary, AppError>` and use `.context()` for all database error wrapping.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Module Pattern: add the service method within the existing `SbomService` impl block following the established method layout.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust module file scope.

## Reuse Candidates
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference for how service methods query advisory data and handle errors
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting that may be applicable to the aggregation query
- `entity/src/sbom_advisory.rs` — SeaORM entity definition for the SBOM-Advisory join table, needed for constructing the join query
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService::fetch` — existing method to verify SBOM existence before aggregating

## Acceptance Criteria
- [ ] `SbomService::advisory_severity_summary` method exists and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Method counts unique advisories per severity level (Critical, High, Medium, Low) using the `sbom_advisory` join table
- [ ] Duplicate advisory IDs are not double-counted
- [ ] The `total` field equals the sum of all severity counts
- [ ] Returns `AppError::NotFound` (404) when the SBOM ID does not exist
- [ ] Database errors are wrapped with `.context()` per error handling convention

## Test Requirements
- [ ] Unit/integration test: returns correct severity counts for an SBOM with known advisory data
- [ ] Unit/integration test: deduplicates advisories with the same ID linked multiple times
- [ ] Unit/integration test: returns 404 error for a non-existent SBOM ID
- [ ] Unit/integration test: returns all-zero counts for an SBOM with no linked advisories

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental advisory_severity` — service tests pass

## Dependencies
- Depends on: Task 1 — Add advisory severity summary response model
