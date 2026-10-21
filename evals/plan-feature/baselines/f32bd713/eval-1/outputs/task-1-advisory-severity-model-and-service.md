## Repository
trustify-backend

## Target Branch
main

## Description
Add the AdvisorySeveritySummary response model and a severity aggregation service method to SbomService. The model struct holds deduplicated advisory counts grouped by severity level (critical, high, medium, low) plus a total count. The service method queries the sbom_advisory join table, joins to the advisory table to read severity, deduplicates by advisory ID, and returns the aggregated counts. This lays the foundation for the advisory-summary REST endpoint (Task 2).

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` -- AdvisorySeveritySummary struct with fields: critical (i64), high (i64), medium (i64), low (i64), total (i64); derive Serialize, Clone, Debug

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod advisory_summary;` and re-export AdvisorySeveritySummary
- `modules/fundamental/src/sbom/service/sbom.rs` -- add `async fn get_advisory_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method that queries entity::sbom_advisory joined with entity::advisory, groups by severity, deduplicates by advisory ID, and counts per severity level

## API Changes
- No external API changes in this task (service layer only)

## Implementation Notes
- The AdvisorySeveritySummary struct follows the same pattern as SbomSummary in `modules/fundamental/src/sbom/model/summary.rs` -- derive Serialize for JSON responses, implement Default for zero-count initialization.
- The aggregation query should use SeaORM's `select` with `group_by` on the advisory severity column from `entity/src/advisory.rs`, joined through `entity/src/sbom_advisory.rs`. Use `count()` aggregation and deduplicate by advisory ID using `DISTINCT` in the count expression.
- Follow the existing SbomService method patterns in `modules/fundamental/src/sbom/service/sbom.rs` for method signature, connection handling, and error wrapping with `.context()`.
- Return `AppError` (from `common/src/error.rs`) when the SBOM ID does not exist -- the caller (endpoint handler in Task 2) will map this to a 404 response.
- The AdvisorySummary struct in `modules/fundamental/src/advisory/model/summary.rs` includes a severity field -- use the same severity enum/type for consistency.
- Per CONVENTIONS.md §Module Pattern: create the new model file under `modules/fundamental/src/sbom/model/` following the existing model/ + service/ + endpoints/ structure. Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's Rust module file scope.
- Per CONVENTIONS.md §Error Handling: wrap database errors with `.context()` and return `Result<T, AppError>`. See `modules/fundamental/src/sbom/service/sbom.rs` for the established pattern. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service file scope.
- Per CONVENTIONS.md §Query Helpers: use shared query builder helpers from `common/src/db/query.rs` for building the aggregation query if applicable. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust query file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- example of a model struct with Serialize derive and standard field patterns
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- contains the severity field type to reuse for consistent severity classification
- `entity/src/sbom_advisory.rs` -- the join table entity for SBOM-Advisory relationships, used as the base for the aggregation query
- `common/src/db/query.rs` -- shared query builder helpers for filtering and aggregation

## Acceptance Criteria
- [ ] AdvisorySeveritySummary struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs` with fields: critical, high, medium, low, total
- [ ] AdvisorySeveritySummary is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] SbomService has a `get_advisory_summary` method that accepts an SBOM ID and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] The aggregation query deduplicates advisories by advisory ID before counting
- [ ] The method returns an error when the SBOM ID does not exist in the database

## Test Requirements
- [ ] Unit test: verify AdvisorySeveritySummary serializes to JSON with the expected field names
- [ ] Unit test: verify the aggregation query counts each severity level correctly when multiple advisories have the same severity
- [ ] Unit test: verify deduplication -- the same advisory linked to an SBOM multiple times is counted only once
- [ ] Unit test: verify the method returns an error for a non-existent SBOM ID

## Dependencies
- None (this is the first task in the chain)
