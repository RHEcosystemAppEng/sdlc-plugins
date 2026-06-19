## Repository
trustify-backend

## Target Branch
main

## Description
Add an `advisory_severity_summary` method to `SbomService` that queries the database to aggregate advisory severity counts for a given SBOM. The method queries the `sbom_advisory` join table joined with the `advisory` table, deduplicates by advisory ID, groups by severity, and returns an `AdvisorySeveritySummary`. It also supports an optional severity threshold filter for the alerting use case.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `async fn advisory_severity_summary(&self, sbom_id: Uuid, threshold: Option<String>) -> Result<AdvisorySeveritySummary, AppError>` method to `SbomService`

## Implementation Notes
Follow the existing query patterns in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService` methods like fetch and list) for database access style, connection pool usage, and error handling.

Use `entity/src/sbom_advisory.rs` (SBOM-Advisory join entity) and `entity/src/advisory.rs` (Advisory entity with severity field) for the SeaORM query. The query should:
1. Filter `sbom_advisory` by the given `sbom_id`
2. Join with `advisory` to access the severity field
3. Select distinct advisory IDs to deduplicate
4. Group by severity and count
5. If `threshold` is provided, filter to only severities at or above the threshold level

Use `common/src/db/query.rs` helpers for query building where applicable.

Return 404 via `AppError` if the SBOM ID does not exist, consistent with the pattern in `modules/fundamental/src/sbom/endpoints/get.rs`.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping on all fallible operations.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` Rust scope.

Per CONVENTIONS.md §Query helpers: use shared filtering via `common/src/db/query.rs` for threshold filtering logic.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` Rust scope.

Per CONVENTIONS.md §Framework: use SeaORM for database queries.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` Rust scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service with database access patterns; add the new method here
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — Error type for 404 and internal error responses
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join entity for the aggregation query
- `entity/src/advisory.rs` — Advisory entity with severity field

## Acceptance Criteria
- [ ] `SbomService::advisory_severity_summary` method exists and compiles
- [ ] Method returns correct severity counts aggregated from the `sbom_advisory` + `advisory` tables
- [ ] Advisory deduplication by advisory ID is implemented (no double-counting)
- [ ] Method returns 404 `AppError` when the SBOM ID does not exist
- [ ] Optional `threshold` parameter filters counts to only severities at or above the given level
- [ ] All database errors are wrapped with `.context()` for meaningful error messages

## Test Requirements
- [ ] Unit test for threshold filtering logic (critical-only, high-and-above, etc.)
- [ ] Unit test verifying deduplication logic (same advisory linked multiple times counts once)

## Dependencies
- Depends on: Task 1 — Advisory summary model (requires `AdvisorySeveritySummary` struct)
