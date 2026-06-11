# Task 9 — Add integration tests for the SBOM comparison endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/compare` endpoint. The tests exercise the full request-response cycle against a real PostgreSQL test database, validating correct diff computation, error handling, and response format.

## Files to Create
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## Files to Modify
- `tests/api/mod.rs` or test harness entry point — Register the new test module (if the test framework requires explicit registration)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` — use `assert_eq!(resp.status(), StatusCode::OK)` pattern, set up test data in a real PostgreSQL test database.
- **Test data setup**: create two SBOMs with known package sets, advisory associations, and license data. Ensure the test data produces predictable diffs across all six categories.
- **Test scenarios to cover**:
  1. **Happy path**: two SBOMs with differences across all categories — verify each section contains expected entries.
  2. **Identical SBOMs**: compare an SBOM with itself — verify all diff lists are empty.
  3. **Missing left param**: `GET /api/v2/sbom/compare?right={id}` — verify 400 response.
  4. **Missing right param**: `GET /api/v2/sbom/compare?left={id}` — verify 400 response.
  5. **Non-existent SBOM**: provide a valid UUID that does not correspond to any SBOM — verify 404 response.
  6. **Version direction**: set up packages with version changes where one is an upgrade and one is a downgrade — verify `direction` field values.
  7. **Critical vulnerability**: include an advisory with critical severity — verify it appears in the `new_vulnerabilities` section with correct severity value.
- Use the existing test utilities and database setup helpers from the test infrastructure.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for SBOM endpoint integration test patterns, test data setup, and assertion style
- `tests/api/advisory.rs` — reference for advisory-related test data setup
- `tests/api/search.rs` — reference for query parameter handling in tests

## Acceptance Criteria
- [ ] All integration test scenarios pass against the test database
- [ ] Happy path test validates entries in all six diff categories
- [ ] Identical SBOMs test validates empty diff lists
- [ ] Error handling tests validate 400 and 404 responses
- [ ] Version direction test validates upgrade and downgrade detection
- [ ] Tests follow existing patterns in `tests/api/`

## Test Requirements
- [ ] Integration test: happy path with known diffs across all categories
- [ ] Integration test: identical SBOMs produce empty diff
- [ ] Integration test: missing query parameters return 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: version direction correctly identified
- [ ] Integration test: critical severity vulnerability appears with correct severity

## Verification Commands
- `cargo test --test api sbom_compare` — expected: all comparison tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add GET /api/v2/sbom/compare endpoint
