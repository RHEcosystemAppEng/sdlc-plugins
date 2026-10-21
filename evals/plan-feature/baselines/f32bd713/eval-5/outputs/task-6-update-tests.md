## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new schema. The tests in `tests/api/advisory.rs` currently test advisory queries that join the `advisory_status` lookup table. After the migration, these tests must verify that advisory queries use the `status` enum column directly, that status filtering works correctly with enum values, and that the API response shape remains unchanged.

## Files to Modify
- `tests/api/advisory.rs` — update test setup to insert advisories with enum `status` values instead of FK references to `advisory_status`; update assertions to verify enum-based filtering; add tests for each of the four status values; remove any test setup that creates `advisory_status` rows

## Implementation Notes
- Update test data setup: instead of inserting rows into `advisory_status` and setting `status_id` on advisory rows, set the `status` column directly to `AdvisoryStatusEnum` values.
- Update filter tests: verify that `GET /api/v2/advisory?status=Fixed` returns only advisories with `status = 'Fixed'` enum value.
- Verify backward compatibility: the JSON response should still contain `"status": "Fixed"` as a string — the internal representation changed but the API contract is unchanged.
- Add a test for each status value to ensure all four enum values work correctly.
- Per repo Key Conventions §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's integration test file scope.
- Reference `tests/api/sbom.rs` for the established integration test pattern (setup, request, assert).

## Reuse Candidates
- `tests/api/sbom.rs` — existing integration tests demonstrating the test setup, HTTP request, and assertion patterns
- `tests/api/search.rs` — another integration test example showing query parameter testing patterns

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new enum schema
- [ ] Test data setup uses `AdvisoryStatusEnum` values instead of `advisory_status` FK references
- [ ] Tests cover filtering by each of the four status values (New, Analyzing, Fixed, Rejected)
- [ ] Tests verify the API response shape is unchanged (status as string)
- [ ] No references to `advisory_status` table or `status_id` column remain in test code

## Test Requirements
- [ ] `GET /api/v2/advisory` returns advisories with status as a string in the response
- [ ] `GET /api/v2/advisory?status=Fixed` returns only Fixed advisories
- [ ] `GET /api/v2/advisory?status=New` returns only New advisories
- [ ] `GET /api/v2/advisory/{id}` returns the correct enum status for a specific advisory
- [ ] Test database setup correctly creates advisories with enum status values

## Verification Commands
- `cargo test -p tests --test advisory` — advisory integration tests pass
- `cargo test` — full test suite passes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoint queries to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
