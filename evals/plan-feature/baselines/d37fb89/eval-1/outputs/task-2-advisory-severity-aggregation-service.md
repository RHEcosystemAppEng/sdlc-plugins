## Repository
trustify-backend

## Target Branch
main

## Description
Add a service method `advisory_severity_summary` to `SbomService` that queries the database to compute severity counts for advisories linked to a given SBOM. The method joins the `sbom_advisory` join table with the `advisory` table, groups by severity, deduplicates by advisory ID, and returns an `AdvisorySeveritySummary`. It also validates that the SBOM exists, returning an appropriate error if not found. An optional severity threshold filter restricts which severity levels are counted.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `pub async fn advisory_severity_summary(&self, sbom_id: Uuid, threshold: Option<SeverityThreshold>) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Files to Create
- `modules/fundamental/src/sbom/service/advisory_summary.rs` — If the service file is too large, extract the aggregation logic into a dedicated file (optional; the method can also be added directly to `sbom.rs`)

## Implementation Notes
The query should use SeaORM's query builder to:
1. Start from the `sbom_advisory` entity (`entity/src/sbom_advisory.rs`) filtered by `sbom_id`
2. Join to the `advisory` entity (`entity/src/advisory.rs`) to access the `severity` field
3. Use `SELECT DISTINCT advisory_id` or `GROUP BY advisory_id` to deduplicate advisories (an advisory may be linked to an SBOM via multiple paths)
4. Group by severity and count distinct advisory IDs
5. If `threshold` is provided, add a WHERE clause filtering to severities at or above the threshold level

Reference `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) for the existing service pattern: methods take `&self` with a database connection from the service's connection pool, use `.context()` for error wrapping, and return `Result<T, AppError>`.

Reference `common/src/db/query.rs` for shared query builder helpers — check if any existing filtering or aggregation utilities can be reused rather than writing raw SQL.

Reference `common/src/error.rs` (`AppError`) for the error enum — it likely has a `NotFound` variant or similar for 404 responses.

For the SBOM existence check, query the SBOM entity first. If not found, return `AppError::NotFound` (or equivalent) to produce an HTTP 404 — consistent with existing patterns in `modules/fundamental/src/sbom/endpoints/get.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service methods demonstrate connection handling, error wrapping, and query patterns
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error type with `NotFound` variant for 404 responses
- `entity/src/sbom_advisory.rs` — join table entity needed for the aggregation query
- `entity/src/advisory.rs` — advisory entity with `severity` field for grouping

## Acceptance Criteria
- [ ] `SbomService::advisory_severity_summary()` method exists and compiles
- [ ] Method returns correct severity counts when given a valid SBOM ID with linked advisories
- [ ] Method deduplicates advisories by advisory ID before counting
- [ ] Method returns `AppError::NotFound` (404) when SBOM ID does not exist
- [ ] Method supports optional `threshold` parameter that filters severity levels
- [ ] Method returns zero counts for severity levels with no matching advisories

## Test Requirements
- [ ] Unit test: correct aggregation with multiple advisories at different severity levels
- [ ] Unit test: deduplication — same advisory linked via multiple paths counts only once
- [ ] Unit test: SBOM not found returns appropriate error
- [ ] Unit test: threshold filter returns only counts at or above the threshold

## Dependencies
- Depends on: Task 1 — Advisory severity summary model (needs `AdvisorySeveritySummary` struct)

[sdlc-workflow] Description digest: sha256-md:73428423545bcfb6638820c0af178f7bb8c70c9119bff758e40bea03b13b9237
