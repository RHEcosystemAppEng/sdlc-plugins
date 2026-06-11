## Repository
trustify-backend

## Target Branch
main

## Description
Add an `AdvisorySeveritySummary` response model and a service method on `SbomService` that aggregates advisory severity counts for a given SBOM. The service method queries the `sbom_advisory` join table, deduplicates by advisory ID, groups by severity level, and returns counts for Critical, High, Medium, Low, and a total. This provides the data layer for the new advisory summary endpoint (TC-9001).

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — AdvisorySeveritySummary struct with fields: critical, high, medium, low, total (all u64), deriving Serialize, Deserialize, ToSchema

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export AdvisorySeveritySummary
- `modules/fundamental/src/sbom/service/sbom.rs` — add `advisory_severity_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method that queries the sbom_advisory table joined with advisory to count severities

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails) for struct conventions (derive macros, serde attributes, utoipa ToSchema).
- The `AdvisorySeveritySummary` struct should derive `serde::Serialize`, `serde::Deserialize`, and `utoipa::ToSchema` consistent with sibling model structs.
- The service method should be added to `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`, following the existing patterns for `fetch` and `list` methods.
- Use SeaORM query builder to join `entity::sbom_advisory` with `entity::advisory` on advisory ID, filter by the given SBOM ID, select distinct advisory IDs to avoid double-counting, and group by severity field from `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs` for the severity field definition).
- Use `common/src/db/query.rs` query helpers if applicable for building the query.
- Return `AppError` with `.context()` wrapping for error handling, consistent with `common/src/error.rs` patterns.
- The method should return a 404-equivalent error (AppError::NotFound or similar) if the SBOM ID does not exist, checking SBOM existence before running the aggregation query. Follow the pattern in the existing `get` endpoint at `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per docs/constraints.md section 5 (Code Change Rules): changes must be scoped to the files listed, code must not be modified without first inspecting it, and implementation must follow the patterns referenced in these notes.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing model struct demonstrating the derive macro pattern and struct conventions to follow
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition; reference this to understand the severity enum/type used in the advisory entity
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — the service where the new method will be added; existing methods show the query pattern and error handling approach
- `entity/src/sbom_advisory.rs` — the join table entity that links SBOMs to advisories; this is the primary table to query for aggregation
- `common/src/error.rs::AppError` — error enum used across all services for consistent error handling

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: critical (u64), high (u64), medium (u64), low (u64), total (u64)
- [ ] `AdvisorySeveritySummary` derives Serialize, Deserialize, and ToSchema
- [ ] `SbomService` has a method that returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] The service method deduplicates advisories by advisory ID before counting
- [ ] The service method returns a not-found error if the SBOM ID does not exist
- [ ] The service method correctly counts advisories at each severity level

## Test Requirements
- [ ] Unit test for AdvisorySeveritySummary serialization (verify JSON field names match the expected response shape: critical, high, medium, low, total)
- [ ] The service method is testable via integration tests (covered in Task 4)

## Dependencies
- None
