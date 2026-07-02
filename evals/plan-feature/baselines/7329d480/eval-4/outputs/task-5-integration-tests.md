## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. Tests should cover the primary use cases: generating a report for an SBOM with mixed license compliance, handling SBOMs with no packages, and returning 404 for non-existent SBOMs.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — Add test module reference if required by the test harness configuration

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` which tests the SBOM endpoints against a real PostgreSQL test database. Use the same test setup, database seeding, and assertion patterns.
- Test fixture data should include: (1) an SBOM with packages having a mix of approved (MIT, Apache-2.0), restricted (LGPL-2.1), and prohibited (GPL-3.0) licenses, (2) an SBOM with transitive dependencies, and (3) an SBOM with no packages.
- Per CONVENTIONS.md §Testing: use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions, and run tests against a real PostgreSQL test database. Applies: task creates `tests/api/license_report.rs` matching the convention's .rs scope.
- Per CONVENTIONS.md §Error handling: verify that error responses use the `AppError` format with appropriate status codes (404 for not found). Applies: task creates `tests/api/license_report.rs` matching the convention's .rs scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Pattern reference for SBOM endpoint integration test structure, test database setup, and assertion patterns
- `tests/api/advisory.rs` — Additional reference for integration test patterns

## Acceptance Criteria
- [ ] Test passes: SBOM with mixed licenses returns a report with correct compliance flags per group
- [ ] Test passes: approved licenses (MIT, Apache-2.0) have `compliant: true`
- [ ] Test passes: prohibited licenses (GPL-3.0) have `compliant: false`
- [ ] Test passes: transitive dependencies are included in the report with `transitive: true`
- [ ] Test passes: non-existent SBOM ID returns HTTP 404
- [ ] Test passes: SBOM with no packages returns an empty groups array

## Test Requirements
- [ ] Integration test: GET /api/v2/sbom/{id}/license-report with a seeded SBOM returns 200 with correctly grouped and flagged licenses
- [ ] Integration test: GET /api/v2/sbom/{id}/license-report with non-existent ID returns 404
- [ ] Integration test: report includes transitive dependencies with correct flag
- [ ] Integration test: unknown licenses (not in policy) are flagged as non-compliant
- [ ] Integration test: empty SBOM returns 200 with `{ groups: [] }`

## Verification Commands
- `cargo test --test api -- license_report` — All license report integration tests pass

## Dependencies
- Depends on: Task 4 — License report endpoint

## additional_fields
```json
{ "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```
