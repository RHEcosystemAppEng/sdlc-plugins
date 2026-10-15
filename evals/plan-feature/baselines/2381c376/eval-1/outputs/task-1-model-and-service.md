## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model and an aggregation service method to `SbomService` that queries the `sbom_advisory` join table, deduplicates advisories by ID, groups them by severity level (Critical, High, Medium, Low), and returns the counts along with a total. This provides the data layer for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint defined in TC-9001.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct with `critical`, `high`, `medium`, `low`, `total` fields, deriving `Serialize` and `Deserialize`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`
- `modules/fundamental/src/sbom/service/sbom.rs` — add `async fn advisory_severity_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method that queries `sbom_advisory` joined with `advisory` to aggregate severity counts

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) for struct layout, derive macros, and serialization annotations.
- The aggregation query should join `entity::sbom_advisory` with `entity::advisory` on advisory ID, filter by the given SBOM ID, and use `SELECT COUNT(DISTINCT advisory.id)` grouped by `advisory.severity` to deduplicate advisories.
- Use SeaORM query builder patterns from `common/src/db/query.rs` for constructing the aggregation query.
- The service method must return `AppError::NotFound` (from `common/src/error.rs`) when no SBOM with the given ID exists. Check SBOM existence before running the aggregation query, following the pattern in `modules/fundamental/src/sbom/service/sbom.rs` (the existing `fetch` method).
- Wrap database errors with `.context()` per the error handling convention.
- Per CONVENTIONS.md §Module Pattern: follow the `model/ + service/` structure for the new model and service method.
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's model directory scope.
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` with `.context()` wrapping on all database calls.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md §Query Helpers: use shared filtering and query builder helpers from `common/src/db/query.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reuse for constructing the aggregation query
- `common/src/error.rs` — `AppError` enum with `NotFound` variant; reuse for SBOM-not-found error
- `modules/fundamental/src/sbom/model/summary.rs` — `SbomSummary` struct; follow its derive macros and serialization pattern for the new model

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with `critical`, `high`, `medium`, `low`, and `total` fields (all integer types)
- [ ] `AdvisorySeveritySummary` is exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] `SbomService` has an `advisory_severity_summary` method that returns correct severity counts for a given SBOM ID
- [ ] Advisories are deduplicated by advisory ID before counting (no double-counting)
- [ ] Method returns `AppError::NotFound` when the SBOM ID does not exist
- [ ] Database errors are wrapped with `.context()` for clear error messages

## Test Requirements
- [ ] Unit test: verify `AdvisorySeveritySummary` serializes to the expected JSON shape `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Service-level test: verify correct severity counts with a known set of advisories linked to an SBOM
- [ ] Service-level test: verify deduplication — linking the same advisory twice does not double-count
- [ ] Service-level test: verify `NotFound` error when SBOM ID does not exist

## Dependencies
- None (first task in the chain)
