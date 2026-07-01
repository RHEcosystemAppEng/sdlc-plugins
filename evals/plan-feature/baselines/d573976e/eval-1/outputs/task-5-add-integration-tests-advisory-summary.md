# Task 5 — Add comprehensive integration tests for advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add a comprehensive integration test suite for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering all use cases: correct severity aggregation, advisory deduplication, SBOM-not-found handling, threshold filtering, and cache behavior. These tests follow the existing integration test pattern used by the SBOM and advisory endpoint tests.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add the new test module if test discovery requires explicit registration

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` — these tests hit a real PostgreSQL test database
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in the test suite
- Test setup should:
  1. Create an SBOM via the ingestion pipeline
  2. Create advisories at various severity levels (Critical, High, Medium, Low)
  3. Link advisories to the SBOM via the `sbom_advisory` join table
- Test cases must cover:
  - SBOM with advisories at all four severity levels — verify correct counts per level
  - SBOM with duplicate advisory links — verify deduplication (each advisory counted once)
  - SBOM with zero advisories — verify all counts are zero
  - Non-existent SBOM ID — verify 404 response
  - `?threshold=critical` — verify only critical count returned
  - `?threshold=high` — verify critical and high counts returned
  - `?threshold=medium` — verify critical, high, and medium counts returned
  - `?threshold=low` — verify all counts returned (equivalent to no threshold)
  - Invalid threshold value — verify appropriate error response

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests showing test setup, database seeding, and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint integration tests showing advisory creation and test patterns
- `tests/api/search.rs` — additional integration test example for reference

## Acceptance Criteria
- [ ] All integration test cases pass against a PostgreSQL test database
- [ ] Tests cover the positive path (correct counts), edge cases (zero advisories, deduplication), error path (404), and threshold filtering
- [ ] Tests follow the established patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`

## Test Requirements
- [ ] Integration test: SBOM with advisories at all four severity levels returns correct counts
- [ ] Integration test: duplicate advisory links produce deduplicated counts
- [ ] Integration test: SBOM with zero advisories returns all-zero counts and total of zero
- [ ] Integration test: non-existent SBOM ID returns 404 status code
- [ ] Integration test: threshold=critical returns only critical and total counts
- [ ] Integration test: threshold=high returns critical, high, and total counts
- [ ] Integration test: invalid threshold value returns an error response

## Verification Commands
- `cargo test --test api advisory_summary` — expected: all advisory-summary tests pass
- `cargo test --test api` — expected: all API integration tests pass (including existing ones, no regressions)

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint
- Depends on: Task 4 — Add cache invalidation for advisory-summary on advisory ingestion
