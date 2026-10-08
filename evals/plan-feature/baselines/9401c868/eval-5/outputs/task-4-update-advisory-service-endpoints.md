## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query (reducing p95 latency by approximately 40ms on the list endpoint) and simplifies the query logic throughout the advisory module.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` -- remove `advisory_status` table join from fetch, list, and search queries; filter by `advisory.status` enum column directly using SeaORM enum comparison
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` struct to source the status field from the enum column on the advisory row instead of from a joined table field
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` struct similarly to source status from enum column
- `modules/fundamental/src/advisory/model/mod.rs` -- update module-level type imports if advisory_status types were re-exported
- `modules/fundamental/src/advisory/endpoints/list.rs` -- update status filter logic to use enum column comparison (e.g., `WHERE status = 'Fixed'` instead of a join-based filter)
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update status retrieval to read from enum column

## Implementation Notes
- In `AdvisoryService`, replace join-based queries with direct enum column queries. For example, replace:
  ```rust
  advisory::Entity::find()
      .join(JoinType::InnerJoin, advisory::Relation::AdvisoryStatus.def())
      .filter(advisory_status::Column::Name.eq("Fixed"))
  ```
  with:
  ```rust
  advisory::Entity::find()
      .filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed))
  ```
- Update `AdvisorySummary` and `AdvisoryDetails` to derive the status string from the `AdvisoryStatusEnum` value using `to_string()` or `serde` serialization -- the API response shape must remain identical (status is still a string)
- Remove all `use` imports referencing `advisory_status` entity throughout the advisory module
- Follow the existing query pattern in `common/src/db/query.rs` for building filtered, paginated queries
- No external API contract changes -- this is an internal optimization

Per CONVENTIONS.md section "Error handling": all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust file scope.

Per CONVENTIONS.md section "Module pattern": each domain module follows `model/ + service/ + endpoints/` structure.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust file scope.

Per CONVENTIONS.md section "Response types": list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's Rust file scope.

Per CONVENTIONS.md section "Query helpers": use shared filtering, pagination, and sorting via `common/src/db/query.rs`.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting; use these for the updated advisory list queries
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` response wrapper used by list endpoints
- `modules/fundamental/src/sbom/service/sbom.rs` -- `SbomService` as a reference implementation showing query patterns without lookup table joins

## Acceptance Criteria
- [ ] `AdvisoryService::fetch` retrieves status from enum column, not from a join
- [ ] `AdvisoryService::list` filters by enum column directly
- [ ] `AdvisoryService::search` uses enum column for status-based search
- [ ] `GET /api/v2/advisory` endpoint returns advisories with status sourced from enum column
- [ ] `GET /api/v2/advisory/{id}` endpoint returns advisory details with status from enum column
- [ ] API response shape is unchanged -- status is still returned as a string value
- [ ] No `advisory_status` table join remains in any advisory query path
- [ ] No `use` imports reference the removed `advisory_status` entity

## Test Requirements
- [ ] Advisory list endpoint returns correct status values from enum column
- [ ] Advisory list endpoint with status filter returns correctly filtered results
- [ ] Advisory detail endpoint returns correct status value from enum column
- [ ] Verify no performance regression -- advisory list queries no longer include a join

## Verification Commands
- `cargo check -p fundamental` -- module compiles without error
- `cargo test -p fundamental` -- module unit tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
