## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for both remediation API endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`). Tests exercise the full HTTP stack against a real PostgreSQL test database, following the established integration test pattern in the repository.

## Files to Create
- `tests/api/remediation.rs` — integration tests for remediation summary and by-product endpoints

## Files to Modify
- `tests/api/mod.rs` — register `remediation` test module (if a mod.rs exists; otherwise ensure test discovery finds the new file)

## Implementation Notes
- Follow the existing integration test pattern: tests in `tests/api/` hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern. See `tests/api/sbom.rs` and `tests/api/advisory.rs` for established patterns.
  Per CONVENTIONS.md §Testing: integration tests in tests/api/ use real PostgreSQL and assert on StatusCode.
  Applies: task creates `tests/api/remediation.rs` matching the convention's test file scope.
- Test data setup: insert advisory and SBOM records with known severities and statuses into the test database before calling the endpoints, so the expected aggregation counts are deterministic.
- Test the summary endpoint with: (a) empty data returning zero counts, (b) known data returning correct severity x status breakdown, (c) large dataset (if performance NFR needs verification).
- Test the by-product endpoint with: (a) single product, (b) multiple products, (c) pagination parameters.
- Per docs/constraints.md §5.2: inspect code before modifying — read existing test patterns first.

## Reuse Candidates
- `tests/api/sbom.rs` — integration test pattern for SBOM endpoints; follow the same test setup, HTTP client initialization, and assertion patterns
- `tests/api/advisory.rs` — integration test pattern for advisory endpoints; reference for test data setup involving advisories with severity fields

## Acceptance Criteria
- [ ] Integration test for `GET /api/v2/remediation/summary` verifies correct aggregation counts with known test data
- [ ] Integration test for `GET /api/v2/remediation/by-product` verifies correct per-product breakdown
- [ ] Tests verify empty dataset returns valid (zero-count) responses
- [ ] Tests verify response status codes and JSON structure
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Test: summary endpoint returns correct severity x status matrix for seeded advisory data
- [ ] Test: by-product endpoint returns correct product-level counts for seeded SBOM-advisory relationships
- [ ] Test: both endpoints return 200 with valid JSON for empty datasets
- [ ] Test: by-product endpoint supports pagination parameters (offset, limit)

## Verification Commands
- `cargo test -p trustify-tests -- api::remediation` — all integration tests pass

## Dependencies
- Depends on: Task 2 — Add remediation summary and by-product API endpoints
