## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests cover the full request-response cycle against a real PostgreSQL test database, verifying correct severity aggregation, deduplication, 404 handling, threshold filtering, and cache headers.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — Integration test module with test cases for the advisory summary endpoint

## Files to Modify
- `tests/Cargo.toml` — Add any necessary test dependencies if not already present (e.g., `serde_json` for response parsing)

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` — these show how to set up the test database, create test fixtures (SBOMs, advisories), make HTTP requests to the test server, and assert on response status codes and JSON bodies.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern from Key Conventions (Testing) for status code assertions.
- Test data setup should create an SBOM, create advisories with varying severities (Critical, High, Medium, Low), and link them via the `sbom_advisory` join table to establish the test scenario.
- For the deduplication test, link the same advisory to the same SBOM twice and verify it is counted only once.
- For the threshold test, use `?threshold=high` and verify that only Critical and High counts are non-zero (Medium and Low should be zero).
- Per Key Conventions (Testing): integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's `.rs` file scope.
- Per Key Conventions (Error handling): all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Test setup patterns for creating SBOMs and making assertions against SBOM endpoints
- `tests/api/advisory.rs` — Test setup patterns for creating advisories with severity levels

## Acceptance Criteria
- [ ] Integration test `test_advisory_summary_returns_correct_counts` verifies correct aggregation of severity counts for an SBOM with multiple advisories
- [ ] Integration test `test_advisory_summary_deduplication` verifies that duplicate advisory links are counted only once
- [ ] Integration test `test_advisory_summary_not_found` verifies 404 response for a non-existent SBOM ID
- [ ] Integration test `test_advisory_summary_threshold_filter` verifies threshold filtering returns only counts at or above the specified severity
- [ ] Integration test `test_advisory_summary_cache_headers` verifies the response includes `Cache-Control: max-age=300`
- [ ] Integration test `test_advisory_summary_empty_sbom` verifies an SBOM with zero advisories returns all-zero counts
- [ ] All tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Test for successful aggregation: create SBOM with 2 Critical, 3 High, 1 Medium, 0 Low advisories; verify counts `{ critical: 2, high: 3, medium: 1, low: 0, total: 6 }`
- [ ] Test for deduplication: link same advisory twice to same SBOM; verify it is counted once
- [ ] Test for 404: request summary for UUID that does not exist in database; verify HTTP 404
- [ ] Test for threshold filtering: request with `?threshold=high`; verify only Critical and High counts are included
- [ ] Test for cache headers: verify `Cache-Control` header value
- [ ] Test for empty SBOM: SBOM with no linked advisories returns all-zero counts

## Verification Commands
- `cargo test --test api -- sbom_advisory_summary` — runs all advisory summary integration tests

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (tests require the endpoint to exist and be registered)


[sdlc-workflow] Description digest: sha256-md:cbdd01bc473eb39b2af40b06a5dad07c508d9048fc176306dfcaf22a81230694
