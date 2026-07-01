# Task 8 — Add integration tests for the SBOM comparison endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/compare` endpoint. These tests should exercise the comparison logic with real database state, covering all six diff categories, edge cases (empty diffs, missing SBOMs, missing parameters), and validating the response shape matches the API contract.

## Files to Create
- `tests/api/sbom_compare.rs` — Integration tests for the SBOM comparison endpoint

## Files to Modify
- `tests/api/mod.rs` — Register the new `sbom_compare` test module (if a mod.rs exists for test modules)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs` — tests use a real PostgreSQL test database, create test data via the ingestion service, and assert on HTTP response status and body.
- Use `assert_eq!(resp.status(), StatusCode::OK)` for success cases and `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` / `StatusCode::NOT_FOUND` for error cases, following the existing test assertion pattern.
- Test scenarios:
  1. **Full diff**: Ingest two SBOMs with known differences across all categories, compare, and assert each diff section
  2. **Self-comparison**: Compare an SBOM with itself, assert all diff sections are empty
  3. **Missing left param**: Call without `left`, assert 400
  4. **Missing right param**: Call without `right`, assert 400
  5. **Nonexistent left SBOM**: Call with a non-existent left ID, assert 404
  6. **Nonexistent right SBOM**: Call with a non-existent right ID, assert 404
  7. **Version change direction**: Ingest two SBOMs where a package has a higher version in the right (upgrade) and another has a lower version (downgrade), assert direction values
  8. **Vulnerability diff**: Ingest SBOMs with different advisory associations, verify new/resolved vulnerabilities
- Use the `IngestorService` (`modules/ingestor/src/service/mod.rs`) to create test SBOMs and their associated packages/advisories in the test database.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM endpoint tests for test setup patterns, database initialization, and assertion style
- `tests/api/advisory.rs` — Existing advisory endpoint tests for advisory-related test data creation
- `modules/ingestor/src/service/mod.rs::IngestorService` — Service for ingesting test SBOM and advisory data

## Acceptance Criteria
- [ ] All eight test scenarios pass
- [ ] Tests use real database (not mocks) following the project's integration test convention
- [ ] Response body assertions validate the structure and content of each diff category
- [ ] Error cases (400, 404) are covered
- [ ] Tests are isolated (each test creates its own test data)

## Test Requirements
- [ ] Integration test: full diff scenario with all six categories populated
- [ ] Integration test: self-comparison returns empty diff
- [ ] Integration test: missing left parameter returns 400
- [ ] Integration test: missing right parameter returns 400
- [ ] Integration test: nonexistent left SBOM returns 404
- [ ] Integration test: nonexistent right SBOM returns 404
- [ ] Integration test: version change direction (upgrade/downgrade) is correct
- [ ] Integration test: new/resolved vulnerabilities are correctly computed from advisory associations

## Verification Commands
- `cargo test --package trustify-tests -- sbom_compare` — run all comparison integration tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison service and endpoint
