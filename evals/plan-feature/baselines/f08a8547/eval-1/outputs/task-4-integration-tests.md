## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint (TC-9001). Tests should cover the happy path, 404 for non-existent SBOM, advisory deduplication, threshold filter behavior, and cache header presence. Tests follow the existing integration test patterns in `tests/api/`.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add the new test file to the test configuration if required by the project's test setup

## Implementation Notes
- Follow the existing test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`: set up a test database, ingest test SBOMs and advisories with known severity distributions, then make HTTP requests to the endpoint and assert on the response.
- Use `assert_eq!(resp.status(), StatusCode::OK)` for success cases and `assert_eq!(resp.status(), StatusCode::NOT_FOUND)` for missing SBOM cases, consistent with existing test assertions.
- For deduplication testing, link the same advisory to the same SBOM multiple times and verify the count reflects only unique advisories.
- For threshold testing, use `?threshold=high` and verify that `medium` and `low` are 0 or omitted while `critical` and `high` reflect correct counts.
- Verify that the response JSON shape matches `{ critical: N, high: N, medium: N, low: N, total: N }`.
- Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database; use the `assert_eq!(resp.status(), StatusCode::OK)` pattern. See `tests/api/sbom.rs` for the established test setup and assertion pattern.
  Applies: task creates `tests/api/advisory_summary.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint tests; follow the same test setup (database initialization, SBOM ingestion) and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint tests; follow the same test setup for advisory data ingestion and severity assignment

## Acceptance Criteria
- [ ] Integration test verifies `GET /api/v2/sbom/{id}/advisory-summary` returns 200 with correct severity counts for a valid SBOM
- [ ] Integration test verifies the endpoint returns 404 for a non-existent SBOM ID
- [ ] Integration test verifies that advisories linked multiple times to the same SBOM are counted only once
- [ ] Integration test verifies `?threshold=critical` filters severity counts correctly (non-MVP)
- [ ] Integration test verifies cache headers are present in the response
- [ ] All tests pass with `cargo test`

## Test Requirements
- [ ] Happy path: SBOM with known advisory severity distribution returns correct counts
- [ ] 404: non-existent SBOM ID returns 404 status
- [ ] Deduplication: same advisory linked twice produces a count of 1
- [ ] Threshold filter: `?threshold=high` returns only critical and high counts with adjusted total
- [ ] Cache headers: response includes cache-control headers with 5-minute TTL

## Verification Commands
- `cargo test --test api -- advisory_summary` — run all advisory-summary integration tests

## Dependencies
- Depends on: Task 1 — Add advisory severity count model and service method
- Depends on: Task 2 — Add advisory-summary REST endpoint with caching
