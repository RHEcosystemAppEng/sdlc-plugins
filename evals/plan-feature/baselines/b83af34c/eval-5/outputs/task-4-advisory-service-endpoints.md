## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update all advisory service methods, model structs, and endpoint handlers to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead that added ~40ms to advisory list endpoint p95 latency. The response shape remains unchanged — status is still returned as a string.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — Remove `advisory_status` table joins from `fetch`, `list`, and `search` methods; query `advisory.status` directly
- `modules/fundamental/src/advisory/model/summary.rs` — Update `AdvisorySummary` struct to populate `status` field from the enum column instead of the joined table
- `modules/fundamental/src/advisory/model/details.rs` — Update `AdvisoryDetails` struct similarly
- `modules/fundamental/src/advisory/model/mod.rs` — Update model module re-exports if needed
- `modules/fundamental/src/advisory/endpoints/list.rs` — Update list endpoint handler to filter by `advisory.status` enum directly instead of joining
- `modules/fundamental/src/advisory/endpoints/get.rs` — Update get endpoint handler to read status from the enum column

## Implementation Notes
The `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` currently joins `advisory_status` via `status_id`. Replace these joins with direct column access on `advisory.status`. Use the `AdvisoryStatus` enum from the entity crate for type-safe status comparisons.

For filtering in the list endpoint, use SeaORM's `ColumnTrait::eq` with the enum value:
```rust
advisory::Column::Status.eq(AdvisoryStatus::Fixed)
```

The shared query builder helpers in `common/src/db/query.rs` handle pagination and sorting — these should not need modification since the advisory table structure is unchanged from their perspective.

The `PaginatedResults<T>` wrapper in `common/src/model/paginated.rs` is used by list endpoints and remains unchanged.

Per CONVENTIONS.md §Error Handling: maintain `Result<T, AppError>` with `.context()` wrapping in all modified handlers. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Module Pattern: preserve the `model/ + service/ + endpoints/` structure in the advisory module. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md §Response Types: list endpoints must continue returning `PaginatedResults<T>`. Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's endpoint `.rs` file scope.

## Acceptance Criteria
- [ ] All advisory queries use `advisory.status` column directly — no joins to `advisory_status`
- [ ] `AdvisorySummary` and `AdvisoryDetails` populate status from the enum column
- [ ] List endpoint supports filtering by status using the enum column
- [ ] GET endpoint returns status from the enum column
- [ ] Response shape is unchanged — status is still returned as a string in the API response
- [ ] No references to `advisory_status` table remain in the advisory module

## Test Requirements
- [ ] Integration test: GET /api/v2/advisory returns advisory with correct status string
- [ ] Integration test: GET /api/v2/advisory with status filter returns correctly filtered results
- [ ] Integration test: GET /api/v2/advisory/{id} returns advisory details with correct status
- [ ] Verify no performance regression — status queries should be faster without the join

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
