## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint. Tests exercise the full stack from HTTP request through service to database, verifying correct grouping, compliance flagging, transitive dependency handling, and error cases. Tests follow the existing integration test patterns using a real PostgreSQL test database.

## Files to Create
- `tests/api/license_report.rs` — integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` — add the new test module if needed

## Implementation Notes
Follow the existing integration test patterns from `tests/api/sbom.rs` and `tests/api/advisory.rs`. These tests use a real PostgreSQL test database and follow the `assert_eq!(resp.status(), StatusCode::OK)` pattern documented in the repository conventions.

Test setup should:
1. Ingest a test SBOM with known packages and licenses (some compliant, some non-compliant)
2. Configure a test license policy with specific allowed/denied licenses
3. Call the endpoint and verify the response structure and compliance flags

Test cases should cover:
- Happy path: SBOM with mixed compliant/non-compliant licenses
- All compliant: SBOM where all licenses are in the allowed list
- All non-compliant: SBOM where all licenses are in the denied list
- Transitive dependencies: verify they appear in the report with `transitive: true`
- Empty SBOM: SBOM with no packages returns empty groups
- Non-existent SBOM: returns 404
- CI/CD gate use case: verify the response structure supports automated compliance checking (check for `compliant: false` in any group)

Per CONVENTIONS.md §Testing: integration tests in tests/api/ hit a real PostgreSQL test database; use assert_eq!(resp.status(), StatusCode::OK) pattern.
Applies: task creates `tests/api/license_report.rs` matching the convention's `.rs` test scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration test patterns for test setup and assertion style
- `tests/api/advisory.rs` — existing advisory integration test patterns

## Acceptance Criteria
- [ ] At least 6 integration test cases covering the scenarios listed above
- [ ] Tests pass against a PostgreSQL test database
- [ ] Tests verify JSON response structure matches the LicenseReport contract
- [ ] Tests verify compliance flags are correctly derived from the license policy
- [ ] Tests verify transitive dependency inclusion

## Test Requirements
- [ ] Integration test: happy path with mixed compliant and non-compliant licenses
- [ ] Integration test: all compliant licenses return all groups with `compliant: true`
- [ ] Integration test: denied licenses return groups with `compliant: false`
- [ ] Integration test: transitive dependencies are included with `transitive: true`
- [ ] Integration test: empty SBOM returns 200 with empty groups array
- [ ] Integration test: non-existent SBOM ID returns 404

## Dependencies
- Depends on: Task 4 — License report endpoint

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}
