# Task 4 — Update advisory service and models to use enum status

## Summary

Update AdvisoryService queries and model structs to use status enum column instead of join

## Repository

trustify-backend

## Target Branch

TC-9005

## Description

Update the advisory service layer and model structs to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the JOIN from all advisory queries (fetch, list, search) and simplifies the model structs.

## Files to Modify

- `modules/fundamental/src/advisory/service/advisory.rs` — remove all JOINs to `advisory_status` table from fetch, list, and search queries; use `advisory::Column::Status` directly for filtering and selection
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source `status` from the advisory entity's enum field instead of a joined lookup value
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct similarly to source `status` from the enum field
- `modules/fundamental/src/advisory/model/mod.rs` — update any model re-exports or shared conversion logic that references the old `status_id` join

## Implementation Notes

- In `AdvisoryService`, locate all query builder calls that join `advisory_status::Entity` (via `.join()` or `.find_also_related()`). Remove these joins and replace status field selection with direct column access on `advisory::Column::Status`.
- For status filtering, replace `advisory_status::Column::Value.eq(...)` with `advisory::Column::Status.eq(AdvisoryStatusEnum::...)`.
- Update `AdvisorySummary` and `AdvisoryDetails` construction: the status value now comes directly from the `advisory::Model` rather than from a joined `advisory_status::Model`.
- The response shape to callers must remain identical — status is still exposed as a string. Use `.to_string()` or `serde` serialization on the enum to maintain the same API contract.
- Follow the existing query patterns in `modules/fundamental/src/sbom/service/sbom.rs` for reference on service method structure.
- Use query helpers from `common/src/db/query.rs` for filtering and pagination patterns.

## Reuse Candidates

- `modules/fundamental/src/sbom/service/sbom.rs` — reference for service query patterns (fetch, list) without joins to lookup tables
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper used by list endpoints

## Acceptance Criteria

- [ ] All advisory queries (fetch, list, search) no longer JOIN the `advisory_status` table
- [ ] `AdvisorySummary` and `AdvisoryDetails` correctly populate the `status` field from the enum column
- [ ] Status filtering works with the new enum column (e.g., filtering by `status = "Fixed"`)
- [ ] The advisory service compiles and passes type checking (`cargo check -p fundamental`)
- [ ] The external API response shape for advisory endpoints remains unchanged

## Test Requirements

- [ ] Verify that `AdvisoryService::list` returns advisories with correct status values
- [ ] Verify that `AdvisoryService::fetch` returns advisory details with the correct status
- [ ] Verify that status-based filtering returns correct results using the enum column

## Verification Commands

- `cargo check -p fundamental` — fundamental module compiles without errors

## Dependencies

- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

sha256-md:9d91ab354b978a1ee79b2151204da6ff7e30fa80dccdbe1bdc8b2ad41dfb8f53
