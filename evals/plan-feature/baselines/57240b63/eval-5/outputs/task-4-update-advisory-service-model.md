# Task 4 — Update advisory service and model layer to use status enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and model structs to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join overhead from all advisory queries (list, get, search) and simplifies the query builder logic. The `AdvisorySummary` and `AdvisoryDetails` structs must source the status field from the enum column, and all query code that previously joined `advisory_status` must be updated to read the `status` column directly.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — Remove `advisory_status` table join from `fetch`, `list`, and `search` queries; read `status` directly from the `advisory` table column
- `modules/fundamental/src/advisory/model/summary.rs` — Update `AdvisorySummary` struct to use `AdvisoryStatusEnum` for the status field instead of a joined string value
- `modules/fundamental/src/advisory/model/details.rs` — Update `AdvisoryDetails` struct to use `AdvisoryStatusEnum` for the status field
- `modules/fundamental/src/advisory/model/mod.rs` — Update model module exports if needed for the enum type
- `modules/fundamental/src/advisory/endpoints/list.rs` — Update status filtering logic to use enum comparison (`WHERE status = 'Fixed'`) instead of join-based filtering
- `modules/fundamental/src/advisory/endpoints/get.rs` — Update if it references the advisory status join

## Implementation Notes
- In `modules/fundamental/src/advisory/service/advisory.rs`, locate all queries that join `advisory_status` (e.g., `.join(JoinType::InnerJoin, advisory::Relation::AdvisoryStatus.def())`). Replace these joins with direct column access on `advisory::Column::Status`.
- For the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs`, change the `status` field type from `String` to `AdvisoryStatusEnum` (imported from the entity crate). The serialized API response will remain a string because SeaORM enum serialization produces the variant name.
- For status filtering in endpoint handlers, update the filter expression from a joined column reference (e.g., `advisory_status::Column::Name.eq(filter_value)`) to a direct column filter (e.g., `advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed)`).
- Follow the query builder pattern used in `common/src/db/query.rs` for filtering and pagination — the shared helpers should work unchanged since they operate on column references.
- Follow the error handling pattern: all service methods return `Result<T, AppError>` with `.context()` wrapping, as established throughout the codebase.
- Per CONVENTIONS.md §Module pattern: maintain the `model/ + service/ + endpoints/` structure.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust module scope.
- Per CONVENTIONS.md §Error handling: use `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's endpoint file scope.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting; should work unchanged with enum column filters
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper used by list endpoints
- `common/src/error.rs` — `AppError` enum for error handling pattern reference
- `modules/fundamental/src/sbom/service/sbom.rs` — Reference for service query patterns without lookup table joins

## Acceptance Criteria
- [ ] All advisory queries (list, get, search) read status from the `advisory.status` enum column directly — no `advisory_status` table join remains
- [ ] `AdvisorySummary` and `AdvisoryDetails` structs use `AdvisoryStatusEnum` for the status field
- [ ] Status filtering on the advisory list endpoint works with enum values (e.g., `?status=Fixed`)
- [ ] API response shape is unchanged — status is still serialized as a string in JSON responses
- [ ] Advisory list endpoint p95 latency is reduced (no more join overhead)
- [ ] The fundamental module compiles without errors

## Test Requirements
- [ ] Verify advisory list endpoint returns correct status values as strings in the JSON response
- [ ] Verify advisory list endpoint with status filter returns only matching advisories
- [ ] Verify advisory get endpoint returns the correct status for a single advisory
- [ ] Verify the advisory module compiles: `cargo check -p fundamental`

## Verification Commands
- `cargo check -p fundamental` — expected: compiles without errors
- `cargo test -p fundamental` — expected: existing unit tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

---

[sdlc-workflow] Description digest: sha256-md:193c39afce3605ab28466bb43950a5655eb390ca0235b52fb22efe33b64d4c40
