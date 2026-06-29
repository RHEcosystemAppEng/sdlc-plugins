# Task 5 -- Update advisory endpoints for enum status column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory HTTP endpoints (list and get) to filter by the `advisory.status` enum column instead of joining the `advisory_status` lookup table. The list endpoint must support status filtering via query parameters using enum string values (e.g., `?status=Fixed`). The get endpoint must return the status enum value directly.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` -- update status filter parameter handling to compare against enum values instead of joined table values
- `modules/fundamental/src/advisory/endpoints/get.rs` -- update single advisory fetch to use the enum column directly
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- update route registration if filter parameter types change

## Implementation Notes
- In the list endpoint, update the status query parameter deserialization to accept enum string values ("New", "Analyzing", "Fixed", "Rejected") and convert them to `AdvisoryStatusEnum` variants for filtering.
- For filtering, use `advisory::Column::Status.eq(status_param)` instead of joining and filtering on the lookup table.
- The API response shape must remain unchanged -- status is serialized as a string by serde via the `string_value` attributes on `AdvisoryStatusEnum`. No explicit transformation is needed.
- Follow the existing endpoint patterns in `modules/fundamental/src/sbom/endpoints/list.rs` for how list endpoints handle query parameter filtering.
- The `PaginatedResults<AdvisorySummary>` return type in the list endpoint should work unchanged since the model struct update (Task 4) handles the type change.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference endpoint pattern for list operations with query parameter filtering
- `modules/fundamental/src/advisory/endpoints/list.rs` -- existing advisory list endpoint to modify in-place

## Acceptance Criteria
- [ ] Advisory list endpoint correctly filters by enum status values via query parameter
- [ ] Advisory get endpoint returns the correct status value from the enum column
- [ ] API response shape remains unchanged (status is a string field)
- [ ] No endpoint code references the `advisory_status` join
- [ ] All advisory endpoints compile and serve requests successfully

## Test Requirements
- [ ] Verify advisory list endpoint returns correct results with status filter applied (e.g., `?status=Fixed`)
- [ ] Verify advisory get endpoint returns the correct status value
- [ ] Verify invalid status filter values produce an appropriate error response

## Verification Commands
- `cargo check -p fundamental` -- module compiles without errors
- `cargo test -p fundamental -- advisory` -- advisory-related tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 4 -- Update advisory service and query layer for enum status
