## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint, covering the main use cases: generating a report for an SBOM with mixed licenses, verifying compliance flags, testing the CI/CD gate scenario, and ensuring proper error handling.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report` covering success, error, and compliance scenarios

## Files to Modify
- `tests/Cargo.toml` — Add any necessary test dependencies if not already present

## Implementation Notes
Follow the integration test pattern from `tests/api/sbom.rs` and `tests/api/advisory.rs`. Tests should hit a real PostgreSQL test database. Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in the codebase. Set up test data by ingesting an SBOM with packages that have known licenses (mix of compliant and non-compliant). Test scenarios:
1. SBOM with all compliant licenses — all groups have `compliant: true`
2. SBOM with a non-compliant license — at least one group has `compliant: false`
3. CI/CD gate scenario — verify the response allows programmatic checking of `compliant` field
4. Nonexistent SBOM ID — returns 404
5. SBOM with transitive dependencies — all dependency levels included in report

## Reuse Candidates
- `tests/api/sbom.rs` — Test setup patterns, SBOM ingestion helpers, assertion style
- `tests/api/advisory.rs` — Additional integration test patterns

## Acceptance Criteria
- [ ] At least 5 test cases covering success, error, and edge case scenarios
- [ ] Tests verify response status codes and JSON body structure
- [ ] Tests verify compliance flag accuracy against known license inputs
- [ ] Tests use real PostgreSQL test database following existing test patterns

## Test Requirements
- [ ] Test: valid SBOM with mixed licenses returns correct groups and compliance flags
- [ ] Test: all-compliant SBOM returns all groups with compliant=true
- [ ] Test: SBOM with denied license returns group with compliant=false
- [ ] Test: nonexistent SBOM returns 404
- [ ] Test: report includes transitive dependency packages

## Dependencies
- Depends on: Task 4 — License report endpoint (endpoint must exist to test)
