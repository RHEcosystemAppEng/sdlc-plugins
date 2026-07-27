# Task 1 — Add AdvisorySeveritySummary model and severity aggregation service method

## Repository
trustify-backend

## Target Branch
main

## Description
Create the `AdvisorySeveritySummary` response model and add a severity aggregation method to `SbomService`. This provides the data layer for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The aggregation query must join the `sbom_advisory` table with the `advisory` table, group by severity level (Critical, High, Medium, Low), count unique advisories (deduplicated by advisory ID), and return a summary struct with individual severity counts and a total.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` struct with `critical`, `high`, `medium`, `low`, `total` fields (all `u64`), deriving `Serialize`, `Deserialize`, `Debug`, `Clone`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod advisory_summary;` to register the new model module
- `modules/fundamental/src/sbom/service/sbom.rs` — add `async fn advisory_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method that queries severity counts from the `sbom_advisory` join table

## Implementation Notes
- Follow the existing module pattern (`model/` + `service/` + `endpoints/`). The `SbomSummary` struct in `modules/fundamental/src/sbom/model/summary.rs` demonstrates the established model pattern — use the same derive macros and struct conventions.
  Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's Rust module scope.
- Use SeaORM query builder to join `sbom_advisory` and `advisory` entities. Reference the join table entity at `entity/src/sbom_advisory.rs` and advisory entity at `entity/src/advisory.rs` for column and relation definitions.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service scope.
- The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a `severity` field — use the same severity enum/type for consistency.
- Error handling: wrap database errors with `.context()` per the project's `AppError` pattern (see `common/src/error.rs`).
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust error handling scope.
- Deduplicate advisories by advisory ID before counting — use `DISTINCT` in the SQL query or SeaORM equivalent to avoid double-counting advisories linked through multiple paths.
- Per the non-functional requirement: do not create new database tables — use existing `sbom_advisory` relationship table.

## Reuse Candidates
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; provides the relation between SBOMs and advisories needed for the aggregation query
- `entity/src/advisory.rs` — Advisory entity; contains the severity field used for grouping
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing advisory summary struct; reference its severity field type for consistency
- `common/src/db/query.rs` — shared query builder helpers; may provide reusable filtering/grouping utilities
- `common/src/error.rs::AppError` — error enum with `IntoResponse` implementation; use for error handling in the new service method

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with `critical`, `high`, `medium`, `low`, `total` fields
- [ ] `SbomService::advisory_summary(sbom_id)` returns correct severity counts from the database
- [ ] Advisory counts are deduplicated by advisory ID (no double-counting)
- [ ] Method returns `AppError` with appropriate context on database failure

## Test Requirements
- [ ] Unit test: `advisory_summary` returns correct counts for an SBOM with known advisory severity distribution
- [ ] Unit test: `advisory_summary` deduplicates advisories linked through multiple paths
- [ ] Unit test: `advisory_summary` returns all-zero counts for an SBOM with no advisories

## Verification Commands
- `cargo build -p fundamental` — compiles without errors
- `cargo test -p fundamental -- advisory_summary` — all tests pass

## Dependencies
- None (this is the foundational task)
