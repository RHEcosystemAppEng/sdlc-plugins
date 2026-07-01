# Task 4 — Add integration tests for SBOM comparison endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add comprehensive integration tests for the SBOM comparison endpoint. These tests verify end-to-end behavior against a real PostgreSQL test database, covering happy path comparisons, edge cases (empty SBOMs, identical SBOMs, large diffs), and error handling (missing parameters, non-existent IDs).

## Files to Create
- `tests/api/sbom_compare.rs` — Integration tests for GET /api/v2/sbom/compare covering all comparison scenarios

## Files to Modify
- `tests/api/mod.rs` — Add `mod sbom_compare;` to include the new test module (if test modules are registered in a mod.rs; otherwise the test runner auto-discovers)

## Implementation Notes

### Test patterns

Follow the existing integration test patterns in `tests/api/sbom.rs`:
- Use `assert_eq!(resp.status(), StatusCode::OK)` for success assertions
- Hit the real PostgreSQL test database
- Set up test data by ingesting two SBOM fixtures with known package differences
- Verify response body structure by deserializing into `SbomComparisonResult`

### Test scenarios

1. **Happy path**: Ingest two SBOMs with known differences — verify added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes are all correctly populated
2. **Identical SBOMs**: Compare an SBOM with itself — verify all diff sections are empty arrays
3. **Missing parameters**: Omit `left` or `right` — verify 400 status
4. **Non-existent SBOM**: Use a random UUID — verify 404 status
5. **Large diff**: Test with SBOMs containing many packages to verify performance NFR (p95 < 1s for 2000 packages)

### Reuse candidates

- `tests/api/sbom.rs` — existing SBOM endpoint integration tests demonstrating the test setup and assertion patterns
- `tests/api/advisory.rs` — advisory integration tests for reference on testing advisory-related responses

Per CONVENTIONS.md: integration tests use the pattern `assert_eq!(resp.status(), StatusCode::OK)` and test against a real PostgreSQL test database.
Applies: task creates `tests/api/sbom_compare.rs` matching the convention's Rust test file scope.

## Acceptance Criteria
- [ ] All integration tests pass against the PostgreSQL test database
- [ ] Happy path test verifies all six diff sections contain correct data
- [ ] Identical SBOM comparison returns empty diff sections
- [ ] Error cases (missing params, non-existent IDs) return appropriate HTTP status codes
- [ ] Tests verify response body deserialization into SbomComparisonResult

## Test Requirements
- [ ] Integration test: two SBOMs with added packages — verify added_packages section
- [ ] Integration test: two SBOMs with removed packages — verify removed_packages section
- [ ] Integration test: two SBOMs with version changes — verify version_changes with direction
- [ ] Integration test: two SBOMs with new vulnerabilities — verify new_vulnerabilities with severity
- [ ] Integration test: two SBOMs with resolved vulnerabilities — verify resolved_vulnerabilities
- [ ] Integration test: two SBOMs with license changes — verify license_changes
- [ ] Integration test: identical SBOM comparison returns empty diff
- [ ] Integration test: missing query parameters return 400
- [ ] Integration test: non-existent SBOM ID returns 404

## Verification Commands
- `cargo test -p trustify-tests -- api::sbom_compare` — should pass all comparison integration tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison REST endpoint

---
Priority: Critical
Fix Versions: RHTPA 1.5.0
Labels: ai-generated-jira

[sdlc-workflow] Description digest: sha256-md:d6a0c4b8e3f9572a1d7e0b4c6f8a2d5e9b3c7f1a4d6e8b0c3f5a7d9e1b4c6f8a
