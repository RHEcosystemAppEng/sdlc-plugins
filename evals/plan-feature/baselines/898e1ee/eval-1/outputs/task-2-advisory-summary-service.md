# Task 2 — Advisory Severity Aggregation Service Method

## Repository
trustify-backend

## Target Branch
main

## Description
Add a `get_advisory_severity_summary` method to `SbomService` that queries the database for aggregated advisory severity counts for a given SBOM ID. The method joins the `sbom_advisory` join table with the `advisory` table, groups by severity, deduplicates by advisory ID, and returns an `AdvisorySeveritySummary`. It also supports an optional `SeverityThreshold` parameter to filter counts to only severities at or above the given threshold.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `pub async fn get_advisory_severity_summary(&self, sbom_id: Uuid, threshold: Option<SeverityThreshold>, db: &DatabaseConnection) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`. The method must: (1) verify the SBOM exists by querying `entity::sbom` and return `AppError::NotFound` if absent, (2) query `entity::sbom_advisory` joined with `entity::advisory`, (3) use `SELECT COUNT(DISTINCT advisory_id)` grouped by severity, (4) map results into `AdvisorySeveritySummary` fields, (5) if threshold is provided, zero out severity levels below the threshold.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination; review for reusable query construction patterns.
- `common/src/error.rs::AppError` — Use `AppError::NotFound` for missing SBOM, `AppError` variants with `.context()` for database errors.
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service struct to add the method to; follow the pattern of existing methods like `fetch` and `list` for database connection handling and error wrapping.
- `entity/src/sbom_advisory.rs` — SeaORM entity for the join table; use its `Column` and `Relation` definitions for the join query.
- `entity/src/advisory.rs` — Advisory entity; use its `Column::Severity` for grouping.

## Implementation Notes
Follow the existing method patterns in `modules/fundamental/src/sbom/service/sbom.rs` — methods accept a `&DatabaseConnection` parameter, use SeaORM `Entity::find()` with filters, and wrap errors with `.context("descriptive message")` returning `Result<T, AppError>`.

The aggregation query should use SeaORM's `select_only()`, `column_as()`, and `group_by()` methods to build a `SELECT advisory.severity, COUNT(DISTINCT sbom_advisory.advisory_id) FROM sbom_advisory JOIN advisory ON ... WHERE sbom_advisory.sbom_id = ? GROUP BY advisory.severity` query.

Per CONVENTIONS.md §Framework: use SeaORM for database access. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` file scope.

## Acceptance Criteria
- [ ] `SbomService::get_advisory_severity_summary` method exists and compiles
- [ ] Method returns `AdvisorySeveritySummary` with correct counts for each severity level
- [ ] Method deduplicates advisories by advisory ID before counting
- [ ] Method returns `AppError::NotFound` when SBOM ID does not exist
- [ ] Method accepts optional `SeverityThreshold` and zeros out lower-severity counts when provided
- [ ] `cargo check` passes with no errors

## Test Requirements
- [ ] Unit test (with mocked DB or test fixtures) verifying correct severity counts for an SBOM with known advisories
- [ ] Unit test verifying `NotFound` error when SBOM ID does not exist
- [ ] Unit test verifying threshold filtering zeros out lower severity counts

## Dependencies
- Depends on: Task 1 — Advisory Severity Summary Model (provides `AdvisorySeveritySummary` and `SeverityThreshold` types)

[sdlc-workflow] Description digest: sha256-md:ab03e3570472c449324e80fe9880800940e45ce5880011149b1a1e6aa28e4e42
