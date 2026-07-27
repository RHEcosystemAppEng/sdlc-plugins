## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service and model layer to query the `advisory.status` enum column directly, eliminating the join to the `advisory_status` lookup table. This covers the `AdvisoryService` methods (fetch, list, search) and the model structs (`AdvisorySummary`, `AdvisoryDetails`).

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove `advisory_status` join from all query methods; use `advisory::Column::Status` directly for filtering and selection
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` to populate the status field from the enum column instead of the joined table
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` to populate the status field from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` — update model module if it re-exports status-related types from the old advisory_status entity

## Implementation Notes
- The `AdvisoryService` currently joins `advisory_status` to get status names — replace all join-based queries with direct column access on `advisory::Column::Status`
- Per CONVENTIONS.md §Error Handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping on fallible operations.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's handler file scope.
- Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting from `common/src/db/query.rs` for list operations.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's query helper scope.
- See `modules/fundamental/src/sbom/service/sbom.rs` for the standard service query pattern — `SbomService` uses similar query builder approach without status table joins
- Remove any `use entity::advisory_status` imports from service and model files
- The enum column value serializes directly to the same string format the API previously returned from the join, so model struct field types may remain `String` or change to `AdvisoryStatusEnum` depending on serialization approach

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; advisory queries should continue using these after removing the join
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reference implementation of service query patterns without status table joins

## Acceptance Criteria
- [ ] All `AdvisoryService` methods query `advisory.status` directly without joining `advisory_status`
- [ ] `AdvisorySummary` and `AdvisoryDetails` correctly expose the status field from the enum column
- [ ] No references to `advisory_status` entity remain in the advisory service or model modules
- [ ] Status filtering works correctly with the enum column

## Test Requirements
- [ ] Service methods return correct status values from the enum column
- [ ] Status filtering returns only advisories matching the requested status
- [ ] Service compiles without errors (`cargo check -p fundamental`)

## Verification Commands
- `cargo check -p fundamental` — fundamental module compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions (service depends on updated entity types)
