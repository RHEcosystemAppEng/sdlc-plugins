# Task 5 — Add integration tests for advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should cover the full request-response cycle against a real PostgreSQL test database, validating correct severity aggregation, 404 behavior, threshold filtering, and response shape. These tests serve as the primary verification that the endpoint behaves correctly end-to-end.

## Files to Create
- `tests/api/advisory_summary.rs` — integration test module with test cases for the advisory-summary endpoint

## Files to Modify
- `tests/api/mod.rs` — add `mod advisory_summary;` to register the new test module (if a test module registry exists; otherwise the test runner discovers files automatically)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status verification.
  Applies: task creates `tests/api/advisory_summary.rs` matching the convention's Rust integration test scope.
- Test setup: create test SBOM(s) and link advisories with known severity levels. Use the existing test fixtures/helpers from the `tests/` crate for database setup and teardown.
- Verify JSON response shape: deserialize the response body into `AdvisorySeveritySummary` and assert field values match expected counts.
- The test for 404 should use a UUID that does not correspond to any ingested SBOM.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests; demonstrates test setup, HTTP client usage, database fixture creation, and status assertion patterns
- `tests/api/advisory.rs` — existing advisory integration tests; demonstrates how to create advisory test fixtures with specific severity levels

## Acceptance Criteria
- [ ] Integration test covers: valid SBOM returns 200 with correct severity counts
- [ ] Integration test covers: nonexistent SBOM returns 404
- [ ] Integration test covers: SBOM with no advisories returns all-zero counts
- [ ] Integration test covers: deduplication of advisories linked through multiple paths
- [ ] Integration test covers: threshold parameter filtering
- [ ] Integration test covers: invalid threshold value returns 400
- [ ] All tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Test: `test_advisory_summary_success` — create SBOM with 2 critical, 3 high, 1 medium, 0 low advisories; assert response `{ critical: 2, high: 3, medium: 1, low: 0, total: 6 }`
- [ ] Test: `test_advisory_summary_not_found` — request summary for nonexistent UUID; assert 404
- [ ] Test: `test_advisory_summary_empty` — create SBOM with no advisories; assert all-zero counts
- [ ] Test: `test_advisory_summary_deduplication` — link same advisory to SBOM through multiple paths; assert count is 1 not N
- [ ] Test: `test_advisory_summary_threshold_critical` — assert only critical count is non-zero when `?threshold=critical`
- [ ] Test: `test_advisory_summary_threshold_high` — assert critical and high counts are non-zero when `?threshold=high`
- [ ] Test: `test_advisory_summary_invalid_threshold` — assert 400 for `?threshold=unknown`

## Verification Commands
- `cargo test --test api -- advisory_summary` — all integration tests pass

## Dependencies
- Depends on: Task 3 — Add threshold query parameter to advisory-summary endpoint
- Depends on: Task 4 — Add cache invalidation for advisory-summary on advisory ingestion
