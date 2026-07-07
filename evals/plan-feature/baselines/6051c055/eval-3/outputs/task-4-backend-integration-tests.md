# Task 4 -- Backend integration tests for SBOM comparison

## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the SBOM comparison endpoint that verify the complete request/response cycle against a real PostgreSQL test database. Tests cover the full diff computation including added/removed packages, version changes, vulnerabilities, license changes, error handling, and performance characteristics.

## Files to Create
- `tests/api/sbom_compare.rs` -- Integration tests for the GET /api/v2/sbom/compare endpoint

## Files to Modify
- `tests/api/mod.rs` -- Add `mod sbom_compare;` to include the new test module

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` for test setup, test database initialization, and assertion patterns.
- Use the real PostgreSQL test database to ingest two SBOMs with known package differences, then call the comparison endpoint and verify the response.
- Per CONVENTIONS.md Test Patterns: integration tests hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/sbom_compare.rs` matching the convention's `.rs` test file scope.

## Acceptance Criteria
- [ ] All integration tests pass against a real PostgreSQL test database
- [ ] Tests cover all six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- [ ] Tests verify error responses for missing and invalid parameters
- [ ] Tests verify empty diff result when comparing identical SBOMs

## Test Requirements
- [ ] Integration test: compare two SBOMs with known package differences, verify added_packages and removed_packages in response
- [ ] Integration test: compare two SBOMs with version changes, verify version_changes array with correct direction values
- [ ] Integration test: compare two SBOMs with different vulnerability associations, verify new_vulnerabilities and resolved_vulnerabilities
- [ ] Integration test: compare two SBOMs with license differences, verify license_changes
- [ ] Integration test: request with missing left param returns 400
- [ ] Integration test: request with non-existent SBOM ID returns 404
- [ ] Integration test: compare two identical SBOMs returns all-empty diff sections

## Verification Commands
- `cargo test -p tests -- api::sbom_compare` -- all comparison endpoint integration tests pass
- `cargo check --workspace` -- no compilation errors across the workspace

## Dependencies
- Depends on: Task 3 -- SBOM comparison endpoint
