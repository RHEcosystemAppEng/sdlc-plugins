## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to use the `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query and simplifies status filtering. All advisory list and detail queries must be rewritten to read from the `status` column on the `advisory` table.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `advisory_status` table joins from advisory queries; use `advisory::Column::Status` for filtering and selection instead of join-based status resolution
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to populate `status` from the enum column instead of from a joined relation
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to populate `status` from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` — update any model-level re-exports or shared types that reference the advisory_status relation
- `modules/fundamental/src/advisory/endpoints/list.rs` — update list endpoint to filter by enum column (`WHERE status = 'Fixed'`) instead of join
- `modules/fundamental/src/advisory/endpoints/get.rs` — update get endpoint to return status from enum column

## Implementation Notes
- Remove all `.join()` or `.find_also_related(advisory_status::Entity)` calls from advisory queries in the service layer
- Replace status filter expressions: instead of joining and filtering on `advisory_status::Column::Name`, filter directly on `advisory::Column::Status` using the `AdvisoryStatusEnum` variants
- The `AdvisorySummary` and `AdvisoryDetails` structs should have their `status` field typed as `AdvisoryStatusEnum` (or `String` if the API response serializes it as a string)
- No API response shape changes — the status field in the response remains a string. SeaORM's `DeriveActiveEnum` handles serialization to string automatically

Per CONVENTIONS.md §Error handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping — maintain this pattern in updated query code.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust handler/service scope.

Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting utilities from `common/src/db/query.rs` for updated advisory list queries.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's query helper scope.

Per CONVENTIONS.md §Response types: list endpoints must return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's response type scope.

Per CONVENTIONS.md §Module pattern: maintain the `model/ + service/ + endpoints/` structure for the advisory module.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's module structure scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; reuse for updated advisory list queries
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; already used by list endpoint
- `modules/fundamental/src/sbom/service/sbom.rs` — reference for service query patterns without join-based lookups

## Acceptance Criteria
- [ ] All advisory queries (list, get, search) use `advisory::Column::Status` instead of joining `advisory_status`
- [ ] No remaining references to `advisory_status` entity in service or endpoint code
- [ ] Advisory list endpoint filters by enum column correctly (e.g., `?status=Fixed` works)
- [ ] Advisory detail endpoint returns status from enum column
- [ ] API response shape is unchanged — status is still a string field in the response
- [ ] Advisory list endpoint p95 latency reduced (join eliminated)

## Test Requirements
- [ ] Verify advisory list endpoint returns correct results with status filter
- [ ] Verify advisory detail endpoint returns correct status value
- [ ] Verify no SQL joins to `advisory_status` table in generated queries
- [ ] Verify all four status values (New, Analyzing, Fixed, Rejected) work as filter values

## Verification Commands
- `cargo check -p fundamental` — verify fundamental module compiles
- `cargo test -p fundamental` — run module-level tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
