## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the `AdvisoryService` to query the `status` enum column directly on the `advisory` table, removing all joins to the `advisory_status` lookup table. This includes the `fetch`, `list`, and `search` methods. Status filtering should use `WHERE status = 'Fixed'` style queries instead of `JOIN advisory_status ON ... WHERE advisory_status.name = 'Fixed'`.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` -- remove all `advisory_status` table joins from `fetch`, `list`, and `search` methods; update status filtering to use `WHERE advisory.status = <enum_value>` directly; update the query builder to work with the enum column instead of the FK + join pattern
- `modules/fundamental/src/advisory/service/mod.rs` -- remove any `use` or import of `advisory_status` entity types if present

## Implementation Notes
- The `list` method likely uses the shared query builder helpers from `common/src/db/query.rs` for filtering, pagination, and sorting. Update the status filter column reference from the joined table to the direct enum column.
- When building status filter conditions, use SeaORM's enum comparison: `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` instead of joining and comparing string values.
- The `search` method may interact with `modules/search/src/service/mod.rs` (SearchService) for full-text search. Verify the search service does not independently join `advisory_status` -- if it does, update it as well.
- Follow the query patterns in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) for reference on direct column filtering without joins.
- Per docs/constraints.md section 2 (Commit Rules): commit messages must follow Conventional Commits format, reference TC-9005 in the footer, and include the `--trailer="Assisted-by: Claude Code"`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- reference for service query patterns with direct column filtering
- `common/src/db/query.rs` -- shared query builder helpers (filtering, pagination, sorting) that may need status filter column updates

## Acceptance Criteria
- [ ] `AdvisoryService::fetch` queries the `status` enum column directly, no join to `advisory_status`
- [ ] `AdvisoryService::list` filters by `status` enum column directly, no join to `advisory_status`
- [ ] `AdvisoryService::search` does not reference `advisory_status` table
- [ ] No remaining imports or references to `advisory_status` entity in the service layer
- [ ] Advisory list endpoint p95 latency is reduced by eliminating the join overhead

## Test Requirements
- [ ] Verify advisory list query with status filter returns correct results using enum comparison
- [ ] Verify advisory fetch by ID returns correct status from enum column
- [ ] Verify advisory search results include correct status values

## Verification Commands
- `cargo check -p fundamental` -- fundamental module compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions
- Depends on: Task 4 -- Update advisory models
