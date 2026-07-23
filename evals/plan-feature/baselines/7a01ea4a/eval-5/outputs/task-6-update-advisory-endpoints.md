## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory list and get endpoints to use the new `status` enum column for filtering and response construction. The advisory list endpoint (`GET /api/v2/advisory`) should accept status filter parameters that compare against the enum column directly rather than joining the `advisory_status` table. The get endpoint (`GET /api/v2/advisory/{id}`) should return the status from the enum column. The API response shape must remain identical -- status is still returned as a string.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` -- update the status filter parameter handling to use the enum column; remove any `advisory_status` join logic in the query construction
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update the detail response to source status from the enum column
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- remove any route-level `advisory_status` references; verify route registration is unchanged

## Implementation Notes
- The list endpoint likely accepts a `status` query parameter for filtering. Update the filter to compare against `advisory::Column::Status` using SeaORM enum matching instead of joining `advisory_status`.
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` for reference on query parameter filtering with direct column comparison.
- All handlers return `Result<T, AppError>` with `.context()` wrapping -- maintain this pattern.
- List endpoints return `PaginatedResults<AdvisorySummary>` -- this wrapper is unchanged.
- No user-facing API changes: the response shape remains identical (status is still a string field). Verify this by checking that the JSON serialization of `AdvisorySummary` and `AdvisoryDetails` produces the same output.
- Per docs/constraints.md section 2 (Commit Rules): commit messages must follow Conventional Commits format, reference TC-9005 in the footer, and include the `--trailer="Assisted-by: Claude Code"`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference for endpoint filtering patterns with direct column queries
- `modules/fundamental/src/advisory/service/advisory.rs` -- the updated service layer (Task 5) that the endpoints call

## Acceptance Criteria
- [ ] `GET /api/v2/advisory` with status filter queries the enum column directly (no join)
- [ ] `GET /api/v2/advisory/{id}` returns status from the enum column
- [ ] API response shape is unchanged -- status field is still a string
- [ ] No remaining references to `advisory_status` in the endpoint layer

## Test Requirements
- [ ] Verify `GET /api/v2/advisory?status=Fixed` returns only advisories with Fixed status
- [ ] Verify `GET /api/v2/advisory/{id}` returns correct status string
- [ ] Verify response JSON schema matches the previous format exactly

## Verification Commands
- `cargo check -p fundamental` -- fundamental module compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 5 -- Update AdvisoryService
