# Task 5 — Add remediation endpoint integration tests

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Add integration tests for the remediation aggregation endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`). Tests exercise the full request-response cycle against a real PostgreSQL test database, following the established integration test pattern in `tests/api/`.

## Files to Create
- `tests/api/remediation.rs` — Integration tests for both remediation endpoints covering normal aggregation, empty data, large dataset performance, and error conditions

## Files to Modify
- `tests/Cargo.toml` — Add any required test dependencies if not already present

## Implementation Notes
- Follow the integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test structure: set up test data, make HTTP requests, assert on status codes and response bodies.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in existing tests.
- Test scenarios for the summary endpoint:
  1. Normal case: seed advisories with mixed severity/status, verify aggregated counts are correct
  2. Empty case: no advisories exist, verify zero counts returned
  3. Large dataset: seed 10,000+ vulnerability records, verify response time is acceptable
- Test scenarios for the by-product endpoint:
  1. Normal case: seed multiple products with advisories, verify per-product breakdown
  2. Pagination: verify offset/limit query parameters work correctly
  3. Single product: verify correct counts for a single product with multiple advisories
- Per Key Conventions (Testing): integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/remediation.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration test pattern (setup, request, assertion structure)
- `tests/api/advisory.rs` — Advisory endpoint integration test pattern with severity-related assertions
- `tests/api/search.rs` — Search endpoint tests showing query parameter testing patterns

## Acceptance Criteria
- [ ] Integration tests for `GET /api/v2/remediation/summary` pass with correct aggregation results
- [ ] Integration tests for `GET /api/v2/remediation/by-product` pass with correct per-product breakdown
- [ ] Empty data case returns zero counts without errors
- [ ] Pagination on the by-product endpoint works correctly with offset/limit parameters
- [ ] Tests follow the existing integration test pattern in `tests/api/`

## Test Requirements
- [ ] Test: summary endpoint returns correct severity x status counts with seeded test data
- [ ] Test: summary endpoint returns zero counts when no advisory data exists
- [ ] Test: by-product endpoint returns correct per-product counts with multiple products
- [ ] Test: by-product endpoint pagination returns correct subsets
- [ ] Test: both endpoints return 200 status code on success
- [ ] Performance test: summary endpoint responds within acceptable time with 10,000 vulnerability records

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 4 — Add remediation summary and by-product endpoints

## Parent Epic
TC-9006: trustify-backend
