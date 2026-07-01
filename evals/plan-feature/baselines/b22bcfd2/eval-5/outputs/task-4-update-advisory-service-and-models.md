## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and model structs to use the new `status` enum column instead of joining the `advisory_status` table. This eliminates the join overhead from all advisory queries and simplifies the query logic.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `advisory_status` table joins from `fetch`, `list`, and `search` methods; query `advisory.status` directly; update filtering logic to compare against `AdvisoryStatusEnum` values
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source `status` from the enum column instead of the joined table; change the field type from `String` to `AdvisoryStatusEnum` (or keep as `String` with `.to_string()` conversion for API compatibility)
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct similarly to use the enum column for status
- `modules/fundamental/src/advisory/model/mod.rs` — update any re-exports or shared model logic related to status

## Implementation Notes
In `modules/fundamental/src/advisory/service/advisory.rs`:
- The current `list` and `fetch` methods join `advisory_status` via `advisory::Relation::AdvisoryStatus`. Remove these joins.
- Replace `.filter(advisory_status::Column::Name.eq(status_filter))` with `.filter(advisory::Column::Status.eq(AdvisoryStatusEnum::from_str(status_filter)))`.
- Use `common/src/db/query.rs` query builder helpers for filtering and pagination — these are shared across modules and should continue to be used.

In `modules/fundamental/src/advisory/model/summary.rs`:
- The `AdvisorySummary` struct has a `status` or `severity` field populated from the join. Update it to read from `advisory::Column::Status` directly.
- Ensure the API response still returns status as a string (use `.to_string()` on the enum if needed) so there are no user-facing API changes.

## Acceptance Criteria
- [ ] All advisory queries no longer join the `advisory_status` table
- [ ] Status filtering works against the `advisory.status` enum column
- [ ] `AdvisorySummary` and `AdvisoryDetails` correctly populate status from the enum column
- [ ] API response shape is unchanged — status is still returned as a string
- [ ] No references to `advisory_status` entity remain in the advisory service or model code

## Test Requirements
- [ ] Advisory list endpoint returns correct status values from enum column
- [ ] Advisory list with status filter correctly filters by enum value
- [ ] Advisory detail endpoint returns correct status from enum column
- [ ] Service methods compile and pass unit tests with the updated entity

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005
- Depends on: Task 3 — Update entity definitions
