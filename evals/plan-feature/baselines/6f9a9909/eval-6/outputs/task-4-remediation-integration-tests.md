## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the remediation summary and by-product endpoints. Tests hit a real PostgreSQL test database following the established integration test pattern in `tests/api/`. Cover both endpoints with positive, empty-data, and filtering scenarios to ensure correctness before frontend integration.

## Files to Create
- `tests/api/remediation.rs` -- integration tests for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`

## Files to Modify
- `tests/Cargo.toml` -- add remediation test module to the test suite if needed

## Implementation Notes
Per CONVENTIONS.md "Testing": integration tests in `tests/api/` hit a real PostgreSQL test database. Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established by existing tests. See `tests/api/sbom.rs` and `tests/api/advisory.rs` for reference implementations.
Applies: task creates `tests/api/remediation.rs` matching the convention's `.rs` test file scope.

The tests should seed the test database with known vulnerability, SBOM, and advisory data, then verify the aggregation endpoints return correct counts. Use the same test setup patterns as existing endpoint tests.

Relevant constraints from `docs/constraints.md`:
- Per SS5.2: Inspect existing test code before writing new tests.
- Per SS5.4: Reuse existing test infrastructure and helpers.

## Reuse Candidates
- `tests/api/sbom.rs` -- reference implementation for endpoint integration test structure and assertions
- `tests/api/advisory.rs` -- reference implementation for advisory-related test data seeding
- `tests/api/search.rs` -- reference implementation for search endpoint testing patterns

## Acceptance Criteria
- [ ] Integration test verifies `GET /api/v2/remediation/summary` returns correct aggregated counts for seeded test data
- [ ] Integration test verifies `GET /api/v2/remediation/by-product` returns correct per-product breakdown for seeded test data
- [ ] Test covers empty dataset scenario (no vulnerabilities) for both endpoints
- [ ] Test covers multi-product scenario with different remediation statuses
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Test `GET /api/v2/remediation/summary` with seeded data: verify severity x status counts match expected values
- [ ] Test `GET /api/v2/remediation/summary` with empty data: verify zero counts returned
- [ ] Test `GET /api/v2/remediation/by-product` with seeded data: verify per-product totals match expected values
- [ ] Test `GET /api/v2/remediation/by-product` pagination: verify offset/limit parameters work correctly
- [ ] Test `GET /api/v2/remediation/by-product` with empty data: verify empty list returned

## Verification Commands
- `cargo test --test api remediation` -- runs the remediation integration test suite
- `cargo test --test api` -- runs all integration tests to verify no regressions

## Dependencies
- Depends on: Task 2 -- Add remediation summary endpoint
- Depends on: Task 3 -- Add remediation by-product endpoint

## Parent Epic
TC-9007
