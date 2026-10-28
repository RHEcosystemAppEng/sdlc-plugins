## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to query the `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query and simplifies the filtering logic. The user-facing API response shape remains unchanged -- status continues to be returned as a string.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` -- remove `advisory_status` table join from all query methods; filter on `advisory.status` enum column directly
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` struct to source status from the enum column instead of the join result
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` struct to source status from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` -- update any model re-exports or shared status type references
- `modules/fundamental/src/advisory/endpoints/list.rs` -- update status filter parameter handling to compare against enum values
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update status extraction if applicable

## Implementation Notes
- In `AdvisoryService` (advisory.rs), replace all `.join(advisory_status::Entity)` calls with direct column access on `advisory::Column::Status`.
- Status filtering in list queries should use `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` instead of joining and filtering on the lookup table.
- The `AdvisorySummary` and `AdvisoryDetails` structs should derive the status field directly from the `advisory::Model` without a separate join query.
- Ensure the API response serializes the enum variant as a string (e.g., `"Fixed"`) to maintain backward compatibility with existing API consumers.
- Use the shared query helpers from `common/src/db/query.rs` for pagination and sorting -- these should not need changes since the query structure simplifies.

Per CONVENTIONS.md §Error Handling: maintain `Result<T, AppError>` with `.context()` wrapping on all service methods.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Response Types: continue using `PaginatedResults<AdvisorySummary>` for the list endpoint.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` response wrapper used by list endpoints
- `common/src/error.rs` -- `AppError` enum for error handling
- `modules/fundamental/src/sbom/service/sbom.rs` -- sibling service showing query patterns without lookup table joins

## Acceptance Criteria
- [ ] `AdvisoryService` no longer joins the `advisory_status` table in any query
- [ ] Advisory list endpoint (`GET /api/v2/advisory`) filters by enum column directly
- [ ] Advisory get endpoint (`GET /api/v2/advisory/{id}`) returns status from enum column
- [ ] `AdvisorySummary` and `AdvisoryDetails` source status from the enum field, not a join
- [ ] API response shape is unchanged -- status is serialized as a string
- [ ] All advisory service methods compile and handle errors with `.context()`

## Test Requirements
- [ ] Advisory list query returns correct results when filtering by status
- [ ] Advisory detail query returns the correct status string
- [ ] Status enum values serialize correctly in JSON responses (e.g., `"Fixed"`, not `"fixed"` or `0`)
- [ ] Pagination continues to work correctly on the simplified query

## Verification Commands
- `cargo check -p fundamental` -- fundamental module compiles without errors
- `cargo test -p fundamental` -- fundamental module tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
