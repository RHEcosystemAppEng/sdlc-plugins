# Task 4 — Update advisory service and endpoints to use enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to query the `advisory.status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead that was adding ~40ms to the advisory list endpoint p95 latency. All advisory queries must be updated to filter and read status from the enum column.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all joins to `advisory_status` table; update queries to filter/select by `advisory.status` enum column directly; update `AdvisoryService::fetch`, `list`, and `search` methods
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source the `status` field from the enum column instead of from a joined table
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to source the `status` field from the enum column
- `modules/fundamental/src/advisory/endpoints/list.rs` — update the list endpoint to filter by `advisory.status` enum column (e.g., `WHERE status = 'Fixed'`) without join
- `modules/fundamental/src/advisory/endpoints/get.rs` — update the get endpoint to read status from enum column
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if query parameter types change for status filtering
- `modules/fundamental/src/advisory/mod.rs` — remove re-exports of advisory_status-related types if any

## Implementation Notes
- The advisory list endpoint currently joins `advisory_status` for filtering (e.g., `WHERE advisory_status.name = 'Fixed'`). Replace this with a direct enum comparison: `WHERE advisory.status = 'Fixed'`
- For SeaORM query building, use `Column::Status.eq(AdvisoryStatusEnum::Fixed)` instead of building a join condition
- Remove any `Relation::AdvisoryStatus` usage from query builders in the service layer
- The response shape for API consumers remains identical — status is still returned as a string. The change is internal to the query layer
- Check `common/src/db/query.rs` for any shared query helpers that reference the `advisory_status` join and update them if found
- Follow the existing `Result<T, AppError>` error handling pattern with `.context()` wrapping
- Follow the `PaginatedResults<T>` response pattern from `common/src/model/paginated.rs` for list endpoints
- Per docs/constraints.md §5.2: inspect each file before modifying to understand current query patterns
- Per docs/constraints.md §5.4: reuse existing query builder helpers from `common/src/db/query.rs`

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting — reuse these patterns for the updated enum-based queries
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper used by list endpoints
- `common/src/error.rs` — `AppError` enum for error handling patterns
- `modules/fundamental/src/sbom/service/sbom.rs` — reference implementation of a service that queries without status joins (pattern to follow)

## Acceptance Criteria
- [ ] All advisory queries use `advisory.status` enum column directly — no joins to `advisory_status`
- [ ] Advisory list endpoint supports filtering by status using enum column
- [ ] Advisory get endpoint returns status from enum column
- [ ] `AdvisorySummary` and `AdvisoryDetails` structs source status from enum column
- [ ] No references to `advisory_status` table remain in the advisory module
- [ ] API response shape is unchanged (status is still returned as a string)
- [ ] All advisory endpoints compile and function correctly

## Test Requirements
- [ ] Advisory list endpoint returns correct results when filtering by status
- [ ] Advisory get endpoint returns correct status value
- [ ] Advisory list without status filter returns all advisories with correct statuses
- [ ] Verify no regressions in advisory endpoint response format

## Verification Commands
- `cargo check -p fundamental` — module compiles successfully
- `cargo test -p fundamental` — existing tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
