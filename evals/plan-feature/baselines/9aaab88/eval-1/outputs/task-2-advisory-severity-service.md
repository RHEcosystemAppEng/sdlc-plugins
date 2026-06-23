## Repository
trustify-backend

## Target Branch
main

## Description
Add a service method to `SbomService` that queries the database to aggregate advisory severity counts for a given SBOM ID. The method joins the `sbom_advisory` table with the `advisory` table, deduplicates by advisory ID, groups by severity, and returns an `AdvisorySeveritySummary`. It also supports an optional severity threshold filter.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `get_advisory_summary(&self, sbom_id: Uuid, threshold: Option<String>, db: &DatabaseConnection) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
- Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` — methods like `fetch` and `list` show the pattern for accepting a database connection reference and returning `Result<T, AppError>`.
- Use SeaORM query builder to join `entity::sbom_advisory` (defined in `entity/src/sbom_advisory.rs`) with `entity::advisory` (defined in `entity/src/advisory.rs`) on advisory ID.
- The `advisory` entity in `entity/src/advisory.rs` has a severity field — use this for grouping counts.
- Deduplicate by advisory ID before counting to avoid inflated counts when an advisory is linked multiple times.
- For the optional `threshold` parameter, filter to only count severities at or above the given level. Severity ordering: Critical > High > Medium > Low.
- Return 404 (via `AppError`) if the SBOM ID does not exist — first check SBOM existence using the existing `sbom` entity in `entity/src/sbom.rs`, consistent with how `modules/fundamental/src/sbom/endpoints/get.rs` handles missing SBOMs.
- Use `common/src/error.rs` `AppError` enum with `.context()` wrapping for error handling.
- Per Key Conventions (Error handling): all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` file scope.
- Per Key Conventions (Framework): Axum for HTTP, SeaORM for database. Applies: convention has no file-type restriction (broadly applicable).

## Reuse Candidates
- `common/src/db/query.rs::query` — Shared query builder helpers for filtering and pagination; may be useful for building the aggregation query
- `common/src/error.rs::AppError` — Standard error type for returning 404 and other errors
- `entity/src/sbom_advisory.rs` — Existing SBOM-Advisory join table entity for the aggregation join
- `entity/src/advisory.rs` — Advisory entity with severity field

## Acceptance Criteria
- [ ] `SbomService::get_advisory_summary` method exists and compiles
- [ ] Method returns correct severity counts by querying `sbom_advisory` joined with `advisory`
- [ ] Advisory IDs are deduplicated before counting
- [ ] Method returns 404 error when SBOM ID does not exist
- [ ] Optional threshold parameter filters to severities at or above the threshold
- [ ] Total field equals the sum of included severity counts

## Test Requirements
- [ ] Unit test with mock database verifying correct aggregation of severity counts across multiple advisories
- [ ] Unit test verifying deduplication when the same advisory is linked to an SBOM multiple times
- [ ] Unit test verifying 404 is returned for a non-existent SBOM ID
- [ ] Unit test verifying threshold filtering returns only counts at or above the specified severity

## Dependencies
- Depends on: Task 1 — Advisory severity model (requires `AdvisorySeveritySummary` struct)


[sdlc-workflow] Description digest: sha256-md:3fb4b737709a6139a16c5115a3adc2b9a42c0679cd4b6e989092eb80fed5ddaf
