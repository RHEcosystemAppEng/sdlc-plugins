# Task 4 -- Add integration tests for license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license report endpoint (`GET /api/v2/sbom/{id}/license-report`). These tests exercise the full stack from HTTP request through service logic to database queries, verifying correct behavior for compliant SBOMs, non-compliant SBOMs, transitive dependencies, and edge cases. This ensures the license compliance report feature (TC-9004) works correctly end-to-end.

## Files to Create
- `tests/api/license_report.rs` -- Integration tests for the license report endpoint, following the pattern in existing test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`)

## Files to Modify
- `tests/Cargo.toml` -- Add any necessary test dependencies (if not already present)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/` -- see `sbom.rs` for how tests are structured: setup test data, make HTTP requests, assert on response status and body.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in the test suite.
- Tests should hit a real PostgreSQL test database, consistent with the project's integration test approach.
- Set up test fixtures:
  - An SBOM with packages having only compliant licenses (e.g., all MIT)
  - An SBOM with packages having at least one non-compliant license
  - An SBOM with transitive dependencies that have different licenses than direct dependencies
  - An SBOM with no packages (edge case)
- Each test should verify the response JSON structure matches `{ groups: [{ license: String, packages: [...], compliant: bool }] }`.
- Per CONVENTIONS.md (repository conventions): follow the integration test patterns in `tests/api/`.
  Applies: task creates `tests/api/license_report.rs` matching the convention's Rust test file scope.
- Test the CI/CD pipeline use case: verify that the response can be programmatically checked for any `compliant: false` groups (UC-2 from the feature description).

## Reuse Candidates
- `tests/api/sbom.rs` -- Existing SBOM integration tests; follow the same setup, request, and assertion patterns.
- `tests/api/advisory.rs` -- Another integration test file; reference for additional assertion and fixture patterns.

## Acceptance Criteria
- [ ] Integration tests exist for the license report endpoint covering happy path and error cases
- [ ] Tests verify the JSON response structure matches the expected schema
- [ ] Tests verify compliant and non-compliant license flagging
- [ ] Tests verify transitive dependency license inclusion
- [ ] Tests verify 404 response for non-existent SBOM IDs
- [ ] All tests pass in the CI environment

## Test Requirements
- [ ] Integration test: SBOM with all-compliant licenses returns all groups with `compliant: true`
- [ ] Integration test: SBOM with a non-compliant license returns at least one group with `compliant: false`
- [ ] Integration test: SBOM with transitive dependencies includes transitive package licenses in the report
- [ ] Integration test: non-existent SBOM ID returns 404 status
- [ ] Integration test: SBOM with no packages returns an empty groups array
- [ ] Integration test: response JSON structure matches the documented API contract

## Verification Commands
- `cargo test --test api -- license_report` -- Run only the license report integration tests
- `cargo test` -- Run the full test suite to verify no regressions

## Dependencies
- Depends on: Task 3 -- Add license report endpoint

<!-- [sdlc-workflow] Description digest: sha256-md:3a64bde22c084791c225b2977d7f2ca082ba2010e4944ccc5b80a15ce09a70f7 -->
