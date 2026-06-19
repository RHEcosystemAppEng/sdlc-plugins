# Task 4 — Update advisory service and endpoints to use enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and endpoint handlers to query the `status` enum column directly on the `advisory` table instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, reducing latency on the advisory list endpoint. Update the advisory model structs (AdvisorySummary, AdvisoryDetails) to source the status from the enum field.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove `advisory_status` join from fetch, list, and search queries; filter on `advisory.status` enum column directly
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source status from the enum field instead of joined table
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to source status from the enum field
- `modules/fundamental/src/advisory/model/mod.rs` — update module re-exports if needed for the status type change
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter parameter handling to compare against enum values directly
- `modules/fundamental/src/advisory/endpoints/get.rs` — update if it references the status join

## Implementation Notes
In `advisory.rs` (service), replace any `join` or `find_related` calls to the `advisory_status` entity with direct column access on the `advisory` table's `status` field. Status filtering should use `column.eq(AdvisoryStatusEnum::Fixed)` style comparisons.

Use the shared query helpers from `common/src/db/query.rs` for filtering and pagination, consistent with the existing patterns in the service.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` handler scope.

Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's endpoint scope.

Per CONVENTIONS.md §Query helpers: shared filtering, pagination, and sorting via `common/src/db/query.rs`. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's query scope.

Per CONVENTIONS.md §Module pattern: each domain module follows `model/ + service/ + endpoints/` structure. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's module scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting; reuse for the updated advisory queries
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; already used by advisory list, ensure continued use
- `common/src/error.rs` — `AppError` enum; use `.context()` wrapping on any new error paths

## Acceptance Criteria
- [ ] Advisory list query no longer joins `advisory_status` table
- [ ] Advisory fetch/get query no longer joins `advisory_status` table
- [ ] Status filtering works using the enum column directly
- [ ] `AdvisorySummary` and `AdvisoryDetails` correctly populate status from enum field
- [ ] API response shape is unchanged (status is still returned as a string)
- [ ] All handlers continue to return `Result<T, AppError>`

## Test Requirements
- [ ] Advisory list endpoint returns correct status values from enum column
- [ ] Advisory list endpoint with status filter returns filtered results correctly
- [ ] Advisory get endpoint returns correct status value from enum column
- [ ] No regressions in response shape or status codes

## Verification Commands
- `cargo test --test advisory` — advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
