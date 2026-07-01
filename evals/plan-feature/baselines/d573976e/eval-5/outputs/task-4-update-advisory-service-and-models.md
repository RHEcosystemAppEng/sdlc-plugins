## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory model structs (`AdvisorySummary`, `AdvisoryDetails`) and the `AdvisoryService` to use the new `AdvisoryStatusEnum` column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead that added ~40ms to the advisory list endpoint p95 latency and simplifies all advisory query code.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` — change the status field from a joined string/ID to `AdvisoryStatusEnum`; update any `From` or conversion impls that previously resolved status via the join
- `modules/fundamental/src/advisory/model/details.rs` — same change: replace status ID or joined status name with the enum field
- `modules/fundamental/src/advisory/model/mod.rs` — update re-exports and any type aliases for the status type
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all JOINs to `advisory_status` table from fetch, list, and search query methods; read `status` directly from the `advisory` entity column; update status filter logic to use `advisory_status_enum` values instead of integer IDs
- `modules/fundamental/src/advisory/service/mod.rs` — update imports to reference `AdvisoryStatusEnum` from the entity crate

## Implementation Notes
- In `AdvisoryService`, look for `.join()` or `.find_also_related()` calls that reference `advisory_status::Entity` and remove them
- Replace status filter conditions like `.filter(advisory_status::Column::Name.eq(status_name))` with `.filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed))` (or whichever enum variant)
- The `AdvisorySummary` struct likely has a field like `pub status: String` populated from the join — change it to `pub status: AdvisoryStatusEnum` and rely on serde's `Serialize` derive to produce the same string output
- For `AdvisoryDetails`, apply the same pattern — the status field should be the enum directly
- Follow the existing service query patterns in `modules/fundamental/src/advisory/service/advisory.rs` — examine how `sbom` service queries are structured in `modules/fundamental/src/sbom/service/sbom.rs` for the standard non-join query pattern
- Use `common/src/db/query.rs` helpers for filtering and pagination — verify that `query.rs` filtering works with enum column types

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs` — reference for SeaORM query patterns without lookup table joins (fetch, list operations)
- `modules/fundamental/src/sbom/model/summary.rs` — reference for model struct pattern with direct column mapping
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting that the advisory service already uses

## Acceptance Criteria
- [ ] `AdvisorySummary` has a `status` field of type `AdvisoryStatusEnum` (not a joined string or integer)
- [ ] `AdvisoryDetails` has a `status` field of type `AdvisoryStatusEnum`
- [ ] No code in the advisory service module references `advisory_status` entity or table
- [ ] Advisory list query does not JOIN any status lookup table
- [ ] Advisory fetch-by-ID query does not JOIN any status lookup table
- [ ] Status filtering works with enum string values (e.g., `?status=Fixed`)
- [ ] API response shape for advisory endpoints remains identical (status is still a string in JSON output)

## Test Requirements
- [ ] Unit test or integration test for advisory list with status filter — verify filtering by each enum value (New, Analyzing, Fixed, Rejected) returns correct results
- [ ] Verify advisory detail endpoint returns status as a string in JSON response (backward compatibility)
- [ ] Verify advisory list endpoint returns correct `PaginatedResults<AdvisorySummary>` with enum-based status

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions
