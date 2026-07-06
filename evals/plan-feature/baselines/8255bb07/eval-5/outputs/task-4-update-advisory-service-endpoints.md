## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer, model structs, and endpoint handlers to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, reducing advisory list endpoint p95 latency by approximately 40ms.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` -- Remove the `advisory_status` join from fetch, list, and search queries; filter by `advisory.status` enum column directly
- `modules/fundamental/src/advisory/model/summary.rs` -- Update `AdvisorySummary` struct to source status from the enum column instead of the joined table
- `modules/fundamental/src/advisory/model/details.rs` -- Update `AdvisoryDetails` struct to source status from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` -- Update model module exports if needed
- `modules/fundamental/src/advisory/endpoints/list.rs` -- Update list handler to use enum-based status filtering
- `modules/fundamental/src/advisory/endpoints/get.rs` -- Update get handler to use the new status field

## Implementation Notes
- In `advisory.rs` service, replace all `advisory_status` table joins with direct column access on `advisory::Column::Status`
- Update query filters that previously used `advisory_status::Column::Status` to use `advisory::Column::Status` with the `AdvisoryStatusEnum` type
- The `AdvisorySummary` and `AdvisoryDetails` structs should have their status field type changed from a joined lookup to `AdvisoryStatusEnum` from the entity crate. The response serialization must remain a string value to maintain API backward compatibility.
- Use the `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs` for list endpoint responses (unchanged pattern, but verify status field serialization)
- Use the shared query helpers from `common/src/db/query.rs` for filtering and pagination (verify status filter integration)
- All handlers must continue returning `Result<T, AppError>` with `.context()` for error wrapping

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust handler file scope.

Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>`.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's Rust endpoint file scope.

Per CONVENTIONS.md §Query helpers: use shared filtering and pagination via `common/src/db/query.rs`.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust service file scope.

## Reuse Candidates
- `common/src/db/query.rs` -- Shared query builder helpers for filtering, pagination, and sorting; use for enum-based status filtering
- `common/src/model/paginated.rs` -- PaginatedResults<T> response wrapper; continue using for list endpoint
- `common/src/error.rs` -- AppError enum with IntoResponse; continue using for error handling

## Acceptance Criteria
- [ ] All advisory queries use the `status` enum column directly (no join to `advisory_status`)
- [ ] The advisory list endpoint (`GET /api/v2/advisory`) returns correctly with status filtering
- [ ] The advisory detail endpoint (`GET /api/v2/advisory/{id}`) returns status as a string value
- [ ] API response shape is unchanged (status field remains a string in JSON output)
- [ ] No references to `advisory_status` table remain in the advisory module
- [ ] Error handling follows the `Result<T, AppError>` pattern with `.context()` wrapping

## Test Requirements
- [ ] Verify the advisory list endpoint returns advisories with correct status values
- [ ] Verify status filtering works with each enum value (New, Analyzing, Fixed, Rejected)
- [ ] Verify the advisory detail endpoint returns the correct status
- [ ] Verify the API response shape has not changed (backward compatibility)
- [ ] Verify error cases return appropriate AppError responses

## Verification Commands
- `cargo check -p fundamental` -- module compiles successfully
- `cargo test -p fundamental` -- unit tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
