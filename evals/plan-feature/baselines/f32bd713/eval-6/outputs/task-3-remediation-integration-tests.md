## Repository
trustify-backend

## Parent Epic
TC-9007 (TC-9006: trustify-backend)

## Target Branch
main

## Description
Add integration tests for the remediation tracking endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`). Tests verify correct aggregation behavior, pagination, empty state handling, and performance characteristics against a real PostgreSQL test database.

## Files to Create
- `tests/api/remediation.rs` -- integration tests for both remediation endpoints

## Files to Modify
- `tests/Cargo.toml` -- register the remediation test module if test module registration is required

## Implementation Notes
- Follow the existing integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`.
  Per CONVENTIONS.md section Testing: integration tests in tests/api/ hit a real PostgreSQL test database; use assert_eq!(resp.status(), StatusCode::OK) pattern.
  Applies: task creates `tests/api/remediation.rs` matching the convention's integration test file scope.
- Set up known vulnerability and SBOM data in the test database to verify aggregation correctness.
- Test the summary endpoint with:
  - Known data producing expected severity x status counts
  - Empty dataset (no vulnerabilities correlated)
- Test the by-product endpoint with:
  - Multiple products with known counts
  - Pagination parameters (offset, limit)
  - Empty dataset
- Use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions.
- Verify response body shapes match the documented API contracts.
- Include a test with a larger dataset to validate the p95 < 500ms performance target and the 10,000 vulnerability handling requirement.

## Reuse Candidates
- `tests/api/sbom.rs` -- SBOM endpoint integration test patterns (test setup, request construction, assertion style)
- `tests/api/advisory.rs` -- Advisory endpoint integration test patterns
- `tests/Cargo.toml` -- test dependency configuration pattern

## Acceptance Criteria
- [ ] Integration tests for `GET /api/v2/remediation/summary` pass with correct aggregation results
- [ ] Integration tests for `GET /api/v2/remediation/by-product` pass with correct per-product breakdown
- [ ] Empty state tests verify zero-count responses without errors
- [ ] Pagination tests verify offset/limit behavior for by-product endpoint
- [ ] All tests run successfully against a PostgreSQL test database
- [ ] Performance test validates response under 500ms with representative dataset

## Test Requirements
- [ ] Test summary endpoint returns correct counts grouped by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved) for known test data
- [ ] Test by-product endpoint returns correct per-product breakdown (total, open, in_progress, resolved) for known test data
- [ ] Test summary endpoint with no vulnerability data returns empty/zero-count result
- [ ] Test by-product endpoint pagination with offset=0, limit=10 returns correct page
- [ ] Test by-product endpoint with offset beyond total returns empty items list
- [ ] Test response time with dataset of 1,000+ vulnerabilities stays under performance target

## Verification Commands
- `cargo test -p trustify-tests -- api::remediation` -- run all remediation integration tests
- `cargo test -p trustify-tests -- api::remediation --nocapture` -- run with output for debugging

## Dependencies
- Depends on: Task 2 -- Add remediation summary and by-product endpoints
