# Task 5 — Update advisory endpoints to use enum status filtering

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory REST API endpoints to use the new enum-based status filtering. The endpoint handlers in the advisory module must pass status filter parameters as enum values to the updated service layer instead of string-to-ID lookups via the advisory_status table. The API response shape remains identical to maintain backward compatibility.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` — update the list endpoint handler to parse status query parameters as `AdvisoryStatusEnum` values and pass them to the updated `AdvisoryService::list` method; remove any status ID resolution logic that previously looked up IDs in the `advisory_status` table
- `modules/fundamental/src/advisory/endpoints/get.rs` — update the get endpoint to use the status field from the advisory entity's enum column; no join needed
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if any query parameter types change for status filtering

## Implementation Notes
- The list endpoint likely accepts a `status` query parameter as a string. Parse it directly to `AdvisoryStatusEnum` using SeaORM's enum parsing. Return a 400 Bad Request if the string does not match a valid enum variant
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` for query parameter handling and response wrapping with `PaginatedResults<T>`
- The response type (`AdvisorySummary`) already exposes status as a string after the model update in Task 4, so no serialization changes are needed in the endpoint layer
- Maintain `.context()` error wrapping on all handler methods per the project's `AppError` pattern in `common/src/error.rs`
- The query builder helpers in `common/src/db/query.rs` handle pagination and sorting — reuse them

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference endpoint pattern for list handler with query parameters, pagination, and response wrapping
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference endpoint pattern for get-by-ID handler
- `common/src/db/query.rs` — shared filtering, pagination, and sorting helpers
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper

## Acceptance Criteria
- [ ] `GET /api/v2/advisory` returns advisories with status from the enum column
- [ ] `GET /api/v2/advisory?status=Fixed` filters correctly using the enum value
- [ ] `GET /api/v2/advisory/{id}` returns advisory details with status from the enum column
- [ ] Invalid status filter values return a 400 Bad Request response
- [ ] Response shape is unchanged from the current API contract

## Test Requirements
- [ ] List endpoint returns correct status values from enum column
- [ ] Status filter query parameter works for all four valid values
- [ ] Invalid status filter value returns 400
- [ ] Get endpoint returns correct status for a specific advisory

## Verification Commands
- `cargo check -p fundamental` — endpoint module compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and models to use enum status column
