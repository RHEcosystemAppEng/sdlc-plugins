# Task 5 — Add integration tests for the license compliance report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint, covering compliant SBOMs, non-compliant SBOMs, transitive dependency scenarios, the automated CI/CD compliance gate use case, and edge cases. These tests hit a real PostgreSQL test database following the existing integration test patterns.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report`

## Files to Modify
- `tests/Cargo.toml` — Add the new test file to the test suite if required by the project's test configuration

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Use `assert_eq!(resp.status(), StatusCode::OK)` for success assertions
  - Use a real PostgreSQL test database (test fixtures set up and torn down per test)
  - Deserialize response bodies and assert on specific fields
- Test scenarios to cover:
  1. **All compliant**: Ingest an SBOM with packages that all have allowed licenses (e.g., MIT, Apache-2.0). Verify all groups have `compliant: true`.
  2. **Non-compliant detected**: Ingest an SBOM with a package under a denied license (e.g., GPL-3.0). Verify that group has `compliant: false` and `policy_status: "denied"`.
  3. **Transitive dependencies**: Ingest an SBOM with a dependency tree (A depends on B, B depends on C). Verify all three packages appear in the report and B/C are marked `transitive: true`.
  4. **Mixed compliance**: Ingest an SBOM with both allowed and denied licenses. Verify `compliant_count` and `non_compliant_count` are correct.
  5. **Empty SBOM**: Call the endpoint for an SBOM with no packages. Verify empty groups and zero counts.
  6. **Non-existent SBOM**: Call the endpoint with an invalid ID. Verify HTTP 404.
  7. **CI/CD gate scenario (UC-2)**: Verify that the response structure allows a pipeline to programmatically check for `compliant: false` in any group.
- Per `docs/constraints.md` section 5.9: prefer parameterized tests when multiple test cases exercise the same behavior with different inputs, if the project uses this pattern. Check sibling test files first (per section 5.10).
- Per `docs/constraints.md` section 5.11: add a doc comment to every test function.
- Per `docs/constraints.md` section 5.12: add given-when-then inline comments to non-trivial test functions.

## Reuse Candidates
- `tests/api/sbom.rs` — Follow the same test setup pattern (database fixtures, HTTP client configuration, assertion patterns)
- `tests/api/advisory.rs` — Reference for integration test structure with multiple test scenarios

## Acceptance Criteria
- [ ] All integration test scenarios pass against the test database
- [ ] Tests cover both success and error paths (valid SBOM, non-existent SBOM)
- [ ] Tests verify transitive dependency inclusion
- [ ] Tests verify compliance flag correctness for both allowed and denied licenses
- [ ] Tests verify response counts (total_packages, compliant_count, non_compliant_count)

## Test Requirements
- [ ] Integration test: all-compliant SBOM returns correct report with all groups compliant
- [ ] Integration test: SBOM with denied license returns non-compliant group
- [ ] Integration test: transitive dependencies are included and marked correctly
- [ ] Integration test: mixed compliance report has correct counts
- [ ] Integration test: empty SBOM returns empty report
- [ ] Integration test: non-existent SBOM returns 404
- [ ] Integration test: response structure supports CI/CD compliance gate use case

## Verification Commands
- `cargo test --test api -- license_report` — all license report integration tests pass

## Dependencies
- Depends on: Task 4 — Add GET /api/v2/sbom/{id}/license-report endpoint
