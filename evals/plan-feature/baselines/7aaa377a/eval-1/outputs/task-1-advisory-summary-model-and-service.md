# Task 1 — Add AdvisorySeveritySummary model and aggregation service method

## Repository
trustify-backend

## Target Branch
main

## Description
Add a new `AdvisorySeveritySummary` response model and a corresponding aggregation method on `SbomService` that counts unique advisories by severity level for a given SBOM. This provides the data layer for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint (Task 2). The aggregation must deduplicate advisories by advisory ID before counting, using the existing `sbom_advisory` join table and `advisory` table.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`. Derive `Serialize`, `Deserialize`, `Debug`, `Clone`, `PartialEq`, `ToSchema` (for OpenAPI).

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export the struct
- `modules/fundamental/src/sbom/service/sbom.rs` — add `advisory_summary(&self, sbom_id: Id) -> Result<AdvisorySeveritySummary, AppError>` method that performs the aggregation query

## Implementation Notes
- The aggregation query should join `sbom_advisory` with `advisory` on advisory ID, filter by the given SBOM ID, select distinct advisory IDs (to handle deduplication per the requirement), then group by the `severity` field on the `advisory` entity.
- Use SeaORM query builder. Reference the existing query patterns in `common/src/db/query.rs` for building filtered queries.
- The `advisory` entity (`entity/src/advisory.rs`) contains the `severity` field. The `sbom_advisory` entity (`entity/src/sbom_advisory.rs`) provides the join between SBOMs and advisories.
- Follow the existing `SbomService` method signatures in `modules/fundamental/src/sbom/service/sbom.rs` — methods take `&self` and return `Result<T, AppError>`.
- Return 404 (`AppError::NotFound`) if the SBOM ID does not exist, consistent with existing SBOM endpoints. Check SBOM existence before running the aggregation query.
- Per Key Conventions §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping on database errors.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` file scope.
- Per Key Conventions §Module pattern: follow the `model/ + service/ + endpoints/` structure. This task covers model and service layers.
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; use this for the join query
- `entity/src/advisory.rs` — Advisory entity with severity field; use for grouping by severity
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing advisory summary struct that includes severity field; reference for severity field naming and type
- `common/src/error.rs::AppError` — error type for service return values; reuse `AppError::NotFound` for missing SBOM
- `common/src/db/query.rs` — shared query builder helpers; reuse for constructing the aggregation query

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical`, `high`, `medium`, `low`, `total` (all `u64`)
- [ ] `SbomService::advisory_summary(sbom_id)` returns correct severity counts for a given SBOM
- [ ] Advisories are deduplicated by advisory ID before counting
- [ ] Returns `AppError::NotFound` when SBOM ID does not exist
- [ ] Struct derives `Serialize`, `Deserialize`, and `ToSchema` for API and OpenAPI compatibility

## Test Requirements
- [ ] Unit test: `advisory_summary` returns correct counts for an SBOM with known advisories at each severity level
- [ ] Unit test: `advisory_summary` deduplicates advisories linked multiple times to the same SBOM
- [ ] Unit test: `advisory_summary` returns all zeros for an SBOM with no linked advisories
- [ ] Unit test: `advisory_summary` returns 404 error for a nonexistent SBOM ID

## Dependencies
- None (this is the foundational task)
