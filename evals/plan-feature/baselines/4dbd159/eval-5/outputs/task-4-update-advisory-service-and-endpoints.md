# Task 4 — Update advisory service and endpoints to use enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the AdvisoryService, advisory models, and advisory endpoints to query the `advisory.status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead that added ~40ms to p95 latency on the advisory list endpoint. All advisory queries, filters, and response mappings must be updated to use the new enum column.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `advisory_status` table joins from fetch, list, and search methods; replace `status_id` filters with direct `status` enum column filters (e.g., `Column::Status.eq(AdvisoryStatusEnum::Fixed)`)
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source `status` from the entity's enum field directly instead of from a joined table; update any `From` or conversion impl that mapped from the join result
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct similarly to source `status` from the enum column
- `modules/fundamental/src/advisory/endpoints/list.rs` — update the list endpoint handler to filter by `advisory.status` enum column instead of joining `advisory_status`; update any query parameter parsing for status filters to map to `AdvisoryStatusEnum` values
- `modules/fundamental/src/advisory/endpoints/get.rs` — update the get endpoint to read status from the entity's enum field directly
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if any route configuration references the old join pattern
- `modules/fundamental/src/advisory/mod.rs` — remove any re-exports of `advisory_status` types

## Implementation Notes
- Import `AdvisoryStatusEnum` from `entity::advisory` in all files that need it
- In `advisory.rs` (service), replace patterns like:
  ```rust
  // OLD: join-based query
  Advisory::find()
      .find_also_related(AdvisoryStatus)
      .filter(advisory_status::Column::Name.eq("Fixed"))
  ```
  with:
  ```rust
  // NEW: direct enum filter
  Advisory::find()
      .filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed))
  ```
- In `summary.rs` and `details.rs`, the status field was likely populated from the join result tuple `(advisory::Model, Option<advisory_status::Model>)`. Update the `From` impl to take just `advisory::Model` and read `.status` directly
- For list endpoint status filter query parameters, parse the incoming string (e.g., `"Fixed"`) to `AdvisoryStatusEnum` using SeaORM's enum conversion or a manual match
- Follow the query builder patterns in `common/src/db/query.rs` for filtering and pagination — the advisory list endpoint likely uses shared query helpers that may need updating if they referenced the old join
- Check `common/src/db/query.rs` for any advisory-specific filter helpers that join `advisory_status` and update them

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting; check for advisory status filter logic that may need updating
- `modules/fundamental/src/sbom/service/sbom.rs` — reference for SeaORM service query patterns without joins
- `modules/fundamental/src/sbom/model/summary.rs` — reference for model struct conversion from a single entity (no join tuple)

## Acceptance Criteria
- [ ] All advisory queries (list, get, search) use `advisory.status` directly without joining `advisory_status`
- [ ] Status filtering on the advisory list endpoint works correctly with enum values
- [ ] `AdvisorySummary` and `AdvisoryDetails` structs correctly populate the status field from the enum column
- [ ] No references to `advisory_status` entity or table remain in the advisory module
- [ ] The advisory module compiles without errors
- [ ] API response shape is unchanged — status is still returned as a string

## Test Requirements
- [ ] Verify the advisory list endpoint returns correct results when filtering by status
- [ ] Verify the advisory get endpoint returns the correct status value
- [ ] Verify that the response JSON shape is identical to the pre-migration format (status is a string, not an enum variant object)

## Verification Commands
- `cargo check -p fundamental` — module compiles without errors
- `cargo test -p fundamental -- advisory` — advisory-related unit tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
