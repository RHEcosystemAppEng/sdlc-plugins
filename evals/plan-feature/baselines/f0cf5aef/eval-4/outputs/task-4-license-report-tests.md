## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint (`GET /api/v2/sbom/{id}/license-report`). Tests verify the complete flow: ingesting an SBOM with package license data, calling the report endpoint, and validating the grouped response with compliance flags. Tests cover both compliant and non-compliant scenarios, transitive dependency inclusion, and error cases.

## Files to Modify
- `tests/Cargo.toml` — add any new test dependencies if needed (e.g., test fixture helpers)

## Files to Create
- `tests/api/license_report.rs` — integration tests for the license report endpoint

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` — tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Test setup should ingest an SBOM with known package license data, then call the license report endpoint and verify the response.
- Include test cases for: (1) SBOM with multiple licenses grouped correctly, (2) policy violation detection, (3) transitive dependency inclusion, (4) empty SBOM, (5) non-existent SBOM ID returns 404.
- Use the existing test infrastructure patterns from `tests/api/sbom.rs` and `tests/api/advisory.rs`.
- Per CONVENTIONS.md Key Conventions: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/license_report.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for SBOM integration test patterns, test setup, and fixture ingestion
- `tests/api/advisory.rs` — reference for API endpoint testing patterns
- `tests/api/search.rs` — reference for response body assertion patterns

## Acceptance Criteria
- [ ] Integration test verifies `GET /api/v2/sbom/{id}/license-report` returns 200 for an SBOM with package data
- [ ] Integration test verifies packages are grouped by license identifier
- [ ] Integration test verifies `compliant` flag is `false` for denied licenses
- [ ] Integration test verifies `compliant` flag is `true` for allowed licenses
- [ ] Integration test verifies transitive dependencies appear in the report
- [ ] Integration test verifies 404 response for non-existent SBOM ID
- [ ] Integration test verifies empty response for SBOM with no packages
- [ ] All tests pass with `cargo test --test api`

## Test Requirements
- [ ] Test case: SBOM with packages using MIT, Apache-2.0, and GPL-3.0 licenses returns three groups
- [ ] Test case: Policy denying GPL-3.0 results in that group having `compliant: false`
- [ ] Test case: Policy allowing only MIT and Apache-2.0 results in GPL-3.0 group having `compliant: false`
- [ ] Test case: SBOM with transitive dependencies includes those dependencies' licenses in the report
- [ ] Test case: Non-existent SBOM ID returns HTTP 404
- [ ] Test case: SBOM with no packages returns an empty groups array

## Verification Commands
- `cargo test --test api -- license_report` — runs all license report integration tests, expecting all to pass

## Dependencies
- Depends on: Task 3 — Add license report endpoint
