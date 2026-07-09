## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license report endpoint that verify end-to-end behavior: SBOM ingestion with package license data, license policy evaluation, and correct report generation via the HTTP API. Tests follow the existing integration test patterns in `tests/api/`.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for `GET /api/v2/sbom/{id}/license-report` covering: successful report generation with multiple license types, compliance flag correctness, transitive dependency inclusion, 404 for nonexistent SBOMs, and performance within bounds for larger datasets

## Files to Modify
- `tests/Cargo.toml` — Add any required test dependencies if not already present

## Implementation Notes
- Follow the existing integration test pattern from `tests/api/sbom.rs`: set up a test PostgreSQL database, ingest test SBOM data with known package licenses, then call the endpoint and assert response structure and values
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern consistent with existing tests
- Create test fixtures with packages having a mix of allowed, denied, and review-required licenses to verify compliance grouping
- Include a test with transitive dependencies to verify the full dependency tree is included in the report
- Per CONVENTIONS.md Key Conventions (Testing): integration tests hit a real PostgreSQL test database. Follow the setup/teardown pattern used in `tests/api/sbom.rs`.
  Applies: task creates `tests/api/license_report.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM integration test file; follow its database setup pattern, test structure, and assertion style
- `tests/api/advisory.rs` — additional reference for integration test patterns

## Acceptance Criteria
- [ ] Integration test: successful license report for an SBOM with multiple license types returns correct grouping
- [ ] Integration test: compliance flags match the configured license policy (allowed = true, denied = false)
- [ ] Integration test: transitive dependencies appear in the report
- [ ] Integration test: nonexistent SBOM ID returns HTTP 404
- [ ] All existing tests continue to pass

## Test Requirements
- [ ] Test with an SBOM containing packages under MIT (allowed), GPL-3.0 (review_required), and a custom denied license — verify three groups with correct compliance flags
- [ ] Test with an SBOM containing transitive dependencies — verify all packages appear in the report, not just direct dependencies
- [ ] Test with a nonexistent SBOM ID — verify 404 response
- [ ] Test with an SBOM with no packages — verify empty groups list is returned

## Verification Commands
- `cargo test --test api` — all integration tests pass including new license report tests
- `cargo test --test api license_report` — run only the new license report tests

## Dependencies
- Depends on: Task 3 — Add license report endpoint
