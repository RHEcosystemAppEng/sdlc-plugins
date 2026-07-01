## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory REST endpoints to use the new `AdvisoryStatusEnum` type for status filtering and response serialization. The list endpoint's status query parameter must accept enum string values instead of integer IDs, and the get endpoint must return the enum-serialized status. The external API response shape must remain identical — status is still a string field in JSON.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` — update the status filter query parameter type from integer to `AdvisoryStatusEnum` (or string that maps to the enum); adjust query builder call to pass the enum value to the service layer
- `modules/fundamental/src/advisory/endpoints/get.rs` — update response construction if it explicitly maps status from a join result; with the model change, this may only require import updates
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update imports if the route registration references status-related query parameter types

## Implementation Notes
- The list endpoint likely has a query parameter struct (e.g., `ListQuery` or `AdvisoryFilter`) with a `status` or `status_id` field — change this to accept `AdvisoryStatusEnum` (SeaORM enum types implement `FromStr` and `Deserialize` when properly derived)
- If the filter parameter currently accepts an integer, change it to accept a string matching the enum values: "New", "Analyzing", "Fixed", "Rejected"
- Follow the existing endpoint patterns in `modules/fundamental/src/sbom/endpoints/list.rs` for query parameter handling and response construction
- The response body does not change shape — `AdvisoryStatusEnum` serializes to the same string values that were previously returned from the lookup table join
- Error handling should follow the `Result<T, AppError>` pattern with `.context()` wrapping per project conventions

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for Axum query parameter extraction, pagination, and `PaginatedResults<T>` response pattern
- `modules/fundamental/src/advisory/endpoints/list.rs` — current implementation to understand existing query parameter struct and filter logic before modifying

## Acceptance Criteria
- [ ] `GET /api/v2/advisory?status=Fixed` returns only advisories with status Fixed
- [ ] `GET /api/v2/advisory?status=New` returns only advisories with status New
- [ ] `GET /api/v2/advisory` (no filter) returns all advisories with status as a string field
- [ ] `GET /api/v2/advisory/{id}` returns advisory details with status as a string field
- [ ] API response JSON shape is identical to pre-migration format (no breaking changes)
- [ ] Invalid status filter values return an appropriate error response

## Test Requirements
- [ ] Integration test: `GET /api/v2/advisory?status=Fixed` returns 200 with only Fixed advisories
- [ ] Integration test: `GET /api/v2/advisory?status=InvalidValue` returns 400 or appropriate error
- [ ] Integration test: `GET /api/v2/advisory/{id}` returns 200 with status as string in response body

## Verification Commands
- `cargo test -p tests --test advisory` — advisory integration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and models
