## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and REST endpoints to use the new `advisory_status_enum` column directly instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, reducing the advisory list endpoint p95 latency by approximately 40ms. All query construction, filtering by status, and response serialization must reference the `advisory.status` enum column.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove `advisory_status` table joins from all query methods (fetch, list, search); update status filtering to use `advisory::Column::Status` directly with enum value comparison
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to populate the `status` field from the enum column instead of the joined table
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct similarly if it includes status
- `modules/fundamental/src/advisory/model/mod.rs` — update model module exports if needed for the new enum type
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter parameter handling to compare against `AdvisoryStatusEnum` values
- `modules/fundamental/src/advisory/endpoints/get.rs` — update single advisory fetch to use the enum column

## Implementation Notes
- In `advisory.rs` service, remove all `.join(advisory_status::Entity)` calls and replace `advisory_status::Column::Name` references with `advisory::Column::Status`.
- For status filtering in list/search queries, use `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)` pattern instead of joining and filtering on the lookup table's name column.
- The response shape to API consumers must remain unchanged — status is still serialized as a string (e.g., `"Fixed"`). SeaORM's `DeriveActiveEnum` with `#[sea_orm(string_value = "Fixed")]` handles this automatically.
- Per CONVENTIONS.md §Error handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping for any new error paths.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Query helpers: continue using shared filtering, pagination, and sorting via `common/src/db/query.rs` for the updated advisory queries.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Response types: advisory list endpoint must continue returning `PaginatedResults<AdvisorySummary>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; reuse for status-based filtering
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper already used by advisory list
- `modules/fundamental/src/sbom/service/sbom.rs` — reference for service query patterns without join tables

## Acceptance Criteria
- [ ] All advisory queries no longer join the `advisory_status` table
- [ ] `GET /api/v2/advisory` returns the same response shape as before (status as string)
- [ ] `GET /api/v2/advisory` supports filtering by status using the enum column
- [ ] `GET /api/v2/advisory/{id}` returns advisory details with status from the enum column
- [ ] No references to `advisory_status` entity remain in the service or endpoint code
- [ ] No API contract changes — response shape is identical to the pre-migration format

## Test Requirements
- [ ] Verify `GET /api/v2/advisory` returns advisories with correct status strings
- [ ] Verify `GET /api/v2/advisory?status=Fixed` filters correctly using the enum column
- [ ] Verify `GET /api/v2/advisory/{id}` returns correct status for a single advisory
- [ ] Verify that no SQL joins to `advisory_status` appear in generated queries

## Verification Commands
- `cargo build -p fundamental` — compiles without error
- `cargo test -p fundamental` — all fundamental module tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
