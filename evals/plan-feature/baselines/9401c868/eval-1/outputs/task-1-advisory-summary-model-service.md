## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model and a service method on `SbomService` that aggregates advisory severity counts for a given SBOM. The service method queries the `sbom_advisory` join table, deduplicates by advisory ID, groups by severity, and returns counts for Critical, High, Medium, Low, and a total. This provides the data layer for the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint defined in TC-9001.

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — Define the `AdvisorySeveritySummary` struct with fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`. Derive `Serialize`, `Deserialize`, `Debug`, `Clone`.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod advisory_summary;` and re-export the `AdvisorySeveritySummary` type
- `modules/fundamental/src/sbom/service/sbom.rs` — Add an `advisory_severity_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method that queries the `sbom_advisory` table joined with `advisory` to aggregate severity counts, and a variant `advisory_severity_summary_filtered(&self, sbom_id: Uuid, threshold: Option<Severity>) -> Result<AdvisorySeveritySummary, AppError>` that filters counts at or above a given severity threshold

## Implementation Notes
Per CONVENTIONS.md §Module pattern: place the new model struct in `modules/fundamental/src/sbom/model/advisory_summary.rs` following the established `model/ + service/ + endpoints/` structure. Each domain concept gets its own file within the model directory.
Applies: task creates `modules/fundamental/src/sbom/model/advisory_summary.rs` matching the convention's module directory structure scope.

Per CONVENTIONS.md §Error handling: all service methods must return `Result<T, AppError>` and use `.context()` wrapping for error propagation. Follow the pattern in existing methods in `modules/fundamental/src/sbom/service/sbom.rs`.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Query helpers: use the shared query builder helpers from `common/src/db/query.rs` for constructing the aggregation query if applicable. The aggregation query should use SeaORM's `select` with `group_by` and `count` on the advisory severity column.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` file scope.

The aggregation query must deduplicate advisories by advisory ID before counting severities, as a single advisory may be linked to an SBOM multiple times through different vulnerability paths. Use `DISTINCT` on the advisory ID in the query.

The SBOM existence check should return a 404-compatible error (via `AppError`) when the SBOM ID does not exist, consistent with existing SBOM service methods in `sbom.rs`.

## Reuse Candidates
- `entity/src/sbom_advisory.rs::SbomAdvisory` — The SBOM-Advisory join table entity; use this for the aggregation query join
- `entity/src/advisory.rs::Advisory` — The Advisory entity containing the severity field to group by
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference for how severity is represented in the existing advisory model
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — Standard error type for service method return values

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists in `modules/fundamental/src/sbom/model/advisory_summary.rs` with `critical`, `high`, `medium`, `low`, and `total` fields
- [ ] `AdvisorySeveritySummary` is exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] `SbomService` has an `advisory_severity_summary` method that returns correct counts for a given SBOM ID
- [ ] Advisories are deduplicated by advisory ID before counting
- [ ] Method returns an appropriate `AppError` when the SBOM ID does not exist
- [ ] Threshold filtering returns only counts at or above the specified severity level
- [ ] Total field reflects the sum of the returned severity counts (respecting any threshold filter)

## Test Requirements
- [ ] Unit test: service method returns correct severity counts for an SBOM with known advisory associations
- [ ] Unit test: service method deduplicates advisories linked through multiple paths
- [ ] Unit test: service method returns zero counts for an SBOM with no advisories
- [ ] Unit test: service method returns `AppError` for a nonexistent SBOM ID
- [ ] Unit test: threshold filtering correctly excludes severities below the threshold
- [ ] Unit test: total field equals the sum of individual severity counts

## Verification Commands
- `cargo build -p trustify-fundamental` — Compiles without errors
- `cargo test -p trustify-fundamental -- advisory_summary` — All advisory summary service tests pass

## Dependencies
None
