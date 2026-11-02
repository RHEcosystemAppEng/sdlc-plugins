## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the SBOM comparison endpoint (`GET /api/v2/sbom/compare`) in the existing test suite. Tests exercise the full request/response cycle against a real PostgreSQL test database, covering successful comparisons, error cases, and edge cases.

## Files to Modify
- `tests/api/sbom.rs` — add integration tests for the comparison endpoint

## Implementation Notes
Follow the existing integration test patterns in `tests/api/sbom.rs`:
- Tests use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status assertions
- Tests interact with a real PostgreSQL test database (not mocked)
- Reference `tests/api/advisory.rs` for advisory-related test setup patterns
- Set up test data:
  1. Ingest two SBOMs with overlapping and non-overlapping packages
  2. Associate advisories with specific SBOM-package combinations via `sbom_advisory` entity
  3. Set different licenses on overlapping packages between the two SBOMs
- Test cases:
  - Successful comparison: verify all six diff sections are populated correctly
  - Identical SBOMs: verify all diff sections are empty arrays
  - Non-existent SBOM: verify 404 response
  - Missing query params: verify 400 response
  - Large SBOM (performance): ingest SBOMs with many packages to verify sub-1s response time

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/sbom.rs` matching the convention's integration test scope.

## Acceptance Criteria
- [ ] Integration test for successful comparison with all six diff categories populated
- [ ] Integration test for comparison of identical SBOMs (empty diff)
- [ ] Integration test for 404 when SBOM ID does not exist
- [ ] Integration test for 400 when query parameters are missing
- [ ] All tests pass against the real PostgreSQL test database

## Test Requirements
- [ ] Test added packages: ingest two SBOMs where the right has packages the left does not, verify `added_packages` section
- [ ] Test removed packages: verify `removed_packages` section for packages in left not in right
- [ ] Test version changes: same package name with different versions in each SBOM
- [ ] Test new vulnerabilities: advisory linked to right SBOM but not left
- [ ] Test resolved vulnerabilities: advisory linked to left SBOM but not right
- [ ] Test license changes: same package with different licenses
- [ ] Test empty diff: compare an SBOM with itself

## Dependencies
- Depends on: Task 3 — Backend comparison endpoint
