# Task 5 -- Add license report integration tests

**Summary:** Add integration tests for license compliance report endpoint

**Priority:** Major
**Fix Versions:** RHTPA 1.5.0
**Labels:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint covering the key use cases: compliant SBOM, non-compliant licenses, transitive dependency handling, empty SBOM, and performance with larger SBOMs. These tests validate the end-to-end behavior from HTTP request through service logic to database queries.

## Files to Create
- `tests/api/license_report.rs` -- integration tests for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `tests/Cargo.toml` -- add the new test file to the test configuration if required by the test harness setup

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/` -- see `sbom.rs` for the test setup, database fixture loading, HTTP request pattern, and assertion style
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in sibling tests
- Tests must hit a real PostgreSQL test database, consistent with the project's testing approach
- Test scenarios to implement:
  1. **Compliant SBOM**: ingest an SBOM where all packages have allowed licenses, verify all groups have `compliant: true`
  2. **Non-compliant licenses**: ingest an SBOM with packages using denied licenses, verify the affected groups have `compliant: false`
  3. **Mixed compliance**: ingest an SBOM with both compliant and non-compliant licenses, verify correct flags per group
  4. **Transitive dependencies**: ingest an SBOM with a dependency tree, verify transitive dependency licenses appear in the report
  5. **Empty SBOM**: request a report for an SBOM with no packages, verify empty groups array
  6. **Non-existent SBOM**: request a report for an invalid SBOM ID, verify 404 response
- For the automated compliance gate use case (UC-2), include a test that verifies the response structure allows a CI/CD pipeline to check for `compliant: false` in any group
- Per CONVENTIONS.md (Key Conventions -- Testing): integration tests in `tests/api/` hit a real PostgreSQL test database. Applies: task creates `tests/api/license_report.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- reference for SBOM integration test patterns, fixture loading, and HTTP assertion style
- `tests/api/advisory.rs` -- reference for additional assertion patterns
- `modules/ingestor/src/graph/sbom/mod.rs` -- SBOM ingestion module for setting up test fixtures

## Acceptance Criteria
- [ ] All integration test scenarios pass against the test database
- [ ] Tests cover both compliant and non-compliant license scenarios
- [ ] Tests verify transitive dependency inclusion
- [ ] Tests verify correct HTTP status codes (200 for valid, 404 for invalid SBOM ID)
- [ ] Tests validate the response JSON structure matches the expected shape

## Test Requirements
- [ ] Integration test: compliant SBOM returns all groups with `compliant: true`
- [ ] Integration test: non-compliant SBOM returns affected groups with `compliant: false`
- [ ] Integration test: mixed compliance SBOM returns correct per-group flags
- [ ] Integration test: transitive dependencies are included in the report
- [ ] Integration test: empty SBOM returns empty groups
- [ ] Integration test: non-existent SBOM ID returns 404

## Verification Commands
- `cargo test --test api license_report` -- run all license report integration tests (expected: all pass)
- `cargo test --test api` -- run full API integration test suite (expected: no regressions)

## Dependencies
- Depends on: Task 4 -- Add license report endpoint
