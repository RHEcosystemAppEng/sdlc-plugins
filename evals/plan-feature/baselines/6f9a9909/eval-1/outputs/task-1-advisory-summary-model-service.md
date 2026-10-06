## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response model struct and add an `advisory_summary()` aggregation method to `SbomService`. The model holds severity counts (critical, high, medium, low, total) for advisories linked to a given SBOM. The service method queries the `sbom_advisory` join table, joins with the `advisory` table to read severity, deduplicates by advisory ID, groups by severity level, and returns the counts. Returns an error when the SBOM ID does not exist, consistent with existing SBOM service methods.

This is the data layer foundation for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint defined in Feature TC-9001.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct with fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`; derives `Serialize`, `Deserialize`, `Debug`, `Clone`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`
- `modules/fundamental/src/sbom/service/sbom.rs` — add `async fn advisory_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## API Changes
- None at this layer (service-only; the endpoint is added in Task 2)

## Implementation Notes
- Follow the model struct pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) for struct definition, derive macros, and field naming.
- Follow the service method pattern in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService::fetch`, `SbomService::list`) for method signature and error handling.
- Use SeaORM to build the aggregation query: join `entity::sbom_advisory` with `entity::advisory` on advisory ID, filter by the given SBOM ID, use `SELECT DISTINCT` on advisory ID before grouping by severity to ensure deduplication.
- Reference `entity/src/sbom_advisory.rs` for the join table entity definition and `entity/src/advisory.rs` for the advisory entity (which includes the `severity` field).
- Use `common/src/db/query.rs` query builder helpers if applicable for filtering.
- When the SBOM ID does not exist, return `AppError::NotFound` (see `common/src/error.rs` for the error enum).
- Per CONVENTIONS.md §Module Pattern: follow the `model/ + service/ + endpoints/` structure for the sbom module. Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's module file scope.
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` with `.context()` wrapping on fallible operations. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's handler/service file scope.
- Per docs/constraints.md §5 (Code Change Rules): changes must be scoped to the listed files; reuse existing utilities (SeaORM entities, AppError) rather than duplicating.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — pattern for response model struct definition with serde derives
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with methods to follow for signature, error handling, and database interaction patterns
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for the aggregation query
- `entity/src/advisory.rs` — Advisory entity containing the severity field
- `common/src/error.rs::AppError` — shared error type for 404 and other error responses
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs` with fields: `critical`, `high`, `medium`, `low`, `total` (all `i64`)
- [ ] `AdvisorySeveritySummary` derives `Serialize`, `Deserialize`, `Debug`, `Clone`
- [ ] `SbomService::advisory_summary(sbom_id)` method exists and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] The aggregation query deduplicates advisories by advisory ID before counting
- [ ] The method returns `AppError::NotFound` when the SBOM ID does not exist
- [ ] `modules/fundamental/src/sbom/model/mod.rs` re-exports `AdvisorySeveritySummary`

## Test Requirements
- [ ] Test that `advisory_summary()` returns correct counts for an SBOM with known advisories at multiple severity levels
- [ ] Test that `advisory_summary()` deduplicates advisories linked to the same SBOM multiple times
- [ ] Test that `advisory_summary()` returns a not-found error for a non-existent SBOM ID
- [ ] Test that `advisory_summary()` returns zero counts for an SBOM with no linked advisories

## Dependencies
None
