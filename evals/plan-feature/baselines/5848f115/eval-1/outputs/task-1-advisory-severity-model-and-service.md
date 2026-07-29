## Repository
trustify-backend

## Target Branch
main

## Description
Add the `AdvisorySeveritySummary` response model and a severity aggregation query method to `SbomService`. The model represents the JSON response shape for the advisory-summary endpoint: `{ critical, high, medium, low, total }`. The service method queries the `sbom_advisory` join table to count unique advisories (deduplicated by advisory ID) grouped by severity level. This task provides the data layer that the endpoint handler (Task 2) will call.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new `AdvisorySeveritySummary` struct
- `modules/fundamental/src/sbom/service/sbom.rs` — add `get_advisory_severity_summary(sbom_id)` method to `SbomService`
- `modules/fundamental/Cargo.toml` — add any needed dependencies (if not already present)

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — define `AdvisorySeveritySummary` struct with `critical`, `high`, `medium`, `low`, `total` fields

## Implementation Notes
- Follow the existing module pattern: each domain module uses `model/ + service/ + endpoints/` structure. The new model struct belongs in `sbom/model/` since this is an SBOM-scoped aggregation.
- The `AdvisorySeveritySummary` struct should derive `Serialize`, `Deserialize`, `Debug`, and `Clone`, consistent with existing model structs like `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs`.
- The aggregation query should use the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find advisories linked to the given SBOM, then count by the severity field on the `advisory` entity (`entity/src/advisory.rs`).
- Deduplicate by advisory ID before counting — use `SELECT DISTINCT` or equivalent SeaORM query to ensure each advisory is counted only once per severity level.
- The service method should return `Result<AdvisorySeveritySummary, AppError>` following the error handling pattern in `common/src/error.rs` with `.context()` wrapping.
- If the SBOM ID does not exist, return a 404-appropriate error (use the same not-found pattern as `SbomService::fetch` in `modules/fundamental/src/sbom/service/sbom.rs`).
- Per Key Conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service file scope.
- Per Key Conventions: use SeaORM for database access. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's database access scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM model struct; follow its derive macros and serialization patterns
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — has severity field; reference its severity enum/type for consistency
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list methods; follow its error handling and query patterns
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; use this for the aggregation query
- `entity/src/advisory.rs` — Advisory entity with severity field
- `common/src/error.rs::AppError` — shared error type for Result returns
- `common/src/db/query.rs` — shared query builder helpers if needed for filtering

## Acceptance Criteria
- [ ] `AdvisorySeveritySummary` struct exists with fields: `critical: i64`, `high: i64`, `medium: i64`, `low: i64`, `total: i64`
- [ ] `SbomService::get_advisory_severity_summary(sbom_id)` returns correct severity counts for a given SBOM
- [ ] Advisories are deduplicated by advisory ID (each unique advisory counted once)
- [ ] Returns a not-found error when the SBOM ID does not exist
- [ ] `total` equals the sum of `critical + high + medium + low`

## Test Requirements
- [ ] Unit test: aggregation returns correct counts for an SBOM with known advisories at each severity level
- [ ] Unit test: aggregation returns all zeros for an SBOM with no linked advisories
- [ ] Unit test: duplicate advisory-SBOM links do not inflate counts
- [ ] Unit test: non-existent SBOM ID returns appropriate error

## Verification Commands
- `cargo build -p fundamental` — compiles without errors
- `cargo test -p fundamental` — all existing and new tests pass

## Dependencies
- None (first task in the chain)
