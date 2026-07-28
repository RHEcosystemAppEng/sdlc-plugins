## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer, model structs, and endpoint handlers to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query, which contributed to the 40ms p95 latency increase on the advisory list endpoint. All advisory queries in the service, model population, and endpoint filtering must be updated to reference `advisory.status` directly.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove `advisory_status` table join from all advisory queries (fetch, list, search); use `advisory.status` column directly for filtering and selection
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to populate `status` field from the enum column instead of the joined table
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to populate `status` field from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` — update model module if it re-exports or maps status types
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter parameter handling to use enum comparison (`WHERE status = 'Fixed'`) instead of join-based filtering
- `modules/fundamental/src/advisory/endpoints/get.rs` — update single advisory fetch to use enum column
- `modules/fundamental/src/advisory/mod.rs` — update module-level imports if advisory_status references are removed

## Implementation Notes
- The query change is the core of this task: replace `SELECT ... FROM advisory JOIN advisory_status ON advisory.status_id = advisory_status.id` with `SELECT ... status FROM advisory`. This applies to all query methods in `AdvisoryService`.
- Status filtering in the list endpoint changes from `WHERE advisory_status.name = $1` to `WHERE advisory.status = $1::advisory_status_enum`.
- Use `common/src/db/query.rs` query builder helpers for the updated filter expressions. The existing filtering/pagination/sorting infrastructure should work with the enum column with minimal changes.
- Per CONVENTIONS.md §Module Pattern: maintain the `model/ + service/ + endpoints/` structure for all changes.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's module structure scope.
- Per CONVENTIONS.md §Error Handling: all endpoint handlers must continue returning `Result<T, AppError>` with `.context()` wrapping for any new error paths.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's handler file scope.
- Per CONVENTIONS.md §Response Types: the list endpoint must continue returning `PaginatedResults<AdvisorySummary>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's list endpoint scope.
- Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs` for the updated advisory queries.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's query building scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting; reuse for enum-based status filtering
- `modules/fundamental/src/sbom/service/sbom.rs` — `SbomService` as a reference for query patterns without lookup table joins
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper used by list endpoints

## Acceptance Criteria
- [ ] All advisory queries in `AdvisoryService` use the `status` enum column directly — no join to `advisory_status` table
- [ ] Advisory list endpoint supports status filtering via enum comparison
- [ ] Advisory list endpoint returns the same response shape (status as a string in the JSON response)
- [ ] `AdvisorySummary` and `AdvisoryDetails` structs populate status from the enum column
- [ ] No references to `advisory_status` table remain in the advisory module

## Test Requirements
- [ ] Advisory list endpoint returns correct results when filtered by status (e.g., `?status=Fixed`)
- [ ] Advisory detail endpoint returns the correct status value
- [ ] Advisory list endpoint returns the same response format as before (no API contract change)
- [ ] Query performance: verify the `advisory_status` join is eliminated from query plans

## Verification Commands
- `cargo build -p fundamental` — compiles without errors
- `cargo test -p fundamental` — all module tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
