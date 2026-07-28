## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the remediation summary and by-product endpoints. Tests should verify correct aggregation behavior, edge cases (empty data, single severity, large datasets), and error handling. Tests follow the existing integration test pattern in tests/api/ using a real PostgreSQL test database.

## Files to Create
- `tests/api/remediation.rs` -- integration tests for GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product

## Files to Modify
- `tests/Cargo.toml` -- add remediation test module if test modules are registered explicitly

## Implementation Notes
- Per CONVENTIONS.md (Key Conventions -- Testing): integration tests in `tests/api/` hit a real PostgreSQL test database. Use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/remediation.rs` matching the convention's `.rs` file scope.
- Follow the test structure in `tests/api/advisory.rs` and `tests/api/sbom.rs` for test setup, database seeding, and assertion patterns.
- Test scenarios should seed the database with known vulnerability and SBOM data, then verify that aggregation counts are correct.
- Include tests for the p95 < 500ms performance requirement by verifying that responses complete within a reasonable time for datasets up to 10,000 vulnerabilities.
- Test pagination behavior on the by-product endpoint with varying offset and limit values.

## Reuse Candidates
- `tests/api/advisory.rs` -- reference integration test file; follow the same test setup and assertion patterns
- `tests/api/sbom.rs` -- reference integration test file; reuse database seeding patterns for SBOM test data

## Acceptance Criteria
- [ ] Integration tests cover both remediation endpoints (summary and by-product)
- [ ] Tests verify correct aggregation with known seeded data
- [ ] Tests verify empty-data edge cases
- [ ] Tests verify pagination on the by-product endpoint
- [ ] All tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Test summary endpoint returns correct severity x status counts with seeded data
- [ ] Test summary endpoint returns zero counts with empty database
- [ ] Test by-product endpoint returns correct per-product breakdown
- [ ] Test by-product endpoint pagination with offset and limit
- [ ] Test error handling for both endpoints

## Verification Commands
- `cargo test --test api -- remediation` -- remediation integration tests pass

## Dependencies
- Depends on: Task 1 -- Add remediation summary aggregation endpoint
- Depends on: Task 2 -- Add per-product remediation breakdown endpoint
