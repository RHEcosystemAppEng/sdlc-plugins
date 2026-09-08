## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license report endpoint covering various scenarios: SBOMs with multiple license types, policy violations, transitive dependency inclusion, and edge cases (empty SBOMs, missing license data, non-existent SBOM IDs).

## Files to Create
- `tests/api/license_report.rs` -- integration tests for the GET /api/v2/sbom/{id}/license-report endpoint

## Implementation Notes
- Follow the testing patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup, database fixture creation, and assertion patterns
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code checks as per project convention
- Tests hit a real PostgreSQL test database -- set up test fixtures with SBOMs, packages, package-license mappings, and a test license policy
- Test both compliant and non-compliant license scenarios to verify the policy checking logic end-to-end
- Test the transitive dependency walk by setting up a multi-level dependency chain (package A depends on B which depends on C)
- Per CONVENTIONS.md Testing: use the `assert_eq!(resp.status(), StatusCode::OK)` pattern and integration tests hitting a real PostgreSQL test database.
  Applies: task creates `tests/api/license_report.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- existing SBOM integration tests showing test setup patterns, fixture creation, and assertion conventions
- `tests/api/advisory.rs` -- another example of integration test patterns with different entity types

## Acceptance Criteria
- [ ] Integration test: SBOM with all compliant licenses returns report where all groups have `compliant: true`
- [ ] Integration test: SBOM with non-compliant license returns report where at least one group has `compliant: false`
- [ ] Integration test: SBOM with transitive dependencies includes all transitive packages in the report
- [ ] Integration test: SBOM with no packages returns 200 with empty groups array
- [ ] Integration test: non-existent SBOM ID returns appropriate error status
- [ ] Integration test: SBOM with packages missing license data groups them under "Unknown"

## Test Requirements
- [ ] All tests pass against a real PostgreSQL test database
- [ ] Tests create and clean up their own test fixtures
- [ ] Tests cover the full license compliance check flow: ingest SBOM with packages and licenses, configure policy, call endpoint, verify report structure and compliance flags

## Verification Commands
- `cargo test --test api` -- run the full integration test suite
- `cargo test license_report` -- run license report tests specifically

## Dependencies
- Depends on: Task 3 -- Add GET /api/v2/sbom/{id}/license-report endpoint
