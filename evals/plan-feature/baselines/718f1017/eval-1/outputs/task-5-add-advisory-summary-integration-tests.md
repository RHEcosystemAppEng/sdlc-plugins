# Task 5 — Add comprehensive integration tests for advisory summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all acceptance criteria from the feature: happy path with multiple severity levels, 404 for non-existent SBOM, deduplication of advisories, threshold query parameter filtering, and cache behavior. These tests follow the existing integration test patterns in `tests/api/` and run against a real PostgreSQL test database.

## Files to Modify
- `tests/api/sbom.rs` — add advisory summary integration tests to the existing SBOM test file, or alternatively create a new dedicated test file

## Files to Create
- `tests/api/advisory_summary.rs` — dedicated integration test file for the advisory summary endpoint (if the team convention prefers separate test files per endpoint rather than appending to the existing `sbom.rs`)

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` — these tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Test setup should: (1) create an SBOM via the ingestion pipeline or test fixture, (2) create advisories at various severity levels, (3) link advisories to the SBOM via the `sbom_advisory` join table
- For the deduplication test: create a scenario where the same advisory ID appears multiple times in the join table and verify the count reflects unique advisories only
- For the threshold test: call `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` and verify that only critical and high counts are non-zero
- For the 404 test: use a non-existent UUID as the SBOM ID and verify the response status is 404
- Per the repository's Key Conventions (Testing): integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/advisory_summary.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; demonstrates test setup, SBOM creation, and HTTP request patterns
- `tests/api/advisory.rs` — existing advisory endpoint integration tests; demonstrates advisory creation and assertion patterns
- `entity/src/sbom_advisory.rs` — the join table entity used to link advisories to SBOMs in test setup

## Acceptance Criteria
- [ ] Integration test for happy path: SBOM with advisories at all four severity levels returns correct counts
- [ ] Integration test for empty case: SBOM with no advisories returns all zeros and total=0
- [ ] Integration test for 404: non-existent SBOM ID returns 404 status
- [ ] Integration test for deduplication: duplicate advisory entries produce correct unique counts
- [ ] Integration test for threshold filter: `?threshold=critical` returns only critical count, others are zero
- [ ] Integration test for threshold filter: `?threshold=medium` returns critical, high, and medium counts
- [ ] All tests pass against PostgreSQL test database

## Test Requirements
- [ ] All acceptance criteria above are covered by runnable integration tests
- [ ] Tests use the established test setup patterns from sibling test files (`sbom.rs`, `advisory.rs`)
- [ ] Tests verify both response status codes and response body content

## Verification Commands
- `cargo test --test api -- advisory_summary` — expected: all advisory summary tests pass
- `cargo test --test api` — expected: all existing tests continue to pass (no regressions)

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching

<!-- [sdlc-workflow] Description digest: sha256-md:7c591cf817c7690ed8e8d75641c4e5e67fa23b4b7bea8b1fb3ef6fcd0fcd20d9 -->
