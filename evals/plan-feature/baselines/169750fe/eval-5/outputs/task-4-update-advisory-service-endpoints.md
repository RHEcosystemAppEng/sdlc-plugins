## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer, model structs, and endpoint handlers to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead that was adding ~40ms to p95 latency on the advisory list endpoint.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove `advisory_status` table joins from all advisory queries; update filtering logic to use `advisory.status` column directly with enum comparison
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source `status` from the enum column instead of the joined table
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to source `status` from the enum column
- `modules/fundamental/src/advisory/endpoints/list.rs` — update list handler to pass status filter as enum value; remove join-based filtering
- `modules/fundamental/src/advisory/endpoints/get.rs` — update get handler to read status from enum column
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if query parameter types change for status filtering

## Implementation Notes
In `advisory.rs` (service), locate all query builder calls that join `advisory_status` (e.g., `.join(JoinType::InnerJoin, advisory::Relation::AdvisoryStatus.def())`). Remove these joins and replace status field selection with direct column access on the `advisory` table.

For status filtering in the list endpoint, update the filter to compare against the enum directly:
```rust
.filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed))
```
instead of the current join-based approach.

The `AdvisorySummary` and `AdvisoryDetails` structs should read the `status` field directly from the advisory entity model — no separate status struct or join result needed.

Use the shared query builder helpers from `common/src/db/query.rs` for pagination and sorting — these remain unchanged.

Per CONVENTIONS.md §Error handling: maintain `Result<T, AppError>` with `.context()` wrapping in all service and handler methods.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust handler scope.

Per CONVENTIONS.md §Response types: list endpoints must continue returning `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's Rust endpoint scope.

Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust query scope.

## Reuse Candidates
- `common/src/db/query.rs::QueryBuilder` — shared query builder helpers for filtering, pagination, and sorting; continue using these for advisory queries
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper for list endpoints; no changes needed
- `common/src/error.rs::AppError` — error type for handler returns; continue using with `.context()`

## Acceptance Criteria
- [ ] All advisory queries in `AdvisoryService` use the `status` enum column directly — no joins to `advisory_status`
- [ ] `AdvisorySummary` and `AdvisoryDetails` structs read `status` from the advisory entity model
- [ ] List endpoint supports status filtering via enum comparison
- [ ] Get endpoint returns status from enum column
- [ ] No references to `advisory_status` table or entity remain in the advisory module
- [ ] Response shape is unchanged — status is still returned as a string to API consumers

## Test Requirements
- [ ] Advisory list endpoint returns correct results with status filter
- [ ] Advisory get endpoint returns correct status value
- [ ] Status filtering works for all four enum values (New, Analyzing, Fixed, Rejected)
- [ ] Pagination and sorting continue to work correctly

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update entity definitions (service layer depends on updated entity types)
