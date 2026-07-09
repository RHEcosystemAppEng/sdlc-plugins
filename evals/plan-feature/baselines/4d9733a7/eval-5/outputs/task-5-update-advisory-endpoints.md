## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory REST endpoints to use the new enum-based status filtering instead of the join-based approach. The endpoints must continue to accept the same query parameters and return the same response shape — the change is internal to how status filtering is implemented.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter query parameter handling to pass enum values to the service layer instead of string-based FK lookups
- `modules/fundamental/src/advisory/endpoints/get.rs` — update any status-related response construction to use the enum-based status from the advisory entity
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if any status-related query parameter types or extractors change

## Implementation Notes
- The list endpoint's status filter query parameter should continue to accept string values (e.g., `?status=Fixed`) but convert them to `AdvisoryStatusEnum` variants before passing to the service layer. Use `AdvisoryStatusEnum::from_str()` or a similar conversion.
- Ensure error handling for invalid status filter values returns a clear 400 Bad Request with a message listing valid values.
- Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for all endpoint handlers.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md §Endpoint Registration: follow the existing pattern in `endpoints/mod.rs` for route registration.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Response Types: list endpoint must continue to return `PaginatedResults<AdvisorySummary>`.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's Rust endpoint file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for list endpoint patterns with query parameter extraction and PaginatedResults response
- `modules/fundamental/src/advisory/endpoints/list.rs` — existing advisory list endpoint; modify in place
- `common/src/error.rs` — `AppError` for consistent error responses on invalid filter values

## Acceptance Criteria
- [ ] `GET /api/v2/advisory` returns advisory list with status as a string field (unchanged API response)
- [ ] `GET /api/v2/advisory?status=Fixed` correctly filters by the enum status value
- [ ] `GET /api/v2/advisory/{id}` returns advisory details with status as a string field (unchanged API response)
- [ ] Invalid status filter values return 400 Bad Request with descriptive error message
- [ ] No joins to `advisory_status` table remain in endpoint handler code

## Test Requirements
- [ ] Verify list endpoint returns advisories with correct status strings
- [ ] Verify status filter query parameter works for all four enum values
- [ ] Verify invalid status filter value returns 400 error
- [ ] Verify detail endpoint returns advisory with correct status string

## Verification Commands
- `cargo check -p trustify-fundamental` — verify the module compiles
- `cargo test -p trustify-fundamental -- advisory` — run advisory-related tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and model layer to use enum status
