## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update all advisory service queries and endpoint handlers to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead that added ~40ms to advisory list endpoint p95 latency and simplifies query logic across the advisory module.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` -- remove `advisory_status` table join from `fetch`, `list`, and `search` query methods; replace with direct `advisory::Column::Status` filtering and selection
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` struct to source status from the enum column instead of the joined lookup table
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` struct to source status from the enum column instead of the joined lookup table
- `modules/fundamental/src/advisory/model/mod.rs` -- update any model-level type references or re-exports related to advisory status
- `modules/fundamental/src/advisory/endpoints/list.rs` -- update status filter parameter handling to compare against `AdvisoryStatusEnum` values instead of joining lookup table
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update single advisory retrieval to read status from enum column

## Implementation Notes
- In `AdvisoryService::list`, remove the `.join(JoinType::InnerJoin, advisory::Relation::AdvisoryStatus.def())` call and replace status selection with direct column access: `advisory::Column::Status`
- In `AdvisoryService::fetch`, remove the join and read `status` directly from the advisory query result row
- For status filtering in the list endpoint, replace the join-based filter with `.filter(advisory::Column::Status.eq(AdvisoryStatusEnum::from_str(filter_value)))` or equivalent enum comparison
- The API response shape must remain identical -- status is still returned as a string in the JSON response. Convert `AdvisoryStatusEnum` to its string representation when constructing `AdvisorySummary` and `AdvisoryDetails` response models
- Per CONVENTIONS.md §Error handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping for any new error paths introduced during the refactor.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md §Module pattern: maintain the `model/ + service/ + endpoints/` structure when updating advisory module files.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust module directory scope.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting helpers from `common/src/db/query.rs` for advisory list queries.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md §Response types: list endpoints must return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's Rust endpoint file scope.
- Constraint §5.1: changes scoped to files listed in this task
- Constraint §5.3: follow patterns referenced in Implementation Notes

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs::PaginatedResults<T>` -- response wrapper used by all list endpoints
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- reference for service query patterns without unnecessary joins
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- existing service implementation to modify in-place
- `entity/src/advisory.rs::AdvisoryStatusEnum` -- the enum type defined in Task 3 for column comparisons

## Acceptance Criteria
- [ ] `AdvisoryService::list` no longer joins the `advisory_status` table
- [ ] `AdvisoryService::fetch` reads status directly from the advisory row's enum column
- [ ] Status filtering in the list endpoint compares against `AdvisoryStatusEnum` values
- [ ] `AdvisorySummary` and `AdvisoryDetails` populate the status field from the enum column
- [ ] API response shape for advisory endpoints remains unchanged (status is still a string in JSON)
- [ ] No references to `advisory_status` table or `status_id` column remain in the fundamental module
- [ ] `cargo build -p fundamental` compiles successfully

## Test Requirements
- [ ] Verify advisory list endpoint returns correct status values sourced from the enum column
- [ ] Verify advisory get endpoint returns the correct status from the enum column
- [ ] Verify status filtering works correctly with enum value comparisons
- [ ] Verify no references to `advisory_status` table remain in the fundamental module source

## Verification Commands
- `cargo build -p fundamental` -- compilation succeeds
- `cargo test -p fundamental` -- module tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
