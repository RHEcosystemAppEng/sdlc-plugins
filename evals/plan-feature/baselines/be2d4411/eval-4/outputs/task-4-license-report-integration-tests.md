## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license compliance report endpoint that verify end-to-end behavior against a real PostgreSQL test database. Tests cover compliant SBOMs, non-compliant license detection, transitive dependency inclusion, empty SBOMs, and the automated compliance gate use case (checking for `compliant: false` groups).

## Files to Create
- `tests/api/license_report.rs` — integration tests for GET /api/v2/sbom/{id}/license-report

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` — existing SBOM endpoint tests demonstrate the conventional approach for test database setup, HTTP client configuration, fixture data insertion, and response assertion using `assert_eq!(resp.status(), StatusCode::OK)`.
- Tests hit a real PostgreSQL test database, consistent with the testing convention documented in the repository. Set up test data by inserting SBOM, package, sbom_package, and package_license records that create known scenarios.
- Test scenarios should include:
  1. SBOM with all MIT-licensed packages (all compliant) — verify all groups have `compliant: true`
  2. SBOM with a GPL-3.0 package when policy denies GPL — verify the GPL group has `compliant: false`
  3. SBOM with transitive dependencies — verify all transitive packages appear in the report
  4. SBOM with no packages — verify empty groups array and zero summary counts
  5. Non-existent SBOM ID — verify 404 response
  6. Compliance gate scenario: verify response contains enough information for a CI pipeline to determine pass/fail by checking `summary.non_compliant_count > 0`
- Provide a test license policy JSON file as a fixture or construct it inline during test setup.
- Per docs/constraints.md section 5: follow established test patterns found in sibling test files.

## Reuse Candidates
- `tests/api/sbom.rs` — reference integration test implementation for SBOM endpoints; reuse test infrastructure setup (database connection, HTTP client, fixture loading)
- `tests/api/advisory.rs` — additional reference for integration test patterns
- `entity/src/package_license.rs` — entity for inserting test package-license data

## Acceptance Criteria
- [ ] All six test scenarios pass against a PostgreSQL test database
- [ ] Tests verify both the HTTP status code and the response body structure
- [ ] Tests verify the `compliant` flag logic for both allowed and denied licenses
- [ ] Tests verify transitive dependency inclusion in the report
- [ ] Tests verify the summary counts (total_packages, compliant_count, non_compliant_count) are accurate

## Test Requirements
- [ ] Integration test: SBOM with all compliant licenses returns 200 with all groups compliant
- [ ] Integration test: SBOM with non-compliant license returns 200 with group marked non-compliant
- [ ] Integration test: SBOM with transitive dependencies includes all packages
- [ ] Integration test: empty SBOM returns 200 with empty groups
- [ ] Integration test: non-existent SBOM returns 404
- [ ] Integration test: response structure supports automated compliance gate (non_compliant_count field present)

## Verification Commands
- `cargo test --test api -- license_report` — all integration tests pass

## Documentation Updates
- `README.md` — add the license report endpoint to the API reference section, documenting the request path, response shape, and license policy configuration

## Dependencies
- Depends on: Task 3 — Add license report endpoint (GET /api/v2/sbom/{id}/license-report route)

[sdlc-workflow] Description digest: sha256-md:c4d6cfbcde8208ad9cfdbc036658e4498d8eeb8e9f18b8e2dd7b2120fe87416b
