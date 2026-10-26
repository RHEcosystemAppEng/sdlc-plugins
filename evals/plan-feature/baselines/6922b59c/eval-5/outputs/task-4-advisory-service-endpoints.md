## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and endpoints to query the `status` enum column directly on the `advisory` table instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query (measured at ~40ms p95 latency increase) and simplifies the query builder logic. All advisory listing, fetching, and searching operations must use the new enum column for status filtering and display.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove the `advisory_status` table join from all query methods (fetch, list, search); replace status filtering with a direct `WHERE advisory.status = <enum_value>` clause; update return type mapping to read status from the enum column
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to populate the `status` field from the enum column instead of the joined lookup table value
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to populate the `status` field from the enum column
- `modules/fundamental/src/advisory/endpoints/list.rs` — update the list endpoint to pass enum-based status filter parameters to the service layer
- `modules/fundamental/src/advisory/endpoints/get.rs` — update the get endpoint to read status from the enum column in the response mapping

## Implementation Notes
The key change in `advisory.rs` (service) is removing the `.join()` call that links `advisory` to `advisory_status`. The current pattern likely uses SeaORM's `JoinType::InnerJoin` or a `Related` trait implementation. Replace this with a direct column read:

```rust
// Before: query.join(JoinType::InnerJoin, advisory::Relation::AdvisoryStatus.def())
// After: no join needed — advisory.status is directly on the model
```

For status filtering in the list endpoint, update the filter to compare against the `AdvisoryStatusEnum` variants directly:

```rust
query.filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed))
```

The `AdvisorySummary` and `AdvisoryDetails` structs should update their `From<advisory::Model>` implementations to read `model.status` (enum) instead of extracting status from a joined row.

Per CONVENTIONS.md §Error Handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping. Ensure any new error paths from enum parsing follow this pattern.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` service file scope.

Per CONVENTIONS.md §Response Types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Ensure the list endpoint response type remains unchanged.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md §Query Helpers: shared filtering, pagination, and sorting via `common/src/db/query.rs`. Reuse existing query builder helpers for status filtering.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` service file scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting that should be reused for status enum filtering
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper used by all list endpoints
- `common/src/error.rs` — `AppError` enum for consistent error handling across all endpoint handlers

## Acceptance Criteria
- [ ] `AdvisoryService::list()` no longer joins the `advisory_status` table
- [ ] `AdvisoryService::fetch()` no longer joins the `advisory_status` table
- [ ] `AdvisoryService::search()` no longer joins the `advisory_status` table (if applicable)
- [ ] Status filtering in the list endpoint uses the `advisory.status` enum column directly
- [ ] `AdvisorySummary` status field is populated from the enum column
- [ ] `AdvisoryDetails` status field is populated from the enum column
- [ ] The advisory list endpoint response shape is unchanged (status is still a string in the JSON response)
- [ ] No references to `advisory_status` table or `status_id` column remain in the advisory module
- [ ] The module compiles without errors (`cargo check -p trustify-module-fundamental`)

## Test Requirements
- [ ] Verify advisory list endpoint returns correct status values from the enum column
- [ ] Verify advisory get endpoint returns correct status from the enum column
- [ ] Verify status filtering works correctly with each enum value (New, Analyzing, Fixed, Rejected)
- [ ] Verify no SQL joins to `advisory_status` are generated in queries (inspect query logs or SQL output)

## Verification Commands
- `cargo check -p trustify-module-fundamental` — module compiles without errors
- `grep -r "advisory_status" modules/fundamental/src/advisory/` — returns no matches

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
