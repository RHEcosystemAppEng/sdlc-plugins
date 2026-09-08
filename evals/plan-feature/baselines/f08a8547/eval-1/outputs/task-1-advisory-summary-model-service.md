## Repository
trustify-backend

## Target Branch
main

## Description
Add the advisory severity count model and service method to support the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint (TC-9001). This task creates the response model struct and the database aggregation logic that queries the `sbom_advisory` join table, deduplicates advisories by ID, and groups counts by severity level (critical, high, medium, low). The service method returns the total count alongside per-severity counts.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new `AdvisorySeverityCounts` model
- `modules/fundamental/src/sbom/service/sbom.rs` — add `advisory_severity_counts` method to `SbomService`

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — define `AdvisorySeverityCounts` struct with fields: `critical`, `high`, `medium`, `low`, `total`

## Implementation Notes
- The aggregation query should join `sbom_advisory` with `advisory` to access the severity field, filter by the given SBOM ID, deduplicate by advisory ID (use `DISTINCT` or `GROUP BY advisory_id`), and count by severity level.
- Use SeaORM query builder for the aggregation. If a raw SQL query is needed for the `GROUP BY` aggregation, use SeaORM's `Statement::from_string` or `ConnectionTrait::query_all` pattern.
- The `AdvisorySeverityCounts` struct should derive `Serialize`, `Deserialize`, `Debug`, `Clone` for JSON serialization and standard Rust traits.
- The service method should return `Result<AdvisorySeverityCounts, AppError>` and use `.context()` for error wrapping.
- Validate that the SBOM exists before running the aggregation query; return an appropriate error (mapped to 404 by `AppError`) if not found.
- Per CONVENTIONS.md §Module Pattern: follow the `model/ + service/ + endpoints/` directory structure by placing the model in `model/advisory_summary.rs` and the service method in `service/sbom.rs`.
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` from the service method and use `.context()` wrapping on fallible operations.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust handler scope.

## Reuse Candidates
- `common/src/error.rs::AppError` — error enum implementing `IntoResponse`; use for the service method return type
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; use as the primary query source for aggregation
- `entity/src/advisory.rs` — Advisory entity containing the severity field for counting
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for the severity field values and naming conventions
- `common/src/db/query.rs` — shared query builder helpers; evaluate for reuse in constructing the aggregation query

## Acceptance Criteria
- [ ] `AdvisorySeverityCounts` struct is defined with `critical`, `high`, `medium`, `low`, and `total` fields (all integer types)
- [ ] `SbomService::advisory_severity_counts(sbom_id)` returns correct severity counts for a given SBOM
- [ ] Advisories are deduplicated by advisory ID before counting (an advisory linked multiple times is counted once)
- [ ] Service method returns an error (mappable to 404) when the SBOM ID does not exist
- [ ] The `total` field equals the sum of `critical + high + medium + low`

## Test Requirements
- [ ] Unit or integration test verifying that `advisory_severity_counts` returns correct counts for an SBOM with known advisory-severity distribution
- [ ] Test verifying deduplication: an advisory linked to the same SBOM multiple times is counted only once
- [ ] Test verifying that a non-existent SBOM ID returns an error

## Dependencies
- None
