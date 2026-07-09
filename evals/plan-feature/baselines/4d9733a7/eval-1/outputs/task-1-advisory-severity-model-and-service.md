## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model and the severity aggregation query method to `SbomService`. The model represents the response shape for the advisory severity aggregation endpoint (`GET /api/v2/sbom/{id}/advisory-summary`), containing counts of unique advisories at each severity level (critical, high, medium, low) plus a total count. The service method queries the `sbom_advisory` join table, joins with the `advisory` entity to access the severity field, deduplicates by advisory ID, and groups counts by severity level.

This task lays the data-access foundation that the endpoint handler (Task 2) will call.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`. Derive `Serialize`, `Debug`, `Clone`.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`
- `modules/fundamental/src/sbom/service/sbom.rs` — add `async fn advisory_severity_summary(&self, sbom_id: Id) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) for struct layout and derive macros.
- The severity field is on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` — use this to understand the severity enum or string type.
- Use the `sbom_advisory` join entity (`entity/src/sbom_advisory.rs`) to find advisories linked to a given SBOM. Join with `advisory` entity (`entity/src/advisory.rs`) to access the severity field.
- Deduplicate by advisory ID before counting — the same advisory may be linked to an SBOM through multiple paths.
- The service method should return `Result<AdvisorySeveritySummary, AppError>` following the error handling pattern in existing service methods.
- Use query helpers from `common/src/db/query.rs` if applicable for building the aggregation query.
- Per CONVENTIONS.md §Error Handling: wrap database errors with `.context()` for meaningful error messages.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ structure for the new model file.
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's module structure scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM model struct; follow its derive macros and layout pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field; reference for severity value types
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; use for the aggregation query
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with `critical`, `high`, `medium`, `low`, `total` fields
- [ ] `SbomService::advisory_severity_summary` method queries the database and returns correct severity counts
- [ ] Advisories are deduplicated by advisory ID before counting
- [ ] Method returns `AppError` with appropriate context on database errors

## Test Requirements
- [ ] Unit test: service method returns correct counts for an SBOM with known advisory severities
- [ ] Unit test: service method deduplicates advisories linked through multiple paths
- [ ] Unit test: service method returns all-zero counts for an SBOM with no linked advisories

## Dependencies
- None
