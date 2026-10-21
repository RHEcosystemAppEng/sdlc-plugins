## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and endpoints to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, reducing advisory list endpoint p95 latency by approximately 40ms. Update the `AdvisorySummary` and `AdvisoryDetails` model structs to carry the enum value, and update the list and get endpoints to filter by the enum column.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `advisory_status` joins from `fetch`, `list`, and `search` methods; query `advisory.status` directly using the enum column
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to use `AdvisoryStatusEnum` for the status field instead of a joined string
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to use `AdvisoryStatusEnum` for the status field
- `modules/fundamental/src/advisory/model/mod.rs` — update model module imports if needed for the enum type
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter to use `WHERE advisory.status = <enum_value>` instead of joining advisory_status
- `modules/fundamental/src/advisory/endpoints/get.rs` — update single advisory fetch to use the direct enum column
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if query parameter types change for status filtering
- `modules/fundamental/src/advisory/mod.rs` — update module imports if needed

## Implementation Notes
- In `advisory.rs` (service), replace all occurrences of the `advisory_status` join pattern. The existing code likely has something like:
  ```
  advisory::Entity::find()
      .join(JoinType::InnerJoin, advisory::Relation::AdvisoryStatus.def())
      .filter(advisory_status::Column::Name.eq(status_filter))
  ```
  Replace with:
  ```
  advisory::Entity::find()
      .filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed))
  ```
- In model structs (`summary.rs`, `details.rs`), the status field should serialize to the same string representation as before (e.g., `"Fixed"`, `"New"`) so the API response shape remains identical to callers. Use `#[serde(rename_all = "PascalCase")]` or implement custom serialization if needed.
- Per repo Key Conventions §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Maintain this pattern in any modified handler code.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` service file scope.
- Per repo Key Conventions §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Ensure the advisory list endpoint continues to return `PaginatedResults<AdvisorySummary>`.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's `.rs` endpoint file scope.
- Per repo Key Conventions §Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs` for advisory list queries.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's `.rs` endpoint file scope.
- Reference `modules/fundamental/src/sbom/service/sbom.rs` for the established service query pattern (entity find, filter, pagination).
- Reference `modules/fundamental/src/sbom/endpoints/list.rs` for the established list endpoint pattern.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs` — existing service demonstrating entity find, filter, and pagination patterns without joins
- `modules/fundamental/src/sbom/model/summary.rs` — existing model struct showing field definitions and serde derives
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper used by all list endpoints

## Acceptance Criteria
- [ ] `AdvisoryService::list` queries `advisory.status` directly without joining `advisory_status`
- [ ] `AdvisoryService::fetch` queries `advisory.status` directly without joining `advisory_status`
- [ ] `AdvisorySummary` struct uses `AdvisoryStatusEnum` for the status field
- [ ] `AdvisoryDetails` struct uses `AdvisoryStatusEnum` for the status field
- [ ] Advisory list endpoint (`GET /api/v2/advisory`) supports filtering by status using the enum column
- [ ] Advisory get endpoint (`GET /api/v2/advisory/{id}`) returns the status from the enum column
- [ ] API response shape is unchanged — status is still serialized as a string (e.g., `"Fixed"`, `"New"`)
- [ ] No remaining references to `advisory_status` entity or table in the fundamental module
- [ ] `cargo build -p fundamental` compiles without errors

## Test Requirements
- [ ] Advisory list query returns correct results when filtering by each status value
- [ ] Advisory detail query returns the correct enum status value
- [ ] API response JSON shape matches the previous format (backward compatible)
- [ ] No join to `advisory_status` appears in any query

## Verification Commands
- `cargo build -p fundamental` — fundamental module compiles cleanly
- `cargo test -p fundamental` — fundamental module tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
