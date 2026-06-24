## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory REST endpoints to work with the new enum-based status column and update all advisory integration tests to verify the new behavior. The endpoints must continue to return the same JSON response shape (status as a string), and the status filter query parameter must work against the enum column. Integration tests must cover list, get, and filter-by-status scenarios without any reference to the dropped lookup table.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` — Update status filter parameter handling to use `AdvisoryStatusEnum` instead of joining `advisory_status`
- `modules/fundamental/src/advisory/endpoints/get.rs` — Update status field mapping if the endpoint constructs the response manually
- `modules/fundamental/src/advisory/endpoints/mod.rs` — Update route registration if any status-related routes change
- `tests/api/advisory.rs` — Rewrite integration tests to assert correct behavior with enum status; remove any test setup that creates `advisory_status` lookup rows; add test for status filter query parameter

## Implementation Notes
In `modules/fundamental/src/advisory/endpoints/list.rs`, the status filter query parameter (e.g., `?status=Fixed`) currently triggers a join-based filter. Replace this with a direct enum column filter:

```rust
if let Some(status) = &params.status {
    let status_enum = AdvisoryStatusEnum::try_from(status.as_str())
        .map_err(|_| AppError::BadRequest("Invalid status value".into()))?;
    query = query.filter(advisory::Column::Status.eq(status_enum));
}
```

Follow the error handling pattern in `common/src/error.rs` using `AppError` for invalid filter values. Follow the endpoint patterns in `modules/fundamental/src/sbom/endpoints/list.rs` for query parameter handling and response construction.

In `tests/api/advisory.rs`, follow the integration test patterns in `tests/api/sbom.rs`:
- Use `assert_eq!(resp.status(), StatusCode::OK)` for response validation.
- Test data setup should insert advisories with enum status values directly, not via the lookup table.

## Acceptance Criteria
- [ ] `GET /api/v2/advisory` returns advisory list with status as a string field (API shape unchanged)
- [ ] `GET /api/v2/advisory?status=Fixed` correctly filters by enum value
- [ ] `GET /api/v2/advisory/{id}` returns advisory details with status as a string field
- [ ] Invalid status filter value returns a 400 Bad Request error
- [ ] No endpoint code references `advisory_status` table or entity
- [ ] All advisory integration tests pass

## Test Requirements
- [ ] Integration test: list advisories returns status strings (New, Analyzing, Fixed, Rejected)
- [ ] Integration test: filter by valid status returns correct subset
- [ ] Integration test: filter by invalid status returns 400
- [ ] Integration test: get advisory by ID returns correct status string
- [ ] Integration test: advisory list with mixed statuses returns correct values after enum migration

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and model layer to use status enum

## Digest
[sdlc-workflow] Description digest: sha256-md:882cfb4f089148b065acbcf95af2b7a4b3ae905da65cbd7d668dfe6749e5d0c4
