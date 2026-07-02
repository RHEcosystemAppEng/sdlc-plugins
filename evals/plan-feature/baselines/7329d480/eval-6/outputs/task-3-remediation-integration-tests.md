# Task 3: Add integration tests for remediation endpoints

Parent Epic: TC-9006: trustify-backend

## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the remediation REST endpoints. Tests verify that `GET /api/v2/remediation/summary` returns correctly aggregated severity/status counts and that `GET /api/v2/remediation/by-product` returns accurate per-product breakdowns with pagination support. Tests run against a real PostgreSQL test database following the existing integration test patterns.

## Files to Create
- `tests/api/remediation.rs` — integration tests for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`

## Files to Modify
- `tests/api/mod.rs` — add `mod remediation;` to register the new test module (if a mod.rs exists; otherwise add to the test harness entry point)

## Implementation Notes
- Per CONVENTIONS.md §Testing: place integration tests in `tests/api/` and use a real PostgreSQL test database. Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status assertions. Applies: task creates `tests/api/remediation.rs` matching the convention's .rs test scope.
- Reference `tests/api/sbom.rs` and `tests/api/advisory.rs` for test structure, database setup/teardown, and HTTP client configuration.
- Tests should seed the database with known SBOM, advisory, and vulnerability data to produce predictable aggregation results.
- Test cases for the summary endpoint: verify counts group correctly by severity and status, verify empty dataset returns zero counts.
- Test cases for the by-product endpoint: verify per-product counts are accurate, verify pagination parameters work (`offset`, `limit`), verify response format matches `PaginatedResults<ProductRemediation>`.
- Test the p95 < 500ms requirement is achievable by verifying the summary endpoint responds within a reasonable time for a moderate dataset.

## Reuse Candidates
- `tests/api/sbom.rs` — integration test patterns for HTTP endpoint testing; reuse database setup, HTTP client, and assertion patterns
- `tests/api/advisory.rs` — integration test patterns with advisory data seeding; reference for seeding vulnerability/severity data

## Acceptance Criteria
- [ ] Integration test for `GET /api/v2/remediation/summary` verifies correct severity/status aggregation with seeded data
- [ ] Integration test for `GET /api/v2/remediation/summary` verifies empty dataset returns zero counts
- [ ] Integration test for `GET /api/v2/remediation/by-product` verifies per-product breakdown accuracy
- [ ] Integration test for `GET /api/v2/remediation/by-product` verifies pagination with `offset` and `limit` parameters
- [ ] All tests follow the existing `assert_eq!(resp.status(), StatusCode::OK)` pattern
- [ ] Tests pass against the PostgreSQL test database

## Test Requirements
- [ ] At least 4 integration test cases covering both endpoints with positive and edge-case scenarios
- [ ] Tests seed known data to produce deterministic aggregation results

## Verification Commands
- `cargo test --test api remediation` — all remediation integration tests pass

## Dependencies
- Depends on: Task 2 — Add remediation REST endpoints
