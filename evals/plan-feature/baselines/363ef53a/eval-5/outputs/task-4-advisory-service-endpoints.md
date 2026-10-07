## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update all advisory service layer queries and endpoint handlers to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query and simplifies status filtering. The external response shape remains unchanged -- status is still returned as a string.

## Files to Modify
- `modules/fundamental/src/advisory/model/summary.rs` -- Update `AdvisorySummary` struct to source status from the enum column instead of the join result
- `modules/fundamental/src/advisory/model/details.rs` -- Update `AdvisoryDetails` struct to source status from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` -- Update module-level type exports if the `AdvisoryStatus` type changes or is replaced by `AdvisoryStatusEnum`
- `modules/fundamental/src/advisory/service/advisory.rs` -- Remove `advisory_status` table join from all advisory queries; update status filtering to use `WHERE advisory.status = 'value'` instead of join-based filtering
- `modules/fundamental/src/advisory/endpoints/list.rs` -- Update list handler's query building to use direct enum column for status filtering
- `modules/fundamental/src/advisory/endpoints/get.rs` -- Update get handler to use direct enum column for status retrieval
- `modules/search/src/service/mod.rs` -- Update SearchService if it joins or references `advisory_status` for advisory search or filtering

## Implementation Notes
- Remove all `advisory_status` table joins from advisory queries -- reference `advisory.status` directly
- Status filtering changes from `WHERE advisory_status.name = 'Fixed'` (join-based) to `WHERE advisory.status = 'Fixed'` (direct enum comparison)
- The `AdvisorySummary` and `AdvisoryDetails` structs should read status from the enum column; SeaORM automatically converts enum values to their string representation via `DeriveActiveEnum`
- Check the search module (`modules/search/src/service/mod.rs`) for any `advisory_status` joins -- update if found, skip if absent
- Use the shared query helper patterns from `common/src/db/query.rs` for the updated filtering logic

Per CONVENTIONS.md §Module pattern: maintain the model/ + service/ + endpoints/ structure in the advisory module.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's domain module scope.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's handler (.rs) file scope.

Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust (.rs) file scope.

## Reuse Candidates
- `common/src/db/query.rs` -- Shared query builder helpers for filtering, pagination, and sorting; use for updated advisory status filter queries
- `modules/fundamental/src/sbom/service/sbom.rs` -- SbomService as reference for service-layer query patterns without lookup-table joins
- `modules/fundamental/src/advisory/endpoints/list.rs` -- Existing list endpoint handler to understand current query construction

## Acceptance Criteria
- [ ] All advisory queries use `advisory.status` enum column directly -- no `advisory_status` table joins remain
- [ ] `AdvisorySummary` correctly includes status from the enum column
- [ ] `AdvisoryDetails` correctly includes status from the enum column
- [ ] Advisory list endpoint supports status filtering via direct enum comparison
- [ ] Advisory list endpoint response shape is unchanged (status is still a string)
- [ ] Search module advisory queries are updated if they referenced `advisory_status`
- [ ] No references to `advisory_status` table or `status_id` column remain in the advisory service layer or endpoints

## Test Requirements
- [ ] `cargo check -p fundamental` passes with updated service and endpoint code
- [ ] `cargo check -p search` passes if search module was modified
- [ ] Advisory list endpoint returns correct status values from the enum column
- [ ] Status filtering via query parameter works correctly (e.g., `?status=Fixed`)

## Verification Commands
- `cargo check -p fundamental` -- Verify fundamental module compiles
- `cargo check -p search` -- Verify search module compiles

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
