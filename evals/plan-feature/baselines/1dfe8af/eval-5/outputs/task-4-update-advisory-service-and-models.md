# Task 4 — Update advisory service layer and models to use enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and model structs to query the `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, improving performance (estimated ~40ms p95 reduction on the list endpoint) and simplifying the query logic.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `advisory_status` table joins from `fetch`, `list`, and `search` methods; query `advisory.status` directly; update status filtering to use enum comparison instead of join-based filtering
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to source the status field from the enum column rather than a joined relation; remove any `advisory_status` model references
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct similarly to use the enum column for status
- `modules/fundamental/src/advisory/model/mod.rs` — remove any re-exports of advisory_status model types

## Implementation Notes
In `advisory.rs` service, the current query pattern likely uses something like:
```rust
Advisory::find()
    .find_also_related(AdvisoryStatus)
    .filter(...)
```
Replace with direct column access:
```rust
Advisory::find()
    .filter(advisory::Column::Status.eq(AdvisoryStatusEnum::Fixed))
```

Use the shared query builder helpers from `common/src/db/query.rs` for filtering and pagination — the existing `filter` and `paginate` helpers should work with the enum column directly.

The `AdvisorySummary` and `AdvisoryDetails` structs should map the `status` field from `AdvisoryStatusEnum` to a string for API responses. Use `.to_string()` or a `From` impl to maintain the same API response shape (status as a string).

Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for all service methods.
Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Response Types: list endpoints return `PaginatedResults<T>`.
Applies: task modifies `modules/fundamental/src/advisory/model/summary.rs` matching the convention's `.rs` scope.

## Acceptance Criteria
- [ ] All advisory queries no longer join the `advisory_status` table
- [ ] `AdvisorySummary` and `AdvisoryDetails` structs read status from the enum column
- [ ] Status filtering works with enum values (e.g., `?status=Fixed`)
- [ ] API response shape is unchanged (status is still returned as a string)
- [ ] No references to `advisory_status` entity remain in the advisory module

## Test Requirements
- [ ] `cargo build -p fundamental` compiles successfully
- [ ] Existing advisory list and detail queries return correct status values from the enum column
- [ ] Status filter query parameter works correctly with all four enum values

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

[sdlc-workflow] Description digest: sha256-md:d9f3a6b45e8c0271f4b7d2e53c6a1f04b5e8d7c23f9a4b6182e0c3d5a7f9b2e1
