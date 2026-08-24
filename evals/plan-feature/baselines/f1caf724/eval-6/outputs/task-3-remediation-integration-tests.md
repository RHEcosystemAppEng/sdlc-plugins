## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add comprehensive integration tests for the remediation summary and by-product endpoints. Tests validate response shapes, aggregation accuracy, pagination behavior, empty-state handling, and performance characteristics (p95 < 500ms for datasets up to 10,000 vulnerabilities). Tests follow the established integration test pattern of hitting a real PostgreSQL test database.

## Files to Create
- `tests/api/remediation.rs` — integration tests for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs` — tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)`.
  Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/remediation.rs` matching the convention's integration test file scope.
- Set up test data by inserting SBOMs, advisories, and vulnerability associations into the test database before each test.
- Verify that the summary endpoint returns the correct severity x status matrix for known test data.
- Verify that the by-product endpoint returns accurate per-product breakdowns.
- Include edge case tests: no data, single product, multiple products with overlapping vulnerabilities.
- Performance test: verify response time with a moderately sized dataset to validate the p95 < 500ms NFR.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for integration test setup, database seeding, and assertion patterns
- `tests/api/advisory.rs` — reference for advisory-related test data seeding
- `common/src/model/paginated.rs::PaginatedResults` — expected response structure for by-product endpoint tests

## Acceptance Criteria
- [ ] Summary endpoint test validates response contains all four severity levels with correct counts
- [ ] Summary endpoint test validates correct status breakdown (Open, In Progress, Resolved) per severity
- [ ] By-product endpoint test validates per-product breakdown with multiple products
- [ ] By-product endpoint test validates pagination (offset/limit) works correctly
- [ ] Empty database test validates both endpoints return valid (empty/zero) responses without errors
- [ ] All tests pass in CI with `cargo test --test api remediation`

## Test Requirements
- [ ] Integration test for summary endpoint with known test data verifying exact count values
- [ ] Integration test for by-product endpoint with multi-product test data
- [ ] Integration test for by-product pagination with offset and limit parameters
- [ ] Integration test for empty state (no vulnerabilities ingested)
- [ ] Integration test for single-product scenario

## Verification Commands
- `cargo test --test api remediation` — verify all remediation integration tests pass
- `cargo test --test api` — verify no regressions in existing integration tests

## Dependencies
- Depends on: Task 1 — Add remediation module with summary aggregation endpoint
- Depends on: Task 2 — Add remediation by-product aggregation endpoint
