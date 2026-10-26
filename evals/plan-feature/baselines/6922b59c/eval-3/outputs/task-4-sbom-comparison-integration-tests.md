## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add integration tests for the SBOM comparison endpoint. These tests exercise the full HTTP request/response cycle against a real PostgreSQL test database, verifying that the comparison endpoint returns correct structured diffs for various scenarios.

## Files to Modify
- `tests/api/sbom.rs` — add integration test cases for the comparison endpoint

## Implementation Notes
- Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/sbom.rs` matching the convention's test file scope. See existing tests in `tests/api/sbom.rs` for the established pattern.
- Test setup should:
  1. Ingest two SBOMs with known, different package sets using the existing ingestion infrastructure in `modules/ingestor/src/graph/sbom/mod.rs`
  2. Call `GET /api/v2/sbom/compare?left={id1}&right={id2}`
  3. Deserialize the response as `SbomComparisonResult`
  4. Assert the diff categories match expected values
- Reference existing test setup patterns in `tests/api/sbom.rs` for database initialization and test client creation.
- Include test scenarios for:
  - Valid comparison with mixed changes across all six categories
  - Identical SBOMs (expect empty diff)
  - Missing query parameters (expect 400)
  - Nonexistent SBOM ID (expect 404)
- Error handling assertions should use `StatusCode::BAD_REQUEST` and `StatusCode::NOT_FOUND` from `axum::http::StatusCode`.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint tests provide the test harness pattern (database setup, HTTP client, assertion style)
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion logic for setting up test fixtures with known package data

## Acceptance Criteria
- [ ] Integration test verifies successful comparison with known added, removed, and changed packages
- [ ] Integration test verifies comparison of identical SBOMs returns empty diff
- [ ] Integration test verifies 400 response when query parameters are missing
- [ ] Integration test verifies 404 response when an SBOM ID does not exist
- [ ] All existing SBOM integration tests continue to pass

## Test Requirements
- [ ] Integration test: compare two SBOMs with distinct package sets and verify added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, and license_changes
- [ ] Integration test: compare an SBOM with itself and verify all diff arrays are empty
- [ ] Integration test: send request without `left` parameter and verify 400 status
- [ ] Integration test: send request with nonexistent SBOM ID and verify 404 status

## Verification Commands
- `cargo test -p trustify-tests api::sbom` — all SBOM integration tests pass (existing + new)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison service and REST endpoint
