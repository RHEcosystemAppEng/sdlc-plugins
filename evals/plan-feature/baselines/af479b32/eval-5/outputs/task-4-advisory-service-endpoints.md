# Task 4: Update advisory service layer and endpoints to use status enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update all advisory queries in the service layer and endpoint handlers to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead that added ~40ms to the advisory list endpoint p95 latency. The API response shape remains identical -- status is still returned as a string to consumers.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` -- remove all `.join()` or `.find_also_related()` calls to `advisory_status`; query `advisory.status` column directly; update status filtering to use `WHERE status = 'value'` instead of a join condition
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` struct to source the status field from the advisory entity's enum field instead of a joined relation
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` struct similarly to use the enum field
- `modules/fundamental/src/advisory/model/mod.rs` -- update any model re-exports or shared status mapping logic
- `modules/fundamental/src/advisory/endpoints/list.rs` -- update status filter parameter handling to compare against enum values directly
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update status access in the single-advisory response
- `common/src/db/query.rs` -- update advisory status filtering helpers if status filtering is implemented in the shared query module

## Implementation Notes
- The key change in the service layer is removing the join. Before: `Advisory::find().find_also_related(AdvisoryStatus)` with a map to extract the status label. After: `Advisory::find()` with the status available directly as `model.status`.
- For status filtering in list endpoints, replace the join-based filter with a direct column filter: `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` instead of filtering through the joined table.
- The `AdvisorySummary` and `AdvisoryDetails` structs likely have a `status: String` field that was populated by mapping the joined `advisory_status.label` value. Now populate it by converting the `AdvisoryStatusEnum` variant to a string (e.g., `model.status.to_string()` or a match expression).
- Per CONVENTIONS.md: all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's endpoint handler scope.
- Per CONVENTIONS.md: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's list endpoint scope.
- Per CONVENTIONS.md: shared filtering, pagination, and sorting via `common/src/db/query.rs`.
  Applies: task modifies `common/src/db/query.rs` matching the convention's query helper scope.
- Reference the SBOM service implementation (`modules/fundamental/src/sbom/service/sbom.rs`) for the pattern of querying entities without joins.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs` -- existing service demonstrating entity queries without lookup table joins; use as a pattern for the simplified advisory queries
- `modules/fundamental/src/sbom/endpoints/list.rs` -- existing list endpoint showing filter parameter handling and `PaginatedResults` usage without joins
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting that may already support enum column filtering

## Acceptance Criteria
- [ ] No advisory query joins the `advisory_status` table
- [ ] Advisory list endpoint (`GET /api/v2/advisory`) returns correct status values using the enum column
- [ ] Advisory list endpoint supports filtering by status (e.g., `?status=Fixed`) using the enum column directly
- [ ] Advisory detail endpoint (`GET /api/v2/advisory/{id}`) returns the correct status string
- [ ] API response shape is unchanged -- status is still returned as a string in `AdvisorySummary` and `AdvisoryDetails`
- [ ] All endpoint handlers compile and return `Result<T, AppError>`

## Test Requirements
- [ ] Verify the advisory list endpoint returns advisories with correct status values
- [ ] Verify the advisory list endpoint filters by status correctly (each of the four enum values)
- [ ] Verify the advisory detail endpoint returns the correct status for a specific advisory
- [ ] Verify that no SQL queries reference the `advisory_status` table (check query logs or generated SQL)

## Verification Commands
- `cargo check -p fundamental` -- fundamental module compiles without errors
- `cargo test -p fundamental -- advisory` -- advisory-related unit tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
