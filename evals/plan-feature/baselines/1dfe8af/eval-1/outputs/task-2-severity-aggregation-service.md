## Repository
trustify-backend

## Target Branch
main

## Description
Add a service method to `SbomService` that queries the `sbom_advisory` join table to aggregate advisory severity counts for a given SBOM ID. This method performs the database query that powers the new advisory-summary endpoint, counting unique advisories grouped by severity level using SeaORM query builders.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `get_advisory_severity_summary(&self, sbom_id: Uuid) -> Result<AdvisorySeveritySummary, AppError>` method to SbomService

## Implementation Notes
Add the aggregation method to the existing `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`. Follow the query patterns used by existing service methods (fetch, list, ingest) in the same file.

The query should:
1. Join `sbom_advisory` with `advisory` to access the severity field
2. Filter by the given SBOM ID
3. Group by severity and count distinct advisory IDs to deduplicate
4. Map the grouped counts into `AdvisorySeveritySummary` fields

Use the shared query builder helpers from `common/src/db/query.rs` for any filtering logic. Use `entity/src/sbom_advisory.rs` for the join table entity and `entity/src/advisory.rs` for the advisory entity (which contains the severity column).

Return `AppError::NotFound` (from `common/src/error.rs`) if the SBOM ID does not exist in the database. Verify SBOM existence before running the aggregation query, consistent with how `GET /api/v2/sbom/{id}` works in `modules/fundamental/src/sbom/endpoints/get.rs`.

Per CONVENTIONS.md §Error Handling: use Result<T, AppError> with .context() wrapping.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Extend this existing service; follow fetch/list method patterns for database access and error handling
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — Use AppError::NotFound for missing SBOM, AppError::Internal for query failures
- `entity/src/sbom_advisory.rs` — SeaORM entity for the SBOM-Advisory join table; use for the join query
- `entity/src/advisory.rs` — Advisory entity containing the severity field to group by

## Acceptance Criteria
- [ ] `SbomService::get_advisory_severity_summary` method exists and returns `Result<AdvisorySeveritySummary, AppError>`
- [ ] Method counts unique advisories per severity level (deduplicated by advisory ID)
- [ ] Method returns AppError::NotFound when SBOM ID does not exist
- [ ] Method correctly maps severity values to critical/high/medium/low counts
- [ ] Total field equals sum of critical + high + medium + low

## Test Requirements
- [ ] Unit test verifying correct severity counts for a known SBOM with mixed severity advisories
- [ ] Unit test verifying NotFound error when SBOM ID does not exist
- [ ] Unit test verifying deduplication: same advisory linked twice does not double-count

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental sbom::service` — service tests pass

## Dependencies
- Depends on: Task 1 — Advisory severity summary model

[sdlc-workflow] Description digest: sha256-md:b5d8e0a2c4f6179684f20b5d6e9a3c7f8b01d2e4f6a8190b2c4d6e8f0a1b3c5
