## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory integration tests to verify the new enum-based status behavior. The tests must confirm that advisory list and get endpoints return correct status values from the enum column, that status filtering works with enum values, and that no references to the dropped `advisory_status` lookup table remain in test fixtures or assertions.

## Files to Modify
- `tests/api/advisory.rs` — update existing test cases to use enum status values instead of lookup table IDs; update test fixtures to insert advisories with `status` enum values; update assertions to verify status is returned as a string in the API response; add test cases for filtering by each enum value

## Implementation Notes
The existing tests in `tests/api/advisory.rs` likely set up test data by inserting rows into both the `advisory` and `advisory_status` tables. Update these to insert only into the `advisory` table with the `status` enum column.

Follow the existing integration test pattern in `tests/api/advisory.rs`:
- Use the test database setup utilities already established in the test suite
- Use `assert_eq!(resp.status(), StatusCode::OK)` for response status checks
- Insert test advisory data with enum status values

Test scenarios to cover:
1. List advisories — verify status field is present and correct in each item
2. Get single advisory — verify status field is correct
3. Filter by status = "Fixed" — verify only matching advisories returned
4. Filter by status = "New" — verify only matching advisories returned
5. Verify the response shape is unchanged (status is a string, not an integer)

Remove any test code that references the `advisory_status` table, `status_id` column, or advisory status lookup table fixtures.

Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/advisory.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — demonstrates the integration test pattern with test database setup, request building, and response assertion that this task should follow
- `tests/api/advisory.rs` — the existing advisory tests provide the baseline pattern to adapt

## Acceptance Criteria
- [ ] All existing advisory integration tests pass with the new enum schema
- [ ] Test data setup uses enum status values directly (no lookup table inserts)
- [ ] At least one test verifies status filtering with the enum column
- [ ] No references to `advisory_status` table or `status_id` remain in test code
- [ ] The API response shape for status is unchanged (string value, not integer)
- [ ] Tests pass with `cargo test --test api` (or equivalent test runner command)

## Test Requirements
- [ ] Verify advisory list returns correct status strings from enum values
- [ ] Verify advisory get returns correct status string from enum value
- [ ] Verify filtering by each enum value (New, Analyzing, Fixed, Rejected) returns only matching advisories
- [ ] Verify the full test suite passes (`cargo test`)

## Verification Commands
- `cargo test --test api` — all integration tests pass
- `grep -r "advisory_status" tests/` — returns no matches

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and endpoints to use enum column
- Depends on: Task 5 — Update advisory ingestion pipeline for enum values
