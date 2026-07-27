# Task 4: Add remediation endpoint integration tests

**Epic:** TC-9006: trustify-backend

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Add comprehensive integration tests for both remediation endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`). Tests must cover the aggregation logic, edge cases, and performance requirements. Tests should follow the existing integration test patterns in `tests/api/` and use a real PostgreSQL test database.

## Files to Create
- `tests/api/remediation.rs` — integration tests for both remediation endpoints

## Files to Modify
- `tests/api/mod.rs` — add `mod remediation;` to include the new test module (if a module root exists)

## Implementation Notes
- Follow the existing integration test patterns from `tests/api/sbom.rs` and `tests/api/advisory.rs`.
- Tests must hit a real PostgreSQL test database, consistent with the project's testing convention.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in existing tests.
- Set up test data by inserting advisories with known severity values and SBOM relationships via the existing entity layer, then verify that the aggregation endpoints return the expected counts.
- Include a performance-oriented test that inserts up to 10,000 vulnerability records and verifies the summary endpoint responds within acceptable time bounds (p95 < 500ms per the non-functional requirements).
- Test edge cases: empty database, single product with all statuses, multiple products with overlapping vulnerabilities.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests; reference for test setup patterns, database seeding, and assertion style
- `tests/api/advisory.rs` — Advisory endpoint integration tests; reference for advisory-related test data setup
- `entity/src/advisory.rs` — Advisory entity for seeding test data with severity values
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join entity for creating relationships in test data

## Acceptance Criteria
- [ ] Integration tests pass for `GET /api/v2/remediation/summary` with various data scenarios
- [ ] Integration tests pass for `GET /api/v2/remediation/by-product` with various data scenarios
- [ ] Edge cases are covered: empty database, single product, multiple products
- [ ] Performance test validates p95 < 500ms with up to 10,000 vulnerability records
- [ ] All tests follow existing test patterns in the repository

## Test Requirements
- [ ] Summary endpoint returns correct counts for a known set of advisories with mixed severity and status
- [ ] By-product endpoint returns correct per-product breakdown with known SBOM-advisory relationships
- [ ] Empty database scenario returns zero counts (summary) and empty list (by-product)
- [ ] Pagination on by-product endpoint works correctly
- [ ] Response status codes are verified for success and error cases

## Verification Commands
- `cargo test --test api remediation` — run all remediation integration tests
- `cargo test --test api` — run full integration test suite to verify no regressions

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 2 — Add remediation summary endpoint
- Depends on: Task 3 — Add remediation by-product endpoint
