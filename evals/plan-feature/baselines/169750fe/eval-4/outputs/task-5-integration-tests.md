## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint. Tests should cover the full request-response cycle including database setup, SBOM ingestion with package licenses, policy configuration, and report generation. Tests verify both the happy path and edge cases.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — add test module if needed

## Implementation Notes
Follow the integration test pattern from `tests/api/sbom.rs` for test setup, database fixtures, and assertion style. Tests should:

1. Set up a test database with SBOM and package-license data
2. Configure a license policy (allow/deny specific licenses)
3. Call `GET /api/v2/sbom/{id}/license-report`
4. Assert response status and JSON body structure

Use the existing `assert_eq!(resp.status(), StatusCode::OK)` pattern from sibling test files.

Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database using the established test fixtures pattern.
Applies: task creates `tests/api/license_report.rs` matching the convention's Rust test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for SBOM-related test setup and assertion patterns
- `tests/api/advisory.rs` — reference for endpoint integration test structure

## Acceptance Criteria
- [ ] Test: valid SBOM with packages returns 200 with correct license grouping
- [ ] Test: SBOM with denied licenses returns report with `compliant: false`
- [ ] Test: SBOM with only allowed licenses returns report with `compliant: true`
- [ ] Test: non-existent SBOM ID returns 404
- [ ] Test: SBOM with transitive dependencies includes all transitive packages in the report
- [ ] Test: empty SBOM (no packages) returns empty report with `compliant: true`

## Test Requirements
- [ ] All tests pass against a real PostgreSQL test database
- [ ] Tests are independent and do not rely on ordering
- [ ] Test data includes packages with mixed license types (allowed, denied, review)

## Dependencies
- Depends on: Task 4 — License report endpoint
