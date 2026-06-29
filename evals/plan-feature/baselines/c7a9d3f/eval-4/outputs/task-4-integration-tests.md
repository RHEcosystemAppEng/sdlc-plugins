# Task 4 — Add comprehensive integration tests for license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add end-to-end integration tests for the license compliance report endpoint that exercise the full flow: ingest an SBOM with known packages and licenses, configure a license policy, call the endpoint, and validate the response structure and compliance flags. Cover edge cases including SBOMs with only compliant licenses, SBOMs with non-compliant licenses, SBOMs with transitive dependencies, and the automated compliance gate use case (CI/CD pipeline checking for `compliant: false`).

## Files to Modify
- `tests/Cargo.toml` — add any necessary test dependencies if not already present

## Files to Create
- `tests/api/license_report.rs` — integration test module with test functions covering the license report endpoint

## Implementation Notes
- Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` — these tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Set up test data by ingesting an SBOM with known packages and license mappings, then call `GET /api/v2/sbom/{id}/license-report`
- Test with a policy that allows MIT and Apache-2.0 but denies GPL-3.0, and verify the compliance flags in the response
- Include a test case that verifies transitive dependencies are present in the report and correctly marked
- Include a test for the compliance gate use case: parse the response and assert that `groups.iter().any(|g| !g.compliant)` returns `true` when non-compliant licenses are present
- Performance consideration: include a test comment noting the p95 < 500ms target for SBOMs with up to 1000 packages, though the test database may not have that volume

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration tests; follow the same test setup, HTTP client patterns, and assertion style
- `tests/api/advisory.rs` — existing advisory integration tests; follow for additional patterns on response deserialization

## Acceptance Criteria
- [ ] Integration tests cover the happy path (compliant SBOM), non-compliant path, and transitive dependency path
- [ ] All tests pass against the PostgreSQL test database
- [ ] Tests validate the exact JSON response structure including `groups`, `license`, `packages`, and `compliant` fields
- [ ] Tests verify that the compliance gate use case works (programmatic check for non-compliant groups)

## Test Requirements
- [ ] Integration test: SBOM with all MIT packages returns a report where all groups are `compliant: true`
- [ ] Integration test: SBOM with a GPL-3.0 package returns a report where the GPL-3.0 group is `compliant: false`
- [ ] Integration test: SBOM with transitive dependencies includes those packages with `transitive: true`
- [ ] Integration test: empty SBOM returns an empty `groups` array
- [ ] Integration test: programmatic compliance gate check correctly identifies non-compliant SBOMs

## Verification Commands
- `cargo test --test api license_report` — expected: all tests pass

## Dependencies
- Depends on: Task 3 — Add license report REST endpoint
