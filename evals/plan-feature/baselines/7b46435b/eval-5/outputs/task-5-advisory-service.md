# Task 5 — Update advisory service to eliminate status table join

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the `AdvisoryService` to remove all joins with the `advisory_status` table from advisory queries. Replace status filtering and retrieval with direct queries against the `advisory.status` enum column. This eliminates the join overhead that added ~40ms to the advisory list endpoint's p95 latency.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove `advisory_status` table join from `fetch`, `list`, and `search` methods; update status filter predicates to use `WHERE advisory.status = <enum_value>` via SeaORM column filtering

## Implementation Notes
- The `list` method likely builds a query joining `advisory_status` via the `status_id` FK — remove this join and filter directly using SeaORM: `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)`
- The `fetch` method (single advisory lookup) also joins `advisory_status` for the status value — simplify to direct column access from the advisory entity
- Use the shared query helpers in `common/src/db/query.rs` for filtering, pagination, and sorting — the status column may need to be registered as a filterable field in the query builder
- Error handling: maintain the `Result<T, AppError>` return type with `.context()` wrapping per project convention
- Response types: list operations should continue to return `PaginatedResults<AdvisorySummary>` via `common/src/model/paginated.rs`
- Verify that `search` method in the `AdvisoryService` also removes any `advisory_status` join if it performs status-based filtering

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; verify status filter integration with enum values
- `modules/fundamental/src/sbom/service/sbom.rs` — reference service pattern for query construction without lookup table joins
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper used by list operations

## Acceptance Criteria
- [ ] No advisory queries join the `advisory_status` table
- [ ] Status filtering uses direct `WHERE advisory.status = <value>` predicates on the enum column
- [ ] All `AdvisoryService` methods (`fetch`, `list`, `search`) work correctly with the enum column
- [ ] Query performance improves — status filtering no longer requires a join

## Test Requirements
- [ ] Verify service methods compile and pass existing tests: `cargo test -p fundamental`
- [ ] Verify list queries with status filter return correct results using enum values
- [ ] Verify fetch queries return advisory with correct status from enum column

## Verification Commands
- `cargo check -p fundamental` — fundamental module compiles
- `cargo test -p fundamental` — fundamental module tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory model structs for direct enum status
