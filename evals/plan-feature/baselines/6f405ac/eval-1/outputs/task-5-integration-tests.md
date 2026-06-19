## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests verify the happy path (correct severity counts), 404 for non-existent SBOMs, advisory deduplication, and the optional threshold query parameter. All tests follow the existing integration test patterns in `tests/api/`.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — Integration tests for the advisory-summary endpoint covering all acceptance scenarios

## Files to Modify
- `tests/Cargo.toml` — Add any necessary test dependencies if not already present (e.g., test fixtures for advisory-SBOM correlation)

## Implementation Notes
Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions.

Test setup should:
1. Create an SBOM in the test database
2. Create advisories with known severity levels (e.g., 2 critical, 3 high, 1 medium, 1 low)
3. Link advisories to the SBOM via the `sbom_advisory` join table
4. Call the endpoint and verify the response

For the deduplication test, link the same advisory to an SBOM twice and verify it is only counted once.

For the threshold test, use `?threshold=high` and verify only critical and high counts are returned.

Per CONVENTIONS.md §Testing: use integration tests in `tests/api/` hitting a real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's `.rs` test file scope.

Per CONVENTIONS.md §Error handling: verify that error responses use the `AppError` format and return appropriate status codes.
Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's `.rs` Rust scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration tests; follow test setup patterns, database fixtures, and assertion style
- `tests/api/advisory.rs` — Existing advisory integration tests; follow patterns for creating advisory test fixtures
- `common/src/error.rs::AppError` — Error response format to verify in error test cases

## Acceptance Criteria
- [ ] Test for happy path: SBOM with known advisories returns correct severity counts
- [ ] Test for 404: non-existent SBOM ID returns 404 status
- [ ] Test for deduplication: same advisory linked multiple times is counted once
- [ ] Test for threshold filter: `?threshold=critical` returns only critical count, `?threshold=high` returns critical and high counts
- [ ] Test for empty: SBOM with no advisories returns all zeros
- [ ] All tests pass against a PostgreSQL test database

## Test Requirements
- [ ] `test_advisory_summary_happy_path` — Create SBOM with advisories at each severity, verify counts match
- [ ] `test_advisory_summary_not_found` — Request summary for non-existent SBOM, verify 404 response
- [ ] `test_advisory_summary_deduplication` — Link same advisory twice, verify counted once
- [ ] `test_advisory_summary_threshold_critical` — Use `?threshold=critical`, verify only critical returned
- [ ] `test_advisory_summary_threshold_high` — Use `?threshold=high`, verify critical and high returned
- [ ] `test_advisory_summary_empty_sbom` — SBOM with no linked advisories returns all zero counts

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (requires the endpoint to be implemented and routes registered)
