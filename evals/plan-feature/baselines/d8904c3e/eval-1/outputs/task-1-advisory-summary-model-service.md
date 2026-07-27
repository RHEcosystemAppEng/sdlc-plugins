## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` model struct and a service method on `SbomService` that aggregates vulnerability advisory severity counts for a given SBOM. The service method queries the existing SBOM-advisory relationship tables, deduplicates advisories by ID, and returns counts grouped by severity level (critical, high, medium, low) plus a total count. This provides the data layer for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint defined in TC-9001.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct with fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`; derive `Serialize`, `Deserialize`, `Debug`, `Clone`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` and re-export `AdvisorySeveritySummary`
- `modules/fundamental/src/sbom/service/sbom.rs` — add `async fn advisory_severity_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
- Follow the established model pattern in `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary` struct) for struct definition, derives, and serde configuration.
- The service method should query `entity::sbom_advisory` joined with `entity::advisory` to get severity values. Use `SELECT COUNT(DISTINCT advisory.id)` grouped by `advisory.severity` to deduplicate advisories.
- Use SeaORM query builder (`sea_orm::QuerySelect`, `sea_orm::ColumnTrait`, `sea_orm::EntityTrait`) following the same patterns as existing queries in `SbomService` (e.g., the `fetch` and `list` methods in `modules/fundamental/src/sbom/service/sbom.rs`).
- Return `AppError::NotFound` (from `common/src/error.rs`) when the SBOM ID does not exist, consistent with the existing `get` handler in `modules/fundamental/src/sbom/endpoints/get.rs`.
- Error handling: wrap database errors with `.context("advisory severity aggregation")` per the established pattern.
- Per CONVENTIONS.md §Module Pattern: follow the `model/ + service/ + endpoints/` structure — the model goes in `model/advisory_summary.rs` and the service method goes in `service/sbom.rs`.
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for all fallible operations.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference struct for model definition patterns and serde derives
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with query patterns to follow for the new aggregation method
- `common/src/error.rs::AppError` — error enum with `NotFound` variant for SBOM-not-found case
- `entity/sbom_advisory.rs` — SeaORM entity for the SBOM-Advisory join table, provides the relationship needed for the count query
- `entity/advisory.rs` — Advisory entity with the `severity` field to group by

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with `critical`, `high`, `medium`, `low`, and `total` fields
- [ ] `SbomService::advisory_severity_summary` method returns correct severity counts for a given SBOM ID
- [ ] Advisory counts are deduplicated by advisory ID (same advisory linked multiple times is counted once)
- [ ] Method returns `AppError::NotFound` when the SBOM ID does not exist

## Test Requirements
- [ ] Unit test: `advisory_severity_summary` returns correct counts when SBOM has advisories at multiple severity levels
- [ ] Unit test: `advisory_severity_summary` deduplicates advisories linked multiple times to the same SBOM
- [ ] Unit test: `advisory_severity_summary` returns all-zero counts for an SBOM with no advisories
- [ ] Unit test: `advisory_severity_summary` returns `NotFound` error for non-existent SBOM ID

## Verification Commands
- `cargo build -p fundamental` — compiles without errors
- `cargo test -p fundamental -- advisory_summary` — all new tests pass

## Dependencies
- Depends on: None
