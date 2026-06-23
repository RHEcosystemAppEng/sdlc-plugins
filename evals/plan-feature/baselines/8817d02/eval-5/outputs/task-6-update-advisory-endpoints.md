# Task 6 — Update advisory endpoints for enum-based status filtering

## Summary

Update advisory endpoint handlers to use enum status column for filtering and response building

## Repository

trustify-backend

## Target Branch

TC-9005

## Description

Update the advisory REST endpoint handlers to work with the new enum-based status column. The list endpoint's status filter must query the enum column directly (no join). The response shape remains unchanged — status is still serialized as a string.

## Files to Modify

- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter parameter handling to use `AdvisoryStatusEnum` for query filtering instead of joining `advisory_status`
- `modules/fundamental/src/advisory/endpoints/get.rs` — update response building if it directly accesses status through the old join pattern
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if filter parameter types changed

## Implementation Notes

- In `list.rs`, the status filter query parameter should be parsed to `AdvisoryStatusEnum` and applied as a direct `WHERE advisory.status = ?` clause. Remove any join-based filter logic.
- The response serialization must produce the same JSON shape as before (status as a string field). Verify that `serde::Serialize` on `AdvisoryStatusEnum` produces the expected string values ("New", "Analyzing", "Fixed", "Rejected").
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` for query parameter handling and response construction.
- All handlers return `Result<T, AppError>` with `.context()` wrapping per the project convention.
- Use `PaginatedResults<T>` from `common/src/model/paginated.rs` for list endpoint responses.

## Reuse Candidates

- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for list endpoint query parameter handling, filtering, and paginated response
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for single-item get endpoint response pattern
- `common/src/db/query.rs` — shared filtering and pagination helpers
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper

## Acceptance Criteria

- [ ] `GET /api/v2/advisory` returns advisories with correct status values from the enum column
- [ ] `GET /api/v2/advisory?status=Fixed` correctly filters by enum value (no join)
- [ ] `GET /api/v2/advisory/{id}` returns advisory details with correct status
- [ ] The JSON response shape is identical to the previous version (backward compatible)
- [ ] The endpoints module compiles without errors

## Test Requirements

- [ ] Verify the advisory list endpoint returns correct status values
- [ ] Verify status filtering works correctly with each enum value (New, Analyzing, Fixed, Rejected)
- [ ] Verify the advisory get endpoint returns correct status for a single advisory

## Verification Commands

- `cargo check -p fundamental` — fundamental module compiles without errors

## Dependencies

- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and models to use enum status

sha256-md:52919a1ec44801c8e0177fff86cfa16c2967ad4101b437e676a102767063299a
