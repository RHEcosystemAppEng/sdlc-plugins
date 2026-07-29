## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. These tests exercise the full request-response cycle against a real PostgreSQL test database, covering the happy path, edge cases (empty advisories, deduplication), and error scenarios (non-existent SBOM). This task consolidates all endpoint-level integration testing to validate the feature end-to-end.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — ensure test dependencies are configured (if any new deps needed)

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests use a real PostgreSQL test database and the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Test setup should: create an SBOM, create advisories at each severity level (Critical, High, Medium, Low), link them to the SBOM via the `sbom_advisory` relationship, then call the endpoint.
- Cover deduplication: create duplicate advisory-SBOM links and verify counts are not inflated.
- Cover the zero-advisory case: create an SBOM with no linked advisories and verify all counts are zero.
- Cover the 404 case: call the endpoint with a non-existent SBOM ID and verify the response status.
- Per Key Conventions: testing — integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; follow the same test setup, database seeding, and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint integration tests; reference for advisory creation and linking patterns

## Acceptance Criteria
- [ ] Integration tests cover: valid SBOM with advisories at all severity levels returns correct counts
- [ ] Integration tests cover: SBOM with no advisories returns all-zero counts with total = 0
- [ ] Integration tests cover: duplicate advisory links do not inflate counts
- [ ] Integration tests cover: non-existent SBOM ID returns 404
- [ ] Integration tests cover: response body matches expected JSON shape `{ critical, high, medium, low, total }`
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Test: SBOM with 2 critical, 1 high, 3 medium, 0 low advisories returns `{ critical: 2, high: 1, medium: 3, low: 0, total: 6 }`
- [ ] Test: SBOM with no linked advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] Test: SBOM with duplicate advisory links (same advisory linked twice) counts the advisory only once
- [ ] Test: non-existent SBOM ID returns 404 status
- [ ] Test: response content-type is `application/json`

## Verification Commands
- `cargo test --test api -- sbom_advisory_summary` — all integration tests pass

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service layer
- Depends on: Task 2 — Add advisory-summary endpoint with caching
