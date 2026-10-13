## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to query the `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead that was adding ~40ms to advisory list endpoint p95 latency. The advisory model structs must source the status value from the new enum field, and status filtering must use direct enum comparison instead of a join-based filter.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — Remove the `advisory_status` table join from all advisory queries (fetch, list, search). Replace join-based status filtering with direct `WHERE status = <enum_value>` filtering on the `advisory` table. Use `advisory::Column::Status` instead of `advisory_status::Column::Name`
- `modules/fundamental/src/advisory/model/summary.rs` — Update `AdvisorySummary` struct to source the `status` field from `advisory::Model.status` (the enum) instead of from the joined `advisory_status` row
- `modules/fundamental/src/advisory/model/details.rs` — Update `AdvisoryDetails` struct similarly to source `status` from the enum column
- `modules/fundamental/src/advisory/endpoints/list.rs` — Update the list endpoint handler to pass enum-based status filter parameters to the service layer
- `modules/fundamental/src/advisory/endpoints/get.rs` — Update the get endpoint handler if it references the advisory status join
- `modules/fundamental/src/advisory/mod.rs` — Remove any `use` or `mod` references to the `advisory_status` entity

## Implementation Notes
The existing query pattern in `modules/fundamental/src/advisory/service/advisory.rs` likely uses SeaORM's `find().find_also_related(advisory_status::Entity)` or a manual join. Replace this with a direct select on the `advisory` table since `status` is now a column on the entity itself.

For status filtering, the current pattern likely filters by joining to `advisory_status` and comparing `advisory_status::Column::Name`. Replace with filtering directly on `advisory::Column::Status` using the `AdvisoryStatusEnum` variants.

Use the shared query builder helpers in `common/src/db/query.rs` for filtering and pagination, following the existing patterns in other service modules (e.g., `modules/fundamental/src/sbom/service/sbom.rs`).

Reuse `common/src/model/paginated.rs::PaginatedResults<T>` for list endpoint responses. Follow the error handling pattern: `Result<T, AppError>` with `.context()` wrapping from `common/src/error.rs`.

Per CONVENTIONS.md §Error handling: use `Result<T, AppError>` with `.context()` wrapping for all handler returns.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Module pattern: maintain `model/ + service/ + endpoints/` structure.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's module directory scope.

Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>`.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's endpoint scope.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting; reuse for advisory list queries after removing the join
- `common/src/model/paginated.rs::PaginatedResults<T>` — Response wrapper for list endpoints; already in use, ensure it remains the return type
- `common/src/error.rs::AppError` — Error type for all handlers; continue using with `.context()` wrapping
- `modules/fundamental/src/sbom/service/sbom.rs` — Reference implementation for service pattern without cross-table joins; follow its query structure

## Acceptance Criteria
- [ ] All advisory queries in `AdvisoryService` no longer join the `advisory_status` table
- [ ] Status filtering uses direct enum column comparison (`advisory::Column::Status`)
- [ ] `AdvisorySummary` and `AdvisoryDetails` source status from the entity's enum field
- [ ] Advisory list endpoint returns correct results with status filter applied
- [ ] Advisory get endpoint returns correct status value from enum
- [ ] No remaining references to `advisory_status` entity in the advisory module
- [ ] All advisory endpoints return the same response shape as before (status as string)
- [ ] `cargo build -p fundamental` compiles without errors

## Test Requirements
- [ ] `tests/api/advisory.rs` — Advisory list endpoint returns correct status values from enum column
- [ ] `tests/api/advisory.rs` — Advisory list with status filter returns only matching advisories
- [ ] `tests/api/advisory.rs` — Advisory get endpoint returns correct status in response body
- [ ] Verify p95 latency improvement is possible by confirming no joins remain in advisory queries

## Verification Commands
- `cargo test -p fundamental` — fundamental module tests pass
- `cargo test --test advisory` — advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
