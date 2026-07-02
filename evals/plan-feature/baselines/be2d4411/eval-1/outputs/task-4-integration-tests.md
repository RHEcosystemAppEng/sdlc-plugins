## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should cover the happy path with all severity levels, the 404 case for non-existent SBOMs, advisory deduplication behavior, and the empty advisory case. These tests run against a real PostgreSQL test database following the project's established integration testing patterns.

## Files to Modify
- `tests/api/sbom.rs` — add integration test functions for the advisory-summary endpoint

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`: set up test fixtures, make HTTP requests to the test server, and assert on response status codes and body content.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern established in the test suite.
- Test data setup for each test case:
  - **Happy path**: ingest a test SBOM, create and link advisories at each severity level (Critical, High, Medium, Low), call the endpoint, verify all counts match.
  - **404 case**: call the endpoint with a non-existent SBOM UUID, verify HTTP 404 response.
  - **Deduplication**: link the same advisory to the same SBOM via two different paths (e.g., two `sbom_advisory` records with the same advisory ID), verify the count is 1, not 2.
  - **Empty case**: ingest a test SBOM with no linked advisories, verify all counts are 0 and `total` is 0.
- Deserialize the JSON response body into `AdvisorySeveritySummary` and assert field-level equality for precise verification.

Per CONVENTIONS.md §Testing: write integration tests in `tests/api/sbom.rs` using the real PostgreSQL test database with the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
Applies: task modifies `tests/api/sbom.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — reuse existing SBOM test fixture setup (test server initialization, SBOM ingestion helpers)
- `tests/api/advisory.rs` — reuse advisory creation fixtures and correlation helpers for setting up test advisories with specific severity levels

## Acceptance Criteria
- [ ] Happy path test: SBOM with advisories at all four severity levels returns correct counts and correct total
- [ ] 404 test: non-existent SBOM ID returns HTTP 404
- [ ] Deduplication test: same advisory linked multiple times to the same SBOM is counted once, not multiple times
- [ ] Empty case test: SBOM with no linked advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] All tests pass against the PostgreSQL test database via `cargo test`

## Test Requirements
- [ ] `test_advisory_summary_happy_path` — ingest SBOM, link advisories at all severity levels, verify counts
- [ ] `test_advisory_summary_not_found` — request summary for non-existent SBOM, verify 404
- [ ] `test_advisory_summary_deduplication` — link same advisory twice, verify single count
- [ ] `test_advisory_summary_empty` — SBOM with no advisories, verify all zeros

## Verification Commands
- `cargo test --test api -- advisory_summary` — all advisory-summary integration tests pass

## Dependencies
- Depends on: Task 2 — Create GET /api/v2/sbom/{id}/advisory-summary endpoint with caching

---

[sdlc-workflow] Description digest: sha256-md:a68b20ee557da0885017cc7e5d67f55aa263648c86aca9627270da9cb303a8cb
