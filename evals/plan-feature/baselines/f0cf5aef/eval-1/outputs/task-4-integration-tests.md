## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests should cover the full request-response cycle against a real PostgreSQL test database, following the existing integration test patterns in `tests/api/`.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add the new test module if test discovery requires explicit registration

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` for test setup, database seeding, HTTP client construction, and assertion style (`assert_eq!(resp.status(), StatusCode::OK)`).
- Tests must hit a real PostgreSQL test database, consistent with the project's testing conventions. Seed the database with known SBOM and advisory data to produce deterministic severity counts.
- Test deduplication by creating multiple links between the same advisory and SBOM, verifying the count does not inflate.
- Per repo conventions: integration tests in `tests/api/` use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; follow setup and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint integration tests; reference for how advisory test data is seeded

## Acceptance Criteria
- [ ] Integration test: SBOM with known advisories returns correct severity counts per level
- [ ] Integration test: SBOM with no advisories returns all-zero counts and total of 0
- [ ] Integration test: non-existent SBOM ID returns 404 status
- [ ] Integration test: duplicate advisory-SBOM links do not inflate severity counts
- [ ] Integration test: response body deserializes to the expected JSON shape with all five fields (critical, high, medium, low, total)
- [ ] All tests pass with `cargo test`

## Test Requirements
- [ ] Test with SBOM having advisories across all four severity levels (Critical, High, Medium, Low)
- [ ] Test with SBOM having advisories at only one severity level
- [ ] Test edge case: SBOM exists but has zero advisories
- [ ] Test edge case: advisory linked to SBOM multiple times is counted once
- [ ] Test error case: SBOM ID does not exist

## Verification Commands
- `cargo test --test api -- advisory_summary` — run the new integration tests
- `cargo test` — verify no regressions across all tests

## Dependencies
- Depends on: Task 1 — Add AdvisorySeveritySummary model and severity aggregation service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute cache
