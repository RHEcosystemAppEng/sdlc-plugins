## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the GET /api/v2/sbom/{id}/advisory-summary endpoint in the existing SBOM integration test suite. Tests should cover the full request-response cycle against a real PostgreSQL database, verifying correct severity aggregation, deduplication, error handling, and caching behavior.

## Files to Modify
- `tests/api/sbom.rs` — add integration test functions for the advisory-summary endpoint

## Implementation Notes
Follow the integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Use the existing test infrastructure for setting up test data (SBOMs, advisories with known severity levels, SBOM-advisory links via `entity/src/sbom_advisory.rs`). Tests run against a real PostgreSQL instance per the project's testing conventions. Ensure test data includes duplicate advisory links to verify deduplication logic, and advisories across all four severity levels to verify correct grouping.
Per CONVENTIONS.md §Testing Conventions: write integration tests in `tests/api/` using real PostgreSQL. Applies: task modifies `tests/api/sbom.rs` matching the convention's Rust integration test scope.

## Acceptance Criteria
- [ ] Test for successful response with SBOMs containing advisories at all severity levels
- [ ] Test for correct deduplication — same advisory linked multiple times produces a count of 1
- [ ] Test for 404 response when SBOM ID does not exist
- [ ] Test for empty response (all zeros) when SBOM has no linked advisories
- [ ] Test for response JSON structure matching `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }`
- [ ] Test for Cache-Control header presence in response
- [ ] All tests pass against real PostgreSQL

## Test Requirements
- [ ] Integration test: GET /api/v2/sbom/{id}/advisory-summary returns correct counts for SBOM with mixed-severity advisories
- [ ] Integration test: GET /api/v2/sbom/{id}/advisory-summary deduplicates advisories by advisory ID
- [ ] Integration test: GET /api/v2/sbom/{id}/advisory-summary returns 404 for non-existent SBOM
- [ ] Integration test: GET /api/v2/sbom/{id}/advisory-summary returns all-zero counts for SBOM with no advisories
- [ ] Integration test: response includes Cache-Control: max-age=300 header

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint
- Depends on: Task 4 — Cache invalidation
