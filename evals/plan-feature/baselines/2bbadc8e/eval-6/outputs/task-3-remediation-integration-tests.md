## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the remediation API endpoints. These tests verify that the summary and by-product endpoints correctly aggregate vulnerability data from the existing database, handle edge cases (empty data, large datasets), and meet the performance requirements specified in the feature.

## Files to Create
- `tests/api/remediation.rs` — integration tests for GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product

## Files to Modify
- `tests/Cargo.toml` — add test dependencies if needed for the new test module

## Implementation Notes
Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Follow the established patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`.
Applies: task creates `tests/api/remediation.rs` matching the convention's `.rs` test file scope.

Seed the test database with known vulnerability and SBOM data to produce deterministic aggregation results. Verify that:
- The summary endpoint returns the expected severity x status matrix for the seeded data
- The by-product endpoint returns correct per-product counts
- Empty database returns zero counts (not errors)
- Pagination works correctly for the by-product endpoint

Reference `tests/api/sbom.rs` for the test setup pattern including database seeding and HTTP client initialization.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for integration test structure, database seeding, and HTTP client setup
- `tests/api/advisory.rs` — reference for advisory-related test fixtures that can be reused for remediation test data
- `tests/api/search.rs` — reference for search test patterns

## Acceptance Criteria
- [ ] Integration tests cover GET /api/v2/remediation/summary with seeded data
- [ ] Integration tests cover GET /api/v2/remediation/by-product with seeded data
- [ ] Tests verify correct aggregation counts match seeded data
- [ ] Tests verify empty database returns zero counts
- [ ] Tests verify by-product pagination (offset, limit)
- [ ] All integration tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Test summary endpoint returns correct severity x status matrix with seeded vulnerability data
- [ ] Test by-product endpoint returns correct per-product totals with seeded data across multiple products
- [ ] Test summary endpoint with no vulnerability data returns all-zero counts
- [ ] Test by-product endpoint pagination returns correct subsets and total count
- [ ] Test both endpoints return proper error codes for invalid query parameters

## Dependencies
- Depends on: Task 2 — Add remediation API endpoints
