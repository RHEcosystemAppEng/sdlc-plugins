# Task 4 — Update advisory service and endpoints to use status enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to query the `status` enum column directly on the `advisory` table instead of joining the `advisory_status` lookup table. This eliminates the join overhead on every advisory query and simplifies status-based filtering. The response shape remains unchanged — status is still returned as a string to API consumers.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — Remove `advisory_status` join from all advisory queries (fetch, list, search); use `advisory::Column::Status` directly for filtering and selection
- `modules/fundamental/src/advisory/model/summary.rs` — Update `AdvisorySummary` struct to source the `status` field from the enum column instead of the joined table; adjust the `From` impl or query result mapping
- `modules/fundamental/src/advisory/model/details.rs` — Update `AdvisoryDetails` struct similarly to source status from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` — Update module-level re-exports if the status type import path changes
- `modules/fundamental/src/advisory/endpoints/list.rs` — Update status filter parameter handling to compare against enum values instead of joined table columns
- `modules/fundamental/src/advisory/endpoints/get.rs` — Update individual advisory fetch to use the enum column

## Implementation Notes
- In `AdvisoryService`, replace query patterns like `.join(advisory_status::Entity)` and `.column(advisory_status::Column::Name)` with direct `.column(advisory::Column::Status)` access
- For status filtering in the list endpoint, convert the filter string to `AdvisoryStatusEnum` using `FromStr` or a match expression, then use `.filter(advisory::Column::Status.eq(status_enum_value))`
- The `AdvisorySummary` and `AdvisoryDetails` structs should derive status as a `String` from the enum for API response serialization — use `.to_string()` or serde serialization on the enum
- Per CONVENTIONS.md §Error handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping. Apply this pattern to any new error paths introduced by enum conversion.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md §Response types: list endpoints must return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Ensure the response wrapper is preserved after removing the status join.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting from `common/src/db/query.rs` for any new filter logic.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust service file scope.
- Per CONVENTIONS.md §Module pattern: maintain the `model/ + service/ + endpoints/` structure for the advisory module.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's module structure scope.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting; reuse for status enum filtering
- `modules/fundamental/src/sbom/service/sbom.rs` — Reference for service query patterns without join-based filtering
- `modules/fundamental/src/advisory/endpoints/mod.rs` — Existing route registration to verify endpoint structure is preserved

## Acceptance Criteria
- [ ] All advisory queries (list, get, search) use `advisory::Column::Status` directly without joining `advisory_status`
- [ ] Status filtering on the list endpoint works with enum values (e.g., `?status=Fixed`)
- [ ] API response shape is unchanged — `status` is still returned as a string
- [ ] Advisory list endpoint p95 latency is reduced by eliminating the join
- [ ] No references to `advisory_status` entity remain in the service or endpoint code

## Test Requirements
- [ ] Verify advisory list endpoint returns correct status values from the enum column
- [ ] Verify status filter parameter correctly filters advisories by enum value
- [ ] Verify advisory detail endpoint returns the correct status from the enum column
- [ ] Verify invalid status filter values return an appropriate error response

## Verification Commands
- `cargo check -p fundamental` — fundamental module compiles without errors
- `cargo test -p fundamental` — unit tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
