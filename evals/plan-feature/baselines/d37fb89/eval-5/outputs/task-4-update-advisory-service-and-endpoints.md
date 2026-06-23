## Summary
Update advisory service and endpoints to use status enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and HTTP endpoints to query the `status` enum column directly on the `advisory` table instead of joining the `advisory_status` lookup table. This eliminates the join from all advisory queries, reducing p95 latency on the advisory list endpoint. The `AdvisorySummary` and `AdvisoryDetails` model structs must source the status field from the new enum column. Status filtering in the list endpoint must use `WHERE status = 'Fixed'` style queries instead of the previous join-based filter.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` -- remove `advisory_status` table join from all query methods (fetch, list, search); filter and select status directly from `advisory.status` enum column
- `modules/fundamental/src/advisory/model/summary.rs` -- update `AdvisorySummary` struct to source `status` from the enum column instead of the joined lookup table; change the status field type from `String` to `AdvisoryStatusEnum` (or keep as `String` if the API response must remain unchanged, converting with `.to_string()`)
- `modules/fundamental/src/advisory/model/details.rs` -- update `AdvisoryDetails` struct to source `status` from the enum column instead of the joined lookup table
- `modules/fundamental/src/advisory/model/mod.rs` -- update module-level re-exports if the status type changes
- `modules/fundamental/src/advisory/endpoints/list.rs` -- update status filter parameter handling to compare against enum values instead of joining lookup table
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update single-advisory fetch to use enum column (change flows through service layer)

## Implementation Notes
The advisory list endpoint at `GET /api/v2/advisory` currently joins `advisory_status` for both display and filtering. Replace all `advisory_status` joins with direct column access on `advisory.status`. Use SeaORM's enum column filtering: `Column::Status.eq(AdvisoryStatusEnum::Fixed)`. The API response shape must remain identical -- status is still serialized as a string. Use the query builder helpers from `common/src/db/query.rs` for filtering and pagination, following the existing patterns. The list endpoint returns `PaginatedResults<AdvisorySummary>` from `common/src/model/paginated.rs` -- this wrapper does not change, only the inner query changes.

Per CONVENTIONS.md: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's `.rs` endpoint file scope.

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting; reuse for advisory list query construction
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` response wrapper used by all list endpoints
- `common/src/error.rs` -- `AppError` enum for consistent error handling with `.context()` wrapping

## Acceptance Criteria
- [ ] Advisory list endpoint (`GET /api/v2/advisory`) returns results without joining `advisory_status` table
- [ ] Advisory detail endpoint (`GET /api/v2/advisory/{id}`) returns status from enum column
- [ ] Status filtering on advisory list works with enum values (e.g., `?status=Fixed`)
- [ ] API response shape is unchanged -- status is still a string in the JSON response
- [ ] No remaining references to `advisory_status` table in the advisory service or endpoint code
- [ ] All advisory queries compile and execute without errors

## Test Requirements
- [ ] Verify `GET /api/v2/advisory` returns advisory list with correct status values from enum column
- [ ] Verify `GET /api/v2/advisory?status=Fixed` filters correctly using enum comparison
- [ ] Verify `GET /api/v2/advisory/{id}` returns correct status for a single advisory
- [ ] Verify API response JSON shape is unchanged (status field is a string)

## Verification Commands
- `cargo build -p fundamental` -- fundamental module compiles successfully
- `cargo test -p fundamental` -- all existing advisory tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:643161acfe0c9d82bf5c9d0931c34fdb68e9efff58d8ab55363ff0ac3351d3ce
