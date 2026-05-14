# Task 3 — Add integration tests for the advisory-summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The tests verify correct severity aggregation, deduplication, 404 handling, caching behavior, and threshold filtering. These tests follow the existing integration test patterns established in `tests/api/` and use a real PostgreSQL test database.

## Files to Create
- `tests/api/advisory_summary.rs` — Integration test module for the advisory-summary endpoint, covering all acceptance criteria from the feature requirements.

## Files to Modify
- `tests/Cargo.toml` — Add the new test module if test registration is explicit (check existing pattern).

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests use a real PostgreSQL test database and assert on `resp.status()` using `StatusCode::OK` / `StatusCode::NOT_FOUND` patterns.
- Test setup should:
  1. Create an SBOM via the ingestion pipeline or direct database insertion
  2. Create multiple advisories with varying severity levels (Critical, High, Medium, Low)
  3. Link advisories to the SBOM via the `sbom_advisory` join table
- For deduplication testing, create a scenario where the same advisory could be linked to the SBOM through multiple paths and verify that counts reflect unique advisory IDs only.
- For the threshold test, call `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` and verify that only `critical` and `high` counts are included (or that `medium` and `low` are zero, depending on the filtering behavior implemented in Task 1).
- Reference `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/sbom_advisory.rs` for the entity structures needed to set up test data.
- Each test function must have a doc comment explaining the scenario being tested.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests, follow the same test setup, request/response, and assertion patterns
- `tests/api/advisory.rs` — existing advisory endpoint integration tests, demonstrates advisory entity setup in test context
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity used for test data setup

## Acceptance Criteria
- [ ] Test passes for a successful advisory-summary request with known severity counts
- [ ] Test verifies JSON response shape has `critical`, `high`, `medium`, `low`, and `total` fields
- [ ] Test verifies 404 response for a non-existent SBOM ID
- [ ] Test verifies deduplication — same advisory linked multiple times does not inflate counts
- [ ] Test verifies threshold filtering returns correctly filtered counts
- [ ] Test verifies total count equals sum of individual severity counts

## Test Requirements
- [ ] `test_advisory_summary_success` — SBOM with known advisories returns correct severity breakdown
- [ ] `test_advisory_summary_not_found` — non-existent SBOM ID returns 404
- [ ] `test_advisory_summary_empty` — SBOM with no linked advisories returns all zeros
- [ ] `test_advisory_summary_deduplication` — duplicate advisory links do not inflate counts
- [ ] `test_advisory_summary_threshold_filter` — threshold parameter correctly filters severity levels
- [ ] `test_advisory_summary_total_consistency` — total field equals sum of critical + high + medium + low

## Dependencies
- Depends on: Task 1 — Add advisory severity summary model, service method, and REST endpoint
