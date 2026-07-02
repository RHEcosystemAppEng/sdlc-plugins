## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for both remediation endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`). Tests exercise the endpoints against a real PostgreSQL test database following the project's existing integration test pattern in `tests/api/`.

## Files to Create
- `tests/api/remediation.rs` — integration tests for remediation summary and by-product endpoints

## Files to Modify
- `tests/Cargo.toml` — add test dependency on the remediation module if needed

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs` — tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions.
  Per CONVENTIONS.md: integration tests in tests/api/ use real PostgreSQL test database with assert_eq!(resp.status(), StatusCode::OK) pattern.
  Applies: task creates `tests/api/remediation.rs` matching the convention's .rs test file scope.
- Seed test data by ingesting sample SBOMs and advisories through the existing ingestor service (`modules/ingestor/src/service/mod.rs`) before exercising remediation endpoints.
- Test the summary endpoint with varying combinations of severity levels and statuses to verify correct GROUP BY aggregation.
- Test the by-product endpoint with multiple products to verify per-product isolation and pagination.
- Include edge cases: empty dataset (no vulnerabilities), single product with all severities, and boundary pagination values.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for integration test setup and assertion patterns
- `tests/api/advisory.rs` — reference for advisory-related test data seeding
- `modules/ingestor/src/service/mod.rs::IngestorService` — for seeding test data

## Acceptance Criteria
- [ ] Integration tests for `GET /api/v2/remediation/summary` verify correct aggregation across severity levels and statuses
- [ ] Integration tests for `GET /api/v2/remediation/by-product` verify correct per-product breakdown and pagination
- [ ] Edge case tests cover empty datasets and boundary conditions
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Summary endpoint test with seeded data across all severity levels
- [ ] Summary endpoint test with empty dataset returns zero counts
- [ ] By-product endpoint test with multiple products returns correct per-product counts
- [ ] By-product endpoint test verifying pagination offset/limit behavior
- [ ] By-product endpoint test with empty dataset returns empty paginated result

## Verification Commands
- `cargo test --test api remediation -- --nocapture` — run remediation tests with output
- `cargo test --test api` — run all API integration tests to verify no regressions

## Dependencies
- Depends on: Task 1 — Create remediation module with summary aggregation endpoint
- Depends on: Task 2 — Add per-product remediation breakdown endpoint

[sdlc-workflow] Description digest: sha256-md:2631d7593ac0f73cdded8720dd808cc34d91f5b52608707a29b58c098f703520
