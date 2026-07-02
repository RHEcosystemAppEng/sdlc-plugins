## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint, covering the happy path, 404 handling, advisory deduplication, threshold filtering, and cache invalidation after advisory ingestion. These tests validate all acceptance criteria from the feature requirements and ensure the endpoint behaves correctly end-to-end against a real PostgreSQL test database.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — integration test module for the advisory summary endpoint; contains test functions for each scenario

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present (e.g., ensure `trustify-fundamental` and `trustify-ingestor` are listed as dev-dependencies)

## Implementation Notes
- Follow the integration test pattern in `tests/api/sbom.rs` (SBOM endpoint tests) and `tests/api/advisory.rs` (advisory endpoint tests). These tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern per Key Conventions §Testing.
- Test setup should:
  1. Create an SBOM via the ingestion pipeline or direct database insertion
  2. Create advisories with known severity levels (Critical, High, Medium, Low)
  3. Link advisories to the SBOM via the `sbom_advisory` join table
- Test scenarios to cover:
  1. **Happy path**: SBOM with advisories at each severity level returns correct counts and total
  2. **Empty SBOM**: SBOM with no linked advisories returns all zeros
  3. **404**: Non-existent SBOM ID returns 404 status
  4. **Deduplication**: Duplicate advisory links (same advisory linked multiple times) produce correct counts (each advisory counted once)
  5. **Threshold filtering**: Each threshold level (`critical`, `high`, `medium`, `low`) returns correctly filtered counts
  6. **Invalid threshold**: Invalid threshold value returns 400 status
  7. **Cache invalidation**: Ingest a new advisory after initial request, verify subsequent request returns updated counts
- Per Key Conventions §Testing: use integration tests in `tests/api/` with a real PostgreSQL test database. Applies: task creates `tests/api/sbom_advisory_summary.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — follow its test setup, HTTP client configuration, and assertion patterns
- `tests/api/advisory.rs` — reference for advisory-related test data setup and assertion patterns
- `modules/ingestor/src/service/mod.rs::IngestorService` — use for ingesting test SBOMs and advisories in test setup

## Acceptance Criteria
- [ ] Integration test file exists at `tests/api/sbom_advisory_summary.rs`
- [ ] Tests cover: happy path with correct severity counts, empty SBOM (zero counts), 404 for non-existent SBOM, deduplication of advisory links, all threshold filter levels, invalid threshold (400), and cache invalidation after ingestion
- [ ] All tests pass against a PostgreSQL test database
- [ ] Tests follow the project's existing test patterns and assertion style

## Test Requirements
- [ ] Test: `test_advisory_summary_happy_path` — create SBOM with known advisories, verify correct counts
- [ ] Test: `test_advisory_summary_empty` — SBOM with no advisories returns all zeros
- [ ] Test: `test_advisory_summary_not_found` — non-existent SBOM returns 404
- [ ] Test: `test_advisory_summary_deduplication` — duplicate links produce correct counts
- [ ] Test: `test_advisory_summary_threshold_critical` — threshold=critical filters correctly
- [ ] Test: `test_advisory_summary_threshold_high` — threshold=high filters correctly
- [ ] Test: `test_advisory_summary_threshold_invalid` — invalid threshold returns 400
- [ ] Test: `test_advisory_summary_cache_invalidation` — new advisory ingestion updates cached summary

## Verification Commands
- `cargo test -p trustify-tests -- sbom_advisory_summary` — all tests pass

## Dependencies
- Depends on: Task 3 — Implement GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 4 — Add optional threshold query parameter filtering
- Depends on: Task 5 — Add cache invalidation on advisory ingestion

## Jira Fields
- **Labels:** ai-generated-jira
- **Priority:** Major
- **Fix Versions:** RHTPA 1.5.0

[sdlc-workflow] Description digest: sha256-md:5eddc22ed44ebe651d25618e4038e5b32753ee1b181939249da3e5ebd8dc4c7e
