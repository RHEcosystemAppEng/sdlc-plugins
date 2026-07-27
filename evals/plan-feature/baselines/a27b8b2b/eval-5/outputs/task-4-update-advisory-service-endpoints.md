## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer, model structs, and endpoint handlers to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, reducing the advisory list endpoint p95 latency by approximately 40ms. The response shape remains identical — status is still returned as a string to API consumers.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `advisory_status` table joins from fetch, list, and search queries; filter and select using the `status` enum column directly
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source the `status` field from the enum column value rather than the joined lookup table row
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to source the `status` field from the enum column value
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filtering to use `WHERE status = 'Fixed'` pattern instead of join-based filtering
- `modules/fundamental/src/advisory/endpoints/get.rs` — update status retrieval to read from enum column
- `modules/fundamental/src/advisory/mod.rs` — remove any `advisory_status` module imports or re-exports

## Implementation Notes
- The `AdvisoryService` methods (fetch, list, search) in `modules/fundamental/src/advisory/service/advisory.rs` currently join `advisory_status` via `status_id`. Replace these joins with direct column access: `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)`.
- Use SeaORM's enum filtering: `advisory::Column::Status.is_in(vec![AdvisoryStatusEnum::New, AdvisoryStatusEnum::Analyzing])` for multi-value filters.
- The model structs (`AdvisorySummary`, `AdvisoryDetails`) likely convert the joined status row into a string. Update them to convert the enum variant to a string using the derived `ToString`/`Display` implementation or a manual mapping — ensuring the API response shape does not change.
- Follow the existing query builder pattern in `common/src/db/query.rs` for filtering and pagination.
- Follow the existing error handling pattern: all handlers return `Result<T, AppError>` with `.context()` wrapping per project conventions.
- Follow the existing response type pattern: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting; use existing filter infrastructure for enum-based status filtering
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper used by list endpoints; no changes needed but referenced for consistency

## Acceptance Criteria
- [ ] All advisory queries (fetch, list, search) no longer join the `advisory_status` table
- [ ] Advisory list endpoint filters by status using the enum column directly
- [ ] Advisory get endpoint returns status from the enum column
- [ ] `AdvisorySummary` and `AdvisoryDetails` structs correctly serialize the enum status to a string
- [ ] API response shape is unchanged — status field returns the same string values as before
- [ ] No references to `advisory_status` table or `status_id` column remain in the advisory module

## Test Requirements
- [ ] Verify advisory list endpoint returns correct status values for all four enum states
- [ ] Verify advisory list endpoint status filter works correctly with the enum column
- [ ] Verify advisory get endpoint returns the correct status value
- [ ] Verify API response shape has not changed (same JSON structure)

## Verification Commands
- `cargo check -p fundamental` — module compiles without errors
- `grep -r "advisory_status\|status_id" modules/fundamental/src/advisory/` — no remaining references to old schema

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
