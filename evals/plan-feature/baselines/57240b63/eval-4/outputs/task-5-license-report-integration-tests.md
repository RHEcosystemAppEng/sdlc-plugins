## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint. Tests verify the full request-response cycle against a real PostgreSQL test database, covering successful report generation, compliance flagging, transitive dependency inclusion, and error cases.

## Files to Create
- `tests/api/license_report.rs` -- integration tests for GET /api/v2/sbom/{id}/license-report

## Files to Modify
- `tests/Cargo.toml` -- add test module declaration and any required dependencies for the license report tests

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs` for test setup, HTTP client configuration, test database provisioning, and assertion patterns.
- Each test should:
  1. Set up test data by ingesting an SBOM with known packages and license mappings using the existing ingestion test utilities.
  2. Configure a test license policy (create a temporary JSON policy file with known allowed/denied licenses).
  3. Make an HTTP GET request to `/api/v2/sbom/{id}/license-report`.
  4. Assert the response status code and body structure.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status assertions, consistent with existing integration tests.
- Test cases to implement:
  - **All compliant**: SBOM where all package licenses are in the allowed list -> `report.compliant == true`, all groups have `compliant: true`
  - **Non-compliant detected**: SBOM with at least one package using a denied license -> `report.compliant == false`, the violating group has `compliant: false`
  - **Transitive dependencies**: SBOM with transitive dependency chain -> all transitive packages appear in the report's license groups
  - **Not found**: Request with non-existent SBOM ID -> HTTP 404 response
  - **Empty SBOM**: SBOM with no packages -> empty `groups` array, `compliant: true`

- Per CONVENTIONS.md §Testing: use integration tests against a real PostgreSQL test database with the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
  Applies: task creates `tests/api/license_report.rs` matching the convention's integration test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` -- reference for test setup, SBOM ingestion helpers, HTTP request construction, and response assertion patterns
- `tests/api/advisory.rs` -- reference for test structure, database fixture setup, and cleanup patterns

## Acceptance Criteria
- [ ] Integration test verifies HTTP 200 response with correct LicenseReport JSON for a valid SBOM
- [ ] Integration test verifies compliance flags are set correctly based on the license policy
- [ ] Integration test verifies transitive dependencies are included in the report groups
- [ ] Integration test verifies HTTP 404 response for a non-existent SBOM ID
- [ ] Integration test verifies empty SBOM returns empty groups with compliant: true
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Test: compliant SBOM returns report with `compliant: true` and all groups marked compliant
- [ ] Test: SBOM with denied license returns report with `compliant: false` and the violating group flagged
- [ ] Test: SBOM with transitive dependencies includes all transitive packages in license groups
- [ ] Test: non-existent SBOM ID returns HTTP 404
- [ ] Test: SBOM with no packages returns empty groups and `compliant: true`

## Verification Commands
- `cargo test -p trustify-tests --test license_report` -- expected: all integration tests pass

## Dependencies
- Depends on: Task 4 -- License report endpoint and route registration

---

[sdlc-workflow] Description digest: sha256-md:2582d777425e6ea8b607d02b69df472200b16ad81cfc2dd56ab4b6c2b0174909
