## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add integration tests for the remediation REST endpoints (`GET /api/v2/remediation/summary`
and `GET /api/v2/remediation/by-product`). Tests run against a real PostgreSQL test database
following the existing integration test patterns in `tests/api/`.

## Files to Create
- `tests/api/remediation.rs` — integration tests for both remediation endpoints covering success responses, empty data, filtering, and pagination

## Files to Modify
- `tests/api/mod.rs` — add `mod remediation;` to register the new test module (if a module root exists)

## Implementation Notes
- Follow the established integration test pattern from existing tests. See `tests/api/sbom.rs` for the reference implementation.
  Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/remediation.rs` matching the convention's `.rs` test file scope.
- Tests should set up test data by ingesting sample SBOMs and advisories with known vulnerability/remediation states, then verify the aggregation endpoints return correct counts.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern consistently.
- Test pagination on the by-product endpoint: verify offset/limit parameters work correctly.
- Test edge cases: no data (empty database), single product, multiple products with mixed severity levels.
- Non-functional validation: while integration tests cannot enforce p95 latency, they should verify the summary endpoint responds within a reasonable timeframe for the test dataset.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for integration test structure, test data setup, and assertion patterns
- `tests/api/advisory.rs` — reference for advisory-related test data setup that feeds into remediation aggregation

## Acceptance Criteria
- [ ] Integration test verifies `GET /api/v2/remediation/summary` returns correct severity/status counts for known test data
- [ ] Integration test verifies `GET /api/v2/remediation/by-product` returns correct per-product breakdown for known test data
- [ ] Integration test verifies empty-data scenario returns zero counts (not errors)
- [ ] Integration test verifies by-product pagination (offset/limit parameters)
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Test `GET /api/v2/remediation/summary` with seeded SBOMs and advisories at mixed severity levels
- [ ] Test `GET /api/v2/remediation/by-product` with multiple products having different remediation states
- [ ] Test empty database returns `RemediationSummary` with all zero counts
- [ ] Test by-product endpoint pagination: request with limit=1 returns exactly 1 product
- [ ] Test response content types are `application/json`

## Verification Commands
- `cargo test -p trustify-tests -- api::remediation` — run all remediation integration tests
- `cargo test -p trustify-tests` — run full integration test suite to confirm no regressions

## Dependencies
- Depends on: Task 2 — Add remediation summary and by-product REST endpoints
