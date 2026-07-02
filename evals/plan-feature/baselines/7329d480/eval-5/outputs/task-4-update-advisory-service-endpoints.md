# Task 4: Update advisory service, model, and endpoints to use status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory module's model structs, service layer, and HTTP endpoints to use the new `AdvisoryStatusEnum` column instead of joining the `advisory_status` lookup table. This eliminates the status join from all advisory queries, simplifying the query logic and reducing latency on the advisory list endpoint.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` — change `AdvisorySummary` struct to read `status` as an enum string instead of joining `advisory_status`
- `modules/fundamental/src/advisory/model/details.rs` — change `AdvisoryDetails` struct to read `status` as an enum string instead of joining `advisory_status`
- `modules/fundamental/src/advisory/model/mod.rs` — update module-level re-exports if status-related types change
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `advisory_status` table joins from `fetch`, `list`, and `search` queries; filter by `advisory::Column::Status` directly
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter parameter handling to compare against enum values instead of joined table
- `modules/fundamental/src/advisory/endpoints/get.rs` — update advisory fetch to use direct column access instead of join

## Implementation Notes
- In `modules/fundamental/src/advisory/service/advisory.rs`, remove all `.join(advisory_status::Entity)` calls and replace `advisory_status::Column::Name` references with `advisory::Column::Status`.
- For status filtering in the list endpoint, convert the query parameter string to `AdvisoryStatusEnum` and use `.filter(advisory::Column::Status.eq(status_enum_value))`.
- Update `AdvisorySummary` and `AdvisoryDetails` construction to read `status` directly from the advisory model instead of a joined result set. The response shape (status as a string) remains unchanged for API compatibility.
- Reuse the `AdvisoryStatusEnum` type defined in `entity/src/advisory.rs` — import it in the service and model layers.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping in all handler functions. Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's `.rs` scope (Rust syntax signal).
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's `.rs` scope.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `common/src/db/query.rs::apply_filter` — shared query filtering helper; use for status enum filtering instead of building custom filter logic
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper for the advisory list endpoint
- `entity/src/advisory.rs::AdvisoryStatusEnum` — the enum type defined in Task 3; import and use for type-safe status comparisons

## Acceptance Criteria
- [ ] All advisory queries no longer join the `advisory_status` table
- [ ] Advisory list endpoint filters by `advisory::Column::Status` directly
- [ ] Advisory get endpoint reads status from the advisory row directly
- [ ] `AdvisorySummary` and `AdvisoryDetails` populate status from the enum column
- [ ] API response shape is unchanged — status is still returned as a string
- [ ] `cargo check -p fundamental` compiles without errors

## Test Requirements
- [ ] Advisory list endpoint returns correct status values as strings
- [ ] Advisory list endpoint status filter works with enum values (New, Analyzing, Fixed, Rejected)
- [ ] Advisory get endpoint returns correct status for a single advisory
- [ ] No references to `advisory_status` entity remain in the fundamental module

## Verification Commands
- `cargo check -p fundamental` — fundamental module compiles without errors
- `cargo test -p fundamental` — existing unit tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
