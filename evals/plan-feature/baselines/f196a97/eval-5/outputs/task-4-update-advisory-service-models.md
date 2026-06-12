# Task 4 — Update advisory service and models to use enum status column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and model structs to query the `status` enum column directly on the `advisory` table instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, reducing p95 latency by approximately 40ms on the advisory list endpoint.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all joins to `advisory_status` table; update `fetch`, `list`, and `search` methods to read `status` directly from the `advisory` table's enum column; update status filtering to use `WHERE status = 'value'` instead of `WHERE advisory_status.name = 'value'` through the join
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source `status` from the advisory entity's enum field instead of from a joined `advisory_status` record; ensure the serialized output remains a string (no API shape change)
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct similarly to source `status` from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` — update any model re-exports or shared types if the status type changes

## Implementation Notes
- The `AdvisoryService` in `advisory.rs` currently joins `advisory_status` on every query. Remove the `.join()` or `.find_also_related()` calls that reference the `advisory_status` entity
- Use `advisory::Column::Status` directly in query conditions and select expressions
- The `AdvisoryStatusEnum` type from the entity layer (Task 3) implements `Display` and serializes to string, so the API response shape remains identical — status is still returned as a string value
- When building status filter conditions, compare against the enum value directly: `.filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed))` instead of joining and filtering on the lookup table
- Follow the existing query patterns in `common/src/db/query.rs` for filtering and pagination
- Ensure that `.context()` error wrapping is maintained on all service methods per the project's error handling pattern

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; reuse these for the updated status filter
- `modules/fundamental/src/sbom/service/sbom.rs` — reference pattern for service methods that read directly from entity columns without extra joins
- `modules/fundamental/src/sbom/model/summary.rs` — reference pattern for summary struct field mapping

## Acceptance Criteria
- [ ] All advisory queries (fetch, list, search) read status from the enum column without joining `advisory_status`
- [ ] `AdvisorySummary` and `AdvisoryDetails` expose status as a string in the serialized response (no API shape change)
- [ ] Status filtering works correctly for all four values (New, Analyzing, Fixed, Rejected)
- [ ] No references to `advisory_status` entity remain in the advisory service or model code

## Test Requirements
- [ ] Advisory list query returns correct status values from the enum column
- [ ] Advisory list with status filter returns only advisories matching the specified status
- [ ] Advisory fetch by ID returns the correct status from the enum column
- [ ] Response shape is unchanged (status is still a string field)

## Verification Commands
- `cargo check -p fundamental` — fundamental module compiles without errors
- `cargo test -p fundamental` — existing tests pass with updated service

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
