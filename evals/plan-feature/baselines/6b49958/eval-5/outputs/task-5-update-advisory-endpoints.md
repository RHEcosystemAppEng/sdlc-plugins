## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory endpoints to filter and sort by the new `status` enum column instead of joining the `advisory_status` lookup table. Ensure the REST API response shape remains unchanged so this is transparent to API consumers.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` — update query parameter handling for status filter to use the enum column; remove any join logic with `advisory_status`
- `modules/fundamental/src/advisory/endpoints/get.rs` — update single-advisory retrieval to source status from the enum column
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if any route configuration references the `advisory_status` entity

## Implementation Notes
- In `list.rs`, if the endpoint accepts a status filter query parameter (e.g., `?status=Fixed`), update the parsing to convert the string to `AdvisoryStatusEnum` and filter using `advisory::Column::Status.eq(enum_value)` instead of joining `advisory_status`.
- Follow the existing endpoint patterns in `modules/fundamental/src/sbom/endpoints/list.rs` and `get.rs` for how endpoints interact with the service layer and return `PaginatedResults<T>`.
- Error handling must follow the `Result<T, AppError>` pattern with `.context()` wrapping as documented in `common/src/error.rs`.
- The response JSON must remain backward-compatible: the `status` field in advisory responses should still be a string value (e.g., `"Fixed"`), not the Rust enum's debug representation.
- Remove any `use entity::advisory_status;` imports from endpoint files.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates endpoint pattern for list operations with filtering and pagination
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates single-entity retrieval endpoint pattern
- `common/src/error.rs` — `AppError` enum used for error handling in all endpoints

## Acceptance Criteria
- [ ] `GET /api/v2/advisory` returns advisory list without joining `advisory_status`
- [ ] `GET /api/v2/advisory?status=Fixed` correctly filters by enum value
- [ ] `GET /api/v2/advisory/{id}` returns advisory details with status from enum column
- [ ] Response JSON shape is unchanged (status is a string, not an enum variant name)
- [ ] No references to `advisory_status` entity remain in endpoint files

## Test Requirements
- [ ] Verify `GET /api/v2/advisory` returns correct status values from enum column
- [ ] Verify status filtering with each valid enum value returns correct results
- [ ] Verify invalid status filter value returns an appropriate error response
- [ ] Verify response shape backward compatibility (no breaking changes to JSON structure)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256:d08114fb403008b05d010590b40b8edaa0b8f119b35c8f6dc918089a5e6191cb
