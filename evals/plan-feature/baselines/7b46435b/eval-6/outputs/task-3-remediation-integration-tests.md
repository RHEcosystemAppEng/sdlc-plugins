## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the remediation summary and by-product endpoints. Tests follow the existing integration test pattern in `tests/api/` using a real PostgreSQL test database. The tests verify response shapes, aggregation correctness, edge cases (empty data, single product, fully resolved vulnerabilities), and pagination behavior.

## Files to Create
- `tests/api/remediation.rs` -- integration tests for both remediation endpoints

## Files to Modify
- `tests/Cargo.toml` -- register remediation test module if module declaration is needed

## Implementation Notes
- Follow the testing pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`: tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
  Per CONVENTIONS.md section "Testing": integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/remediation.rs` matching the convention's `.rs` test file scope.

- Set up test data by ingesting SBOMs and advisories with known severity and status values via the existing ingestion infrastructure, then assert that the aggregation endpoints return the expected counts.

- Test edge cases: empty database (should return zero counts, not errors), single product, products with all vulnerabilities resolved, mixed severity distributions across multiple products.

- Test pagination behavior for the by-product endpoint: verify limit and offset parameters produce correct result windows and that total count remains consistent across pages.

- Performance: while integration tests cannot enforce the p95 < 500ms NFR directly, include a test that aggregates across a moderate dataset (hundreds of entries) to catch obvious performance regressions.

## Reuse Candidates
- `tests/api/sbom.rs` -- reference integration test patterns for endpoint testing with test database setup
- `tests/api/advisory.rs` -- reference integration test showing advisory data seeding and assertion patterns

## Acceptance Criteria
- [ ] Integration tests cover `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`
- [ ] Tests verify HTTP 200 status codes and response shapes
- [ ] Tests verify aggregation correctness with known seeded test data
- [ ] Tests cover edge cases: empty database, single product, fully resolved vulnerabilities
- [ ] Tests verify pagination behavior (limit, offset, total count)
- [ ] All tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Test: summary endpoint returns correct severity x status breakdown matching seeded data
- [ ] Test: summary endpoint totals equal the sum of individual severity-status counts
- [ ] Test: by-product endpoint returns correct per-product breakdown
- [ ] Test: by-product pagination works correctly with limit and offset parameters
- [ ] Test: both endpoints return 200 with zero counts on empty database (not 404 or 500)
- [ ] Test: summary counts update correctly after ingesting additional advisories

## Verification Commands
- `cargo test --test remediation` -- run all remediation integration tests

## Dependencies
- Depends on: Task 1 -- Add remediation module with summary aggregation endpoint
- Depends on: Task 2 -- Add remediation by-product breakdown endpoint
