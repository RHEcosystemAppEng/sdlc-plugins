## Repository
trustify-backend

## Target Branch
main

## Description
Add end-to-end integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. Tests run against a real PostgreSQL test database and verify the complete flow from SBOM/advisory ingestion through the aggregation endpoint response, including 404 handling, severity counting, deduplication, threshold filtering, and caching behavior.

## Files to Create
- `tests/api/advisory_summary.rs` — integration test module for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add the new test module if required by the test runner configuration

## Implementation Notes
- Per CONVENTIONS.md §Testing: follow the established integration test pattern in `tests/api/` — tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
  Applies: task creates `tests/api/advisory_summary.rs` matching the convention's test file scope.
- Reference `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup patterns including database seeding, HTTP client construction, and response parsing.
- Test data setup should ingest at least one SBOM and multiple advisories at different severity levels, then call the advisory-summary endpoint and verify the counts match.
- Include a test for the deduplication requirement: link the same advisory to an SBOM twice and verify it is counted only once.
- Include a test for the threshold filter: call with `?threshold=high` and verify only critical and high counts are returned.
- Include a test for 404: call with a non-existent SBOM UUID and verify 404 status.

## Reuse Candidates
- `tests/api/sbom.rs` — SBOM endpoint integration tests; reference for test setup, database seeding, and HTTP client patterns
- `tests/api/advisory.rs` — advisory endpoint integration tests; reference for advisory ingestion in test context
- `modules/ingestor/src/service/mod.rs::IngestorService` — use for test data seeding (ingest SBOMs and advisories)

## Acceptance Criteria
- [ ] Integration test verifies 200 response with correct severity counts for an SBOM with known advisories
- [ ] Integration test verifies 404 response for a non-existent SBOM ID
- [ ] Integration test verifies advisory deduplication (same advisory linked multiple times counts once)
- [ ] Integration test verifies optional `?threshold` query parameter filters results correctly
- [ ] Integration test verifies caching behavior (second call within 5 minutes returns cached response)
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Test: POST advisories at each severity level, link to SBOM, call advisory-summary, verify counts
- [ ] Test: link same advisory twice, verify count is 1 (not 2)
- [ ] Test: call with non-existent UUID, verify 404
- [ ] Test: call with `?threshold=high`, verify only critical and high are non-zero (or only those levels are included)
- [ ] Test: call endpoint twice within 5 minutes, verify second response is served from cache (via response headers or timing)

## Verification Commands
- `cargo test --test advisory_summary` — run the full advisory-summary integration test suite
- `cargo test --test advisory_summary -- --nocapture` — run with output for debugging

## Dependencies
- Depends on: Task 1 — Add advisory severity aggregation model and service method
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 3 — Add cache invalidation for advisory summary on advisory ingestion
