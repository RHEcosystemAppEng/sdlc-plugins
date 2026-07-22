## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint covering the primary success path, error cases, threshold filtering, and edge cases. These tests validate the full request-response cycle against a real PostgreSQL test database, consistent with the existing integration test suite.

## Files to Create
- `tests/api/sbom_advisory_summary.rs` — Integration tests for the advisory-summary endpoint

## Implementation Notes
Follow the integration test patterns established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern per Key Conventions. Set up test data by ingesting an SBOM and linking advisories with various severities using the ingestion pipeline from `modules/ingestor/src/service/mod.rs`. Test cases should cover: (1) valid SBOM with mixed-severity advisories returns correct counts and total, (2) nonexistent SBOM ID returns 404, (3) SBOM with no advisories returns all zero counts, (4) `?threshold=critical` returns only critical count, (5) duplicate advisory links are deduplicated in the count, (6) response JSON shape matches `AdvisorySeveritySummary` struct fields from `modules/fundamental/src/sbom/model/advisory_summary.rs`.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration test patterns and test setup helpers
- `tests/api/advisory.rs` — Advisory test data setup patterns
- `modules/ingestor/src/service/mod.rs::IngestorService` — For setting up test data via ingestion

## Acceptance Criteria
- [ ] Test covers successful response with correct severity counts
- [ ] Test covers 404 response for nonexistent SBOM
- [ ] Test covers zero counts for SBOM with no advisories
- [ ] Test covers threshold query parameter filtering
- [ ] Test covers advisory deduplication
- [ ] All tests pass against PostgreSQL test database

## Test Requirements
- [ ] Integration test: GET /api/v2/sbom/{id}/advisory-summary returns 200 with correct counts
- [ ] Integration test: GET /api/v2/sbom/{nonexistent}/advisory-summary returns 404
- [ ] Integration test: advisory-summary returns zeros when SBOM has no advisories
- [ ] Integration test: ?threshold=critical filters to critical-only counts
- [ ] Integration test: duplicate advisory links produce deduplicated counts

## Verification Commands
- `cargo test --test api sbom_advisory_summary` — all integration tests pass

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching