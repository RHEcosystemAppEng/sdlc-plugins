## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer, model structs, and endpoint handlers to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, simplifying the query logic and reducing advisory list endpoint p95 latency. The API response shape remains unchanged — status is still returned as a string.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove `advisory_status` table join from all advisory queries (fetch, list, search); read `status` directly from the `advisory` table
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source status from the enum column instead of the joined table
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to source status from the enum column instead of the joined table
- `modules/fundamental/src/advisory/model/mod.rs` — update any type re-exports or conversions related to advisory status
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filtering logic to use the enum column directly (`WHERE status = 'Fixed'` instead of joining)
- `modules/fundamental/src/advisory/endpoints/get.rs` — update if it references the status join

## Implementation Notes
- In `advisory.rs` service, remove all `join` calls to the `advisory_status` entity. Replace them with direct column access on the `advisory` entity's new `status` field
- Update `AdvisorySummary` and `AdvisoryDetails` to derive the status string from `AdvisoryStatusEnum` instead of from a joined row. Use `.to_string()` or a `Display` impl on the enum
- For status filtering in `list.rs`, change the filter condition from `advisory_status::Column::Name.eq(value)` to `advisory::Column::Status.eq(AdvisoryStatusEnum::from_str(value))` or equivalent enum comparison
- Follow the error handling pattern: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's error handling scope.
- Follow the response type pattern: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's response type scope.
- Use shared query helpers from `common/src/db/query.rs` for filtering and pagination. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's query helper scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; reuse for the updated advisory queries
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; already used by advisory list endpoint
- `modules/fundamental/src/sbom/service/sbom.rs` — reference implementation for service queries that read columns directly without joins

## Acceptance Criteria
- [ ] All advisory queries (fetch, list, search) read status from the `advisory.status` enum column
- [ ] No references to the `advisory_status` table remain in the advisory module
- [ ] Advisory list endpoint supports filtering by status using the enum column
- [ ] API response shape is unchanged — status is returned as a string value
- [ ] All handlers maintain `Result<T, AppError>` error handling with `.context()`
- [ ] `cargo check` passes across all affected crates

## Test Requirements
- [ ] Verify advisory list query returns correct status values from the enum column
- [ ] Verify status filtering works (e.g., `?status=Fixed` returns only fixed advisories)
- [ ] Verify `AdvisorySummary` and `AdvisoryDetails` serialize status as a string in JSON responses
- [ ] Verify no compilation errors from removed `advisory_status` references

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status
