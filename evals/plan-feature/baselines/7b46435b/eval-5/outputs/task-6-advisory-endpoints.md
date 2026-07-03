# Task 6 — Update advisory endpoints for enum status filtering

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory list and get endpoints to work with the enum status column. Ensure that status filtering in the list endpoint uses the enum values directly, and that the get endpoint returns the status from the advisory entity's enum field. The API response shape must remain identical — status is still serialized as a string. No external API changes are needed.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter parameter handling to parse into `AdvisoryStatusEnum` values; remove any `advisory_status` join in the query construction
- `modules/fundamental/src/advisory/endpoints/get.rs` — update status retrieval to use advisory entity's enum field directly
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if status filter parameter types change

## Implementation Notes
- The list endpoint's status filter query parameter likely accepts a string and resolves it via the `advisory_status` table — change it to parse the string into an `AdvisoryStatusEnum` variant and pass to the service layer for direct column filtering
- All handlers return `Result<T, AppError>` with `.context()` wrapping per project convention
- List endpoints return `PaginatedResults<AdvisorySummary>` — the response type is unchanged
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` for query parameter handling and response construction
- Invalid status filter values (strings not matching any enum variant) should return a 400 Bad Request via `AppError`
- Cache behavior should be unchanged — `tower-http` caching middleware configuration does not need modification since the response shape is identical

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference endpoint pattern for Axum query parameter handling and response construction
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper
- `common/src/error.rs` — `AppError` enum for error handling and invalid-input responses

## Acceptance Criteria
- [ ] `GET /api/v2/advisory` with status filter returns correctly filtered results using enum values
- [ ] `GET /api/v2/advisory/{id}` returns advisory with correct status string from enum column
- [ ] API response shape is unchanged — status is still a string in the JSON response
- [ ] Invalid status filter values return appropriate 400 error responses
- [ ] No references to `advisory_status` table remain in the endpoints layer

## Test Requirements
- [ ] Verify endpoints compile: `cargo check -p fundamental`
- [ ] Verify list endpoint with each valid status filter value (New, Analyzing, Fixed, Rejected) returns correct results
- [ ] Verify list endpoint with no status filter returns all advisories with correct status values
- [ ] Verify get endpoint returns advisory with status from enum column

## Verification Commands
- `cargo check -p fundamental` — fundamental module compiles
- `cargo test -p fundamental` — fundamental module tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 5 — Update advisory service to eliminate status table join
