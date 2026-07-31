## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model and the service-layer query method that aggregates advisory severity counts for a given SBOM. This provides the data layer for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The service method queries the existing `sbom_advisory` join table, groups advisories by severity level (Critical, High, Medium, Low), deduplicates by advisory ID, and returns a summary struct with counts and a total. Returns a 404 error if the SBOM ID does not exist, consistent with existing SBOM endpoints.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct with fields: `critical`, `high`, `medium`, `low`, `total` (all integer counts)

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` to expose the new model
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_summary(&self, sbom_id: Id) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }` (this task adds the model and service; the endpoint handler is wired in Task 2)

## Implementation Notes
- The `AdvisorySeveritySummary` struct should derive `Serialize`, `Deserialize`, `Debug`, `Clone`, and `utoipa::ToSchema` for OpenAPI generation, following the pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`).
- The service method should use SeaORM to query the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) and join with the `advisory` entity (`entity/src/advisory.rs`) to access the severity field.
- Deduplication: use `GROUP BY advisory.id` or `DISTINCT` on advisory ID before counting by severity to ensure each advisory is counted only once even if linked multiple times.
- Error handling: use `Result<AdvisorySeveritySummary, AppError>` with `.context()` wrapping per the project's error handling convention. Return `AppError::NotFound` if the SBOM does not exist, consistent with `modules/fundamental/src/sbom/service/sbom.rs` existing fetch methods.
- Per repo Key Conventions §Module pattern: follow the `model/ + service/ + endpoints/` structure. The model goes in `model/advisory_summary.rs`, the service method goes in `service/sbom.rs`.
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's `.rs` module file scope.
- Per repo Key Conventions §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. See `modules/fundamental/src/sbom/service/sbom.rs` for the established pattern.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `entity/src/sbom_advisory.rs` — the SBOM-Advisory join table entity; use this for the aggregation query
- `entity/src/advisory.rs` — the Advisory entity containing the severity field
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for how severity is represented in the existing codebase
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error type to use for 404 and internal error responses
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for model struct patterns (derive macros, field types)

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs` with fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`
- [ ] `SbomService::get_advisory_summary` method exists and returns correct severity counts from the `sbom_advisory` join table
- [ ] Advisory counts are deduplicated by advisory ID (each advisory counted once regardless of how many times it is linked)
- [ ] Method returns `AppError::NotFound` (404-equivalent) when the SBOM ID does not exist
- [ ] The model module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit or integration test verifying correct severity count aggregation for an SBOM with known advisories at each severity level
- [ ] Test verifying deduplication: an advisory linked to the same SBOM multiple times is counted only once
- [ ] Test verifying 404 response when querying a non-existent SBOM ID
- [ ] Test verifying correct counts when an SBOM has zero advisories (all counts should be 0)

## Verification Commands
- `cargo build --workspace` — project compiles without errors
- `cargo test -p fundamental` — fundamental module tests pass

## Dependencies
- None (this is the foundational task)
