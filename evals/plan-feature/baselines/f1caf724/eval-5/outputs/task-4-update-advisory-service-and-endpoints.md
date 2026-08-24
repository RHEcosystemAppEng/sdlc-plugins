## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and endpoint handlers to query the `status` enum column directly instead of joining the `advisory_status` lookup table. Remove all join logic for the advisory status from service queries, model structs, and endpoint handlers. The advisory list endpoint's status filtering should use `WHERE status = 'Fixed'` style queries instead of joining on `advisory_status.name`.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove `advisory_status` table join from all query methods (fetch, list, search); filter by `status` enum column directly
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source status from the enum field instead of a joined relation
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to source status from the enum field instead of a joined relation
- `modules/fundamental/src/advisory/endpoints/list.rs` — update the list handler to pass enum-based status filter parameters to the service
- `modules/fundamental/src/advisory/endpoints/get.rs` — update the get handler to return status from the enum field

## Implementation Notes
The `AdvisoryService` methods that query advisories currently join the `advisory_status` table to resolve the status name. After this change, the status is directly available as a column on the `advisory` table, so:

1. Remove all `.join(JoinType::InnerJoin, advisory::Relation::AdvisoryStatus.def())` calls
2. Replace `advisory_status::Column::Name` references with `advisory::Column::Status`
3. Update any status filter conditions to compare against `AdvisoryStatusEnum` variants instead of string-matching on the joined table

The response shape to API consumers does not change — status is still returned as a string. The `AdvisorySummary` and `AdvisoryDetails` structs should serialize the enum to its string representation.

Per CONVENTIONS.md §Module pattern: maintain the model/ + service/ + endpoints/ structure for the advisory domain module.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's module structure scope.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's handler file scope.

Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's endpoint file scope.

Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's query file scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting; reuse existing filter patterns for the enum column
- `common/src/model/paginated.rs::PaginatedResults<T>` — response wrapper for list endpoints; already in use, no changes needed
- `modules/fundamental/src/sbom/service/sbom.rs` — reference for service query patterns without join tables

## Acceptance Criteria
- [ ] `AdvisoryService::list` queries `advisory.status` directly without joining `advisory_status`
- [ ] `AdvisoryService::fetch` queries `advisory.status` directly without joining `advisory_status`
- [ ] Status filtering on the advisory list endpoint uses the enum column
- [ ] `AdvisorySummary` includes status sourced from the enum field
- [ ] `AdvisoryDetails` includes status sourced from the enum field
- [ ] No references to `advisory_status` table or entity remain in the advisory module
- [ ] API response shape is unchanged (status is still a string in the JSON response)

## Test Requirements
- [ ] Verify advisory list endpoint returns correct status values from the enum column
- [ ] Verify advisory list endpoint filters by status correctly using enum values
- [ ] Verify advisory detail endpoint returns correct status from the enum column
- [ ] Verify no SQL joins to `advisory_status` appear in generated queries

## Verification Commands
- `cargo check -p trustify-fundamental` — fundamental module compiles successfully
- `cargo test -p trustify-fundamental -- advisory` — advisory unit tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
