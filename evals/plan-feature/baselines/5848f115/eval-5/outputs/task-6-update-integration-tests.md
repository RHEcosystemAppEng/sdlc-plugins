## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to reflect the new schema. Test fixtures must create advisory rows with the `status` enum column instead of inserting into the `advisory_status` lookup table and setting `status_id`. Assertions must verify that status filtering works on the enum column and that the API response shape is unchanged (status is still a string in the JSON response).

## Files to Modify
- `tests/api/advisory.rs` — update test fixtures to insert advisories with `status` enum values instead of `status_id` FK references; update status-filter test cases to query by enum value; remove any test setup code that inserts into the `advisory_status` table; verify response shape remains unchanged

## Implementation Notes
- Follow the existing test patterns in `tests/api/sbom.rs` for test structure and assertion style (e.g., `assert_eq!(resp.status(), StatusCode::OK)` pattern).
- Test fixtures should create advisory records with each of the four enum values to verify round-trip serialization.
- Verify that the API response serializes the enum as a string matching the original lookup table values (e.g., `"Fixed"` not `"fixed"` or `"FIXED"`).
- Per the project's Key Conventions: integration tests use a real PostgreSQL test database. Ensure test setup runs the migration before inserting test data.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing integration test pattern showing fixture setup, HTTP request construction, and assertion style
- `tests/api/search.rs` — additional reference for endpoint testing patterns

## Acceptance Criteria
- [ ] All advisory integration tests pass with the new schema
- [ ] Tests verify status filtering with each of the four enum values
- [ ] Tests confirm the API response shape is unchanged (status as a string)
- [ ] No references to `advisory_status` table remain in test code
- [ ] Test fixtures create advisories using enum values directly

## Test Requirements
- [ ] Run the full advisory integration test suite and verify all tests pass
- [ ] Verify no test references the `advisory_status` table or `status_id` column

## Verification Commands
- `cargo test -p tests --test advisory` — all advisory tests pass
- `grep -r "advisory_status\|status_id" tests/api/advisory.rs` — returns no results

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoint queries
- Depends on: Task 5 — Update advisory ingestion pipeline
