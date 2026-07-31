## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering the full range of scenarios including happy path, error cases, edge cases, and non-functional requirements. These tests hit a real PostgreSQL test database following the project's integration test conventions in `tests/api/`.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add test module reference if needed for the new test file

## Implementation Notes
- Follow the integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`: set up test data using the ingestion pipeline, make HTTP requests, and assert on response status codes and JSON bodies.
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern per the project's testing conventions.
- Test data setup: ingest an SBOM and link advisories at various severity levels to exercise the aggregation logic. Include cases with:
  - Multiple advisories at the same severity
  - Duplicate advisory links (same advisory linked multiple times to verify deduplication)
  - SBOMs with no advisories (all counts should be 0)
  - SBOMs with advisories at every severity level
- For performance-related tests, consider adding a test with a larger dataset (50+ advisories) to verify the query performs efficiently, though the p95 < 200ms requirement is better validated via dedicated performance benchmarks.
- Per repo Key Conventions §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database. Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern. See `tests/api/sbom.rs` for the established test setup and assertion patterns.
  Applies: task creates `tests/api/advisory_summary.rs` matching the convention's test `.rs` file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for SBOM endpoint test patterns (setup, request building, assertions)
- `tests/api/advisory.rs` — reference for advisory-related test data setup
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion for test data setup
- `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion and correlation for test data setup

## Acceptance Criteria
- [ ] Integration test for 200 response with correct severity counts for a valid SBOM with known advisories
- [ ] Integration test for 404 response when SBOM ID does not exist
- [ ] Integration test for deduplication (same advisory linked multiple times counts once)
- [ ] Integration test for SBOM with zero advisories (all counts are 0)
- [ ] Integration test for SBOM with advisories at all four severity levels
- [ ] Integration test for threshold query parameter filtering (critical, high, medium, low)
- [ ] Integration test for invalid threshold value returning 400
- [ ] Integration test for cache headers present in response
- [ ] All tests pass against a real PostgreSQL test database

## Test Requirements
- [ ] Tests cover all acceptance criteria listed above
- [ ] Tests follow the existing patterns in `tests/api/sbom.rs` for setup and assertions
- [ ] Tests use realistic advisory data with known severity levels for deterministic assertions

## Verification Commands
- `cargo test --test api` — all integration tests pass
- `cargo test --test api advisory_summary` — new advisory summary tests pass specifically

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model and service
- Depends on: Task 2 — Add advisory summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory severity summary
- Depends on: Task 4 — Add threshold query parameter for advisory summary
