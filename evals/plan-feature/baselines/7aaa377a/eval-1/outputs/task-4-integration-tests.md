# Task 4 — Add integration tests for advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should cover the full request-response lifecycle against a real PostgreSQL test database, following the project's established integration test patterns in `tests/api/`. This covers the primary success path, error cases (nonexistent SBOM), deduplication correctness, and the optional threshold filtering behavior.

## Files to Create
- `tests/api/advisory_summary.rs` — integration test module for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add the new test module if needed for test discovery

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` — tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Test setup should ingest sample SBOMs and advisories with known severity levels, then verify the aggregation endpoint returns expected counts.
- Per Key Conventions §Testing: integration tests go in `tests/api/` and hit a real PostgreSQL test database.
  Applies: task creates `tests/api/advisory_summary.rs` matching the convention's `.rs` test file scope.
- Per Key Conventions §Error handling: verify that the endpoint returns proper `AppError`-based error responses for 404 cases.
  Applies: task creates `tests/api/advisory_summary.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; follow the same test setup, database seeding, and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint integration tests; reference for advisory test data setup
- `common/src/error.rs::AppError` — error response format to assert against in error test cases

## Acceptance Criteria
- [ ] Integration tests pass against a PostgreSQL test database
- [ ] Tests cover: successful aggregation, 404 for nonexistent SBOM, advisory deduplication, threshold filtering, and empty advisory set
- [ ] Tests follow the existing `tests/api/` patterns and conventions
- [ ] All tests have doc comments explaining what scenario they cover

## Test Requirements
- [ ] Test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct counts for an SBOM with advisories at all four severity levels
- [ ] Test: endpoint returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }` for an SBOM with no linked advisories
- [ ] Test: endpoint returns 404 for a nonexistent SBOM ID
- [ ] Test: advisory deduplication — an advisory linked to the same SBOM multiple times is counted only once
- [ ] Test: `?threshold=critical` returns only the critical count with other levels zeroed
- [ ] Test: `?threshold=high` returns critical and high counts with medium and low zeroed
- [ ] Test: `?threshold=medium` returns critical, high, and medium counts with low zeroed
- [ ] Test: invalid threshold value returns 400

## Verification Commands
- `cargo test --test api -- advisory_summary` — run all advisory-summary integration tests
- `cargo test --test api -- advisory_summary::test_advisory_summary_basic` — run a specific test

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
