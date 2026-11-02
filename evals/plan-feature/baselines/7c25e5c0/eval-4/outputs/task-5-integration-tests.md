## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. Tests cover successful report generation, non-compliant license flagging, 404 for missing SBOMs, transitive dependency inclusion, and performance within the p95 < 500ms requirement for SBOMs with up to 1000 packages.

## Files to Modify
- `tests/api/sbom.rs` — Add integration tests for the license-report endpoint alongside existing SBOM endpoint tests

## Implementation Notes
- Follow the integration test pattern in `tests/api/sbom.rs` for test structure, database setup, and HTTP client usage. Existing tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Reference `tests/api/advisory.rs` for additional examples of testing endpoints that join across multiple entity tables.
- Tests should:
  1. Set up test data: ingest an SBOM with packages having various licenses via the existing ingestion test helpers
  2. Configure a test license policy with known allowed/denied licenses
  3. Call `GET /api/v2/sbom/{id}/license-report` and verify the response
- Use the existing PostgreSQL test database infrastructure — do not mock the database.
- Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database. Applies: task modifies `tests/api/sbom.rs` matching the convention's integration test scope.

## Acceptance Criteria
- [ ] Integration test: valid SBOM returns a license report with correct grouping
- [ ] Integration test: denied license in policy results in `compliant: false` for that group
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: transitive dependencies appear in the report
- [ ] Integration test: report generation completes within acceptable time for a test dataset

## Test Requirements
- [ ] Test with an SBOM containing packages under MIT, Apache-2.0, and GPL-3.0 licenses
- [ ] Test with a policy that denies GPL-3.0 and verify only that group is flagged non-compliant
- [ ] Test with an SBOM ID that does not exist in the database
- [ ] Test that packages from transitive dependency tree are present in the report groups
- [ ] Test with an SBOM with no packages (edge case) returns an empty groups list

## Dependencies
- Depends on: Task 4 — License report endpoint
