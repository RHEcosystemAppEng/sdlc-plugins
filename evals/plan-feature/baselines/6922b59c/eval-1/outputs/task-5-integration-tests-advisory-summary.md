## Repository
trustify-backend

## Target Branch
main

## Description
Add end-to-end integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should exercise the full request lifecycle against a real PostgreSQL test database, covering success scenarios, error cases, deduplication correctness, caching behavior, and the optional threshold query parameter. These tests ensure the endpoint, service, and model layers work correctly together.

## Files to Modify
- `tests/api/sbom.rs` — add integration test functions for the advisory summary endpoint

## Implementation Notes
Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Tests should:
1. Set up test data: create an SBOM, create advisories at various severity levels, and link them via the `sbom_advisory` join table
2. Call the endpoint via the test HTTP client
3. Assert on response status codes, JSON body shapes, and specific count values

For the deduplication test, link the same advisory to the same SBOM multiple times (or via different paths) and verify it is counted only once.

For the caching test, verify the `Cache-Control` header is present on the response.

For the threshold test, call the endpoint with `?threshold=high` and verify that only `critical` and `high` counts are non-zero (medium and low should be zero).

Per CONVENTIONS.md §Testing: use the `assert_eq!(resp.status(), StatusCode::OK)` pattern and test against a real PostgreSQL test database.
Applies: task modifies `tests/api/sbom.rs` matching the convention's test file scope.

Per CONVENTIONS.md §Error Handling: verify that error responses use the `AppError` format with appropriate status codes.
Applies: task modifies `tests/api/sbom.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests demonstrating test setup, HTTP client usage, and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint tests for reference on setting up advisory test data
- `entity/src/sbom_advisory.rs` — SeaORM entity for creating test data in the join table

## Acceptance Criteria
- [ ] Integration test: `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct severity counts for an SBOM with known advisory data
- [ ] Integration test: returns 404 for a non-existent SBOM ID
- [ ] Integration test: returns all-zero counts for an SBOM with no linked advisories
- [ ] Integration test: deduplicates advisories — same advisory linked multiple times is counted once
- [ ] Integration test: response includes `Cache-Control` header
- [ ] Integration test: `?threshold=high` returns zero for medium and low counts
- [ ] Integration test: invalid threshold value returns 400

## Test Requirements
- [ ] All integration tests pass against a real PostgreSQL test database
- [ ] Tests are independent — each test sets up its own data and does not depend on test execution order
- [ ] Test functions include doc comments describing the scenario being tested

## Verification Commands
- `cargo test --test api sbom::advisory_summary` — all advisory summary integration tests pass

## Dependencies
- Depends on: Task 1 — Add advisory severity summary response model
- Depends on: Task 2 — Add SBOM advisory severity aggregation service method
- Depends on: Task 3 — Add advisory summary REST endpoint with caching
