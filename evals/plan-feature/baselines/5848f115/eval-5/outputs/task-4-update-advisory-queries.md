## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query and simplifies status-based filtering. The advisory list endpoint's status filter should use `WHERE status = '<value>'` instead of a join condition, reducing p95 latency by approximately 40ms.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `advisory_status` table joins from `fetch`, `list`, and `search` methods; replace with direct `status` column queries using the `AdvisoryStatusEnum` type; update any query builder calls that reference `advisory_status`
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct if it contains a `status` field that was populated from a join; ensure it maps directly from the entity's enum column
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct similarly; remove any nested `AdvisoryStatus` object if one was used to represent the joined data
- `modules/fundamental/src/advisory/endpoints/list.rs` — update the list handler's query filtering to use the enum column directly; update any query parameter parsing for status filters
- `modules/fundamental/src/advisory/endpoints/get.rs` — update the get handler if it performs a status join
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if filter parameter types change

## Implementation Notes
- The existing query patterns in `common/src/db/query.rs` provide shared filtering, pagination, and sorting helpers. Use these helpers for the updated status filter instead of writing custom query logic.
- For the list endpoint filter, the status filter should accept a string parameter and convert it to `AdvisoryStatusEnum` before passing to the query builder. Use SeaORM's `ColumnTrait::eq()` with the enum value.
- The `AdvisorySummary` and `AdvisoryDetails` structs should expose `status` as a `String` in the API response (serialized from the enum) to maintain backward compatibility — the response shape must remain identical.
- Per the project's Key Conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping. Maintain this pattern for any error paths in the updated query logic.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust service file scope.
- Per the project's Key Conventions: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Ensure the updated list query continues to use this wrapper.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's endpoint file scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; use for the updated status filter
- `modules/fundamental/src/sbom/service/sbom.rs` — reference for service method patterns (fetch, list) without joins to lookup tables
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for list endpoint filter implementation pattern

## Acceptance Criteria
- [ ] No references to `advisory_status` table or entity remain in the advisory module
- [ ] The advisory list endpoint filters by `advisory.status` enum column directly (no join)
- [ ] The advisory list endpoint returns the same response shape as before (status as a string)
- [ ] Status filtering works for all four values: New, Analyzing, Fixed, Rejected
- [ ] The advisory get endpoint returns the correct status without a join

## Test Requirements
- [ ] Verify the advisory list endpoint returns correctly filtered results when querying by each status value
- [ ] Verify the advisory get endpoint returns the correct status field in the response
- [ ] Verify that no SQL join to `advisory_status` is generated (check query logs or explain plan)

## Verification Commands
- `cargo check -p fundamental` — compiles without errors
- `grep -r "advisory_status" modules/fundamental/src/advisory/` — returns no results

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions
