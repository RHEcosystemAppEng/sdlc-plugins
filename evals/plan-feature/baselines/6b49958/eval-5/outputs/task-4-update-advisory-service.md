## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and model structs to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, achieving the performance improvement goal of reducing p95 latency by ~40ms on the advisory list endpoint.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `advisory_status` table joins from query construction; use `advisory::Column::Status` for filtering and sorting instead of joining through `advisory_status::Column::Name`
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source the `status` field from the enum column instead of a joined table field
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct similarly to source `status` from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` — update any model re-exports or shared types if they reference the advisory_status entity

## Implementation Notes
- In `advisory.rs` (service), locate all query builder calls that perform `.join()` or `.find_also_related()` on the `advisory_status` entity and replace them with direct column access on `advisory::Column::Status`.
- For status filtering, replace patterns like `.filter(advisory_status::Column::Name.eq("Fixed"))` with `.filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed))`.
- Use the `AdvisoryStatusEnum` from `entity/src/advisory.rs` for type-safe comparisons.
- Follow the existing query builder pattern in `common/src/db/query.rs` for filtering and pagination — the shared query helpers should work with the enum column without modification.
- In the model structs (`AdvisorySummary`, `AdvisoryDetails`), change the `status` field type from `String` (populated via join) to `AdvisoryStatusEnum` (populated directly), or keep it as `String` with a `.to_string()` conversion in the `From` implementation — match whichever pattern the existing codebase uses for enum-to-response mapping.
- Remove any `use entity::advisory_status;` imports from service and model files.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination, already used by advisory service
- `modules/fundamental/src/sbom/service/sbom.rs` — reference implementation of service pattern without lookup table joins
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper used by list operations

## Acceptance Criteria
- [ ] All advisory queries in `AdvisoryService` no longer join the `advisory_status` table
- [ ] Status filtering works using the enum column directly
- [ ] `AdvisorySummary` and `AdvisoryDetails` correctly populate the status field from the enum column
- [ ] No references to `advisory_status` entity remain in the advisory service or model modules
- [ ] The advisory list endpoint response shape remains identical (status is still a string in JSON)

## Test Requirements
- [ ] Verify advisory list query executes without joining `advisory_status`
- [ ] Verify status filter produces correct results with each enum value (New, Analyzing, Fixed, Rejected)
- [ ] Verify `AdvisorySummary` and `AdvisoryDetails` serialize status as a string in JSON responses

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256:ef0c7402cbdd7698775bec881275b2a1ad86d95ab9adad4bfae844533fb1730c
