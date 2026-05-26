# Task 4 — Update advisory service and endpoints to use status enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the AdvisoryService, advisory models, and advisory endpoints to query the `status` enum column directly on the `advisory` table instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query, reducing p95 latency on the advisory list endpoint by approximately 40ms.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — Remove all joins to `advisory_status` table; update `fetch`, `list`, and `search` methods to read `status` directly from the advisory row; update status filtering to use `WHERE advisory.status = 'Fixed'` pattern instead of joining
- `modules/fundamental/src/advisory/model/summary.rs` — Update `AdvisorySummary` struct to source the `status` field from the advisory entity's enum column instead of from a joined relation
- `modules/fundamental/src/advisory/model/details.rs` — Update `AdvisoryDetails` struct similarly to source `status` from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` — Update any model re-exports or conversion logic related to advisory status
- `modules/fundamental/src/advisory/endpoints/list.rs` — Update the list endpoint handler to filter by the enum column; remove any `advisory_status` table references in query construction
- `modules/fundamental/src/advisory/endpoints/get.rs` — Update the get endpoint handler to read status from the enum column
- `modules/fundamental/src/advisory/endpoints/mod.rs` — Update route registration if status filtering parameters reference the old join
- `common/src/db/query.rs` — If shared query builder helpers contain advisory-status-specific join logic, update them to filter on the enum column instead

## Implementation Notes
- The primary change pattern is removing `.join()` / `.find_also_related(advisory_status::Entity)` calls and replacing them with direct column access on the advisory entity.
- For status filtering in list queries, replace join-based filtering like `.filter(advisory_status::Column::Name.eq(status_filter))` with `.filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed))`.
- The `AdvisorySummary` and `AdvisoryDetails` structs likely construct from query results — update the `From` or builder implementations to extract `status` from `advisory::Model.status` instead of from a joined `advisory_status::Model`.
- The response shape to API consumers must remain identical — `status` is still returned as a string. The `AdvisoryStatusEnum` serializes to string via `serde::Serialize`.
- Check `common/src/db/query.rs` for any shared filtering helpers that build advisory status joins — these need updating too.
- Follow the existing patterns in the `sbom` module (`modules/fundamental/src/sbom/`) as a reference for how service methods query entities without lookup table joins.
- Per constraints doc section 5 (Code Change Rules): inspect all files before modifying; follow existing patterns found in sibling modules.
- Per constraints doc section 2 (Commit Rules): commit message must reference TC-9005 and follow Conventional Commits format.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs` — SbomService demonstrates the project's pattern for querying entities without lookup table joins
- `modules/fundamental/src/sbom/model/summary.rs` — SbomSummary shows how model structs are constructed from entity query results
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting patterns

## Acceptance Criteria
- [ ] All advisory queries use the `status` enum column directly — no joins to `advisory_status` remain
- [ ] Advisory list endpoint correctly filters by status using the enum column
- [ ] Advisory get endpoint returns the status from the enum column
- [ ] `AdvisorySummary` and `AdvisoryDetails` correctly populate the `status` field from the enum
- [ ] API response shape is unchanged — status is still returned as a string value
- [ ] No references to `advisory_status` entity remain in the fundamental module
- [ ] `cargo check -p trustify-module-fundamental` succeeds

## Test Requirements
- [ ] Advisory list endpoint returns correct status values after migration
- [ ] Advisory list endpoint filters by status correctly (e.g., `?status=Fixed` returns only fixed advisories)
- [ ] Advisory get endpoint returns the correct status for a specific advisory
- [ ] Queries execute without joining the `advisory_status` table (verify via query plan or code inspection)

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental` — all existing tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
