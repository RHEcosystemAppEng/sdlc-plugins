# Task 4 — Update advisory service, endpoints, and ingestion pipeline to use enum status

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update all advisory-related service logic, endpoint handlers, and the ingestion pipeline to use the new `status` enum column instead of the `status_id` foreign key join to `advisory_status`. This eliminates the join from all advisory queries, simplifies status filtering, and updates the ingestion pipeline to write enum values directly. The response shape remains unchanged — status is still returned as a string to API consumers.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — Remove all joins to `advisory_status` table; update list/fetch/search queries to filter and sort by `advisory.status` enum column directly
- `modules/fundamental/src/advisory/model/summary.rs` — Update `AdvisorySummary` struct to source status from the enum field instead of a joined relation
- `modules/fundamental/src/advisory/model/details.rs` — Update `AdvisoryDetails` struct similarly to use the enum field
- `modules/fundamental/src/advisory/model/mod.rs` — Update module-level type re-exports if they reference `advisory_status`
- `modules/fundamental/src/advisory/endpoints/list.rs` — Update status filter handling in the list endpoint to use enum comparison (`WHERE status = 'Fixed'`) instead of join-based filtering
- `modules/fundamental/src/advisory/endpoints/get.rs` — Update get endpoint if it includes status in the response via a join
- `modules/ingestor/src/graph/advisory/mod.rs` — Update advisory ingestion to write `AdvisoryStatusEnum` values directly to the `status` column instead of inserting into the lookup table and referencing via FK
- `common/src/db/query.rs` — Update shared query helpers if they contain advisory-status-specific join logic or filtering helpers

## Implementation Notes
- In `advisory.rs` service, replace all `advisory_status` joins with direct column access. For example, replace patterns like `.join(JoinType::LeftJoin, advisory::Relation::AdvisoryStatus.def())` with direct `.filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed))`.
- In the model structs (`summary.rs`, `details.rs`), the `status` field should be typed as `String` in the API response (serializing the enum to its string representation) to maintain backward compatibility with consumers.
- In `query.rs`, check for any shared filtering helpers that operate on the `advisory_status` table. Update or remove these to use the enum column.
- In the ingestion pipeline (`modules/ingestor/src/graph/advisory/mod.rs`), replace the two-step process (insert status row, then reference FK) with a single-step process: map the incoming status string to `AdvisoryStatusEnum` and set it directly on the advisory `ActiveModel`.
- Follow the existing error handling pattern: all handlers return `Result<T, AppError>` with `.context()` wrapping per `common/src/error.rs`.
- Follow the existing response pattern: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Use `common/src/db/query.rs` for filtering and pagination helpers.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting that should be reused for the updated advisory queries
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper used by all list endpoints
- `common/src/error.rs` — `AppError` enum for consistent error handling
- `modules/fundamental/src/sbom/service/sbom.rs` — Reference implementation of a service without status table joins, showing the direct-column query pattern to follow

## Acceptance Criteria
- [ ] All advisory queries no longer join the `advisory_status` table
- [ ] Advisory list endpoint supports filtering by status using the enum column directly
- [ ] Advisory list and detail endpoints return the same response shape as before (status as a string)
- [ ] Advisory ingestion pipeline writes enum values directly to `advisory.status`
- [ ] No references to `advisory_status` table or `status_id` column remain in service, endpoint, or ingestion code
- [ ] The application compiles and starts successfully with the updated code

## Test Requirements
- [ ] Verify advisory list endpoint returns correct results when filtering by status
- [ ] Verify advisory detail endpoint returns the status field as a string
- [ ] Verify advisory ingestion correctly writes enum status values
- [ ] Verify list endpoint pagination still works correctly with enum-based filtering
- [ ] Verify error handling when an invalid status filter value is provided

## Verification Commands
- `cargo check` — full project compiles without errors
- `cargo clippy` — no new warnings introduced

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
