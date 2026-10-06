## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint (`GET /api/v2/sbom/{id}/license-report`). Tests cover the full request-response cycle against a real PostgreSQL test database, validating correct license grouping, compliance flag computation, transitive dependency inclusion, and error handling.

## Files to Create
- `tests/api/license_report.rs` -- integration tests for the license report endpoint

## Files to Modify
- `tests/Cargo.toml` -- add the new test module if test modules require explicit registration

## Implementation Notes
- Follow the integration test patterns in `tests/api/sbom.rs` (SBOM endpoint tests) and `tests/api/advisory.rs` (advisory endpoint tests) for test setup, database fixtures, HTTP client usage, and assertion style.
- Per CONVENTIONS.md Testing: integration tests hit a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
  Applies: task creates `tests/api/license_report.rs` matching the convention's integration test file scope.
- Test scenarios should cover:
  1. SBOM with packages having multiple distinct licenses -- verify correct grouping
  2. SBOM with packages having policy-allowed licenses -- verify `compliant: true`
  3. SBOM with packages having policy-denied licenses -- verify `compliant: false`
  4. SBOM with transitive dependencies -- verify indirect packages appear in the report
  5. SBOM with no packages -- verify empty groups response
  6. Non-existent SBOM ID -- verify 404 response
  7. Large SBOM (up to 1000 packages if feasible) -- verify response time is reasonable
- Set up test fixtures by ingesting test SBOMs with known package-license relationships before running the report endpoint.

### Constraints (from docs/constraints.md)
- SS5.1: Keep changes scoped to the files listed in Files to Modify and Files to Create.
- SS5.2: Inspect existing test files before writing to follow established patterns.
- SS5.11: Add a doc comment to every test function.
- SS5.12: Add given-when-then inline comments to non-trivial test functions.
- SS2.1: Commit must reference Jira issue ID in footer.
- SS2.2: Use Conventional Commits format.

## Reuse Candidates
- `tests/api/sbom.rs` -- SBOM endpoint integration test patterns for test setup, database fixtures, and assertion style
- `tests/api/advisory.rs` -- advisory endpoint integration test patterns for reference

## Acceptance Criteria
- [ ] Integration tests for all scenarios listed above pass against a PostgreSQL test database
- [ ] Tests verify HTTP status codes (200, 404) and response body structure
- [ ] Tests verify license grouping correctness (packages grouped by license identifier)
- [ ] Tests verify compliance flag accuracy against the configured license policy
- [ ] Tests verify transitive dependencies are included in the report
- [ ] All test functions have doc comments

## Test Requirements
- [ ] Test: SBOM with mixed licenses produces correct groups with accurate compliance flags
- [ ] Test: SBOM with only allowed licenses returns all groups as compliant
- [ ] Test: SBOM with denied licenses returns non-compliant groups
- [ ] Test: transitive dependency licenses appear in the report
- [ ] Test: empty SBOM returns 200 with empty groups array
- [ ] Test: non-existent SBOM ID returns 404
- [ ] Test: large SBOM (1000 packages) completes within performance bounds

## Verification Commands
- `cargo test -p trustify-tests -- license_report` -- run all license report integration tests

## Dependencies
- Depends on: Task 4 -- Add license report REST endpoint
