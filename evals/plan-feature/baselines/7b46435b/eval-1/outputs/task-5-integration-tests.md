# Task 5 — Add integration tests for advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all MVP requirements: correct severity counts with deduplication, 404 for missing SBOMs, caching behavior, and response shape validation. Integration tests follow the existing pattern in `tests/api/` and run against a real PostgreSQL test database.

## Files to Modify
- `tests/api/sbom.rs` — add advisory-summary integration tests (or create a new test file if the existing file is already large)

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — dedicated integration test file for advisory-summary endpoint (if splitting from sbom.rs)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`: tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for status assertions.
  Applies: task modifies `tests/api/sbom.rs` matching the convention's Rust test file scope.
- Test setup should:
  1. Create an SBOM via the ingestion pipeline
  2. Create advisories at different severity levels (critical, high, medium, low)
  3. Link advisories to the SBOM via the sbom_advisory join table
  4. Make HTTP requests to the advisory-summary endpoint and verify responses
- Test deduplication by linking the same advisory to the SBOM through multiple paths and verifying it is counted only once.
- Test 404 by requesting advisory-summary for a non-existent SBOM ID.
- Test caching by verifying response headers or by making a request, modifying data, and verifying the cached response is returned.
- Per constraints doc section 5 (Code Change Rules): tests must follow the patterns used in sibling test files.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration test patterns (setup, assertions, helper functions)
- `tests/api/advisory.rs` — advisory test patterns and test data creation helpers
- `tests/Cargo.toml` — test dependency configuration

## Acceptance Criteria
- [ ] Integration tests cover: valid SBOM returns correct severity counts
- [ ] Integration tests cover: non-existent SBOM returns 404
- [ ] Integration tests cover: deduplication of advisories by ID
- [ ] Integration tests cover: total equals sum of individual severity counts
- [ ] Integration tests cover: response JSON shape matches expected format
- [ ] All tests pass against a real PostgreSQL test database

## Test Requirements
- [ ] Test: SBOM with advisories at all four severity levels returns correct counts for each
- [ ] Test: SBOM with no advisories returns all zeros
- [ ] Test: SBOM with duplicate advisory links returns deduplicated count
- [ ] Test: Non-existent SBOM ID returns 404
- [ ] Test: Response body deserializes to expected struct with correct field names and types
- [ ] Test: Endpoint returns appropriate content-type header (application/json)

## Verification Commands
- `cargo test --package tests -- sbom_advisory_summary` — all integration tests pass
- `cargo test --workspace` — full test suite passes (no regressions)

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with 5-minute caching
