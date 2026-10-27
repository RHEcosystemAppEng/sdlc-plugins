## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add integration tests for the remediation endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`). Tests exercise both endpoints against a real PostgreSQL test database with seeded vulnerability and SBOM data, verifying correct aggregation results and error handling.

## Files to Create
- `tests/api/remediation.rs` — integration tests for remediation endpoints

## Files to Modify
- `tests/Cargo.toml` — register the new test module if needed

## Implementation Notes
- Follow the integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs` — tests hit a real PostgreSQL test database.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in existing tests.
- Seed test data: create advisory entities with different severities and statuses, associate them with SBOMs, then verify the summary endpoint returns correct aggregated counts.
- For the by-product endpoint, seed multiple products with different remediation states and verify per-product breakdowns.
- Per Key Conventions: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/remediation.rs` matching the convention's integration test scope.

## Reuse Candidates
- `tests/api/sbom.rs` — example integration test patterns with database seeding
- `tests/api/advisory.rs` — example test patterns for advisory-related operations

## Acceptance Criteria
- [ ] Integration tests verify `GET /api/v2/remediation/summary` returns correct severity × status counts
- [ ] Integration tests verify `GET /api/v2/remediation/by-product` returns correct per-product breakdown
- [ ] Tests use real PostgreSQL database (not mocks)
- [ ] Tests verify pagination behavior for the by-product endpoint
- [ ] Tests verify error handling for invalid query parameters

## Test Requirements
- [ ] At least one test per endpoint verifying the happy path with seeded data
- [ ] Test that empty database returns zero counts (not errors)
- [ ] Test pagination parameters produce correct result slices

## Verification Commands
- `cargo test --test api remediation` — run remediation integration tests

## Dependencies
- Depends on: Task 2 — Remediation summary endpoint
- Depends on: Task 3 — Remediation by-product endpoint
