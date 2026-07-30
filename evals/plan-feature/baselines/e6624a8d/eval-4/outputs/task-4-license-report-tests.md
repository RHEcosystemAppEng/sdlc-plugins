## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the license report endpoint that verify end-to-end behavior against a real PostgreSQL test database. Tests cover the happy path (valid SBOM with mixed licenses), edge cases (empty SBOM, non-existent SBOM), compliance evaluation (flagging non-compliant licenses), and transitive dependency inclusion. These tests serve as the automated compliance gate verification described in UC-2.

## Files to Create
- `tests/api/license_report.rs` — Integration test module with test cases for the license report endpoint

## Files to Modify
- `tests/api/mod.rs` — Add `mod license_report;` to register the new test module (if a mod.rs exists; otherwise the test is auto-discovered by Cargo)

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` — use the same test database setup, HTTP client initialization, and assertion patterns
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern per project conventions
- Seed test data: ingest an SBOM with packages that have known licenses (mix of compliant and non-compliant per the default policy) to verify grouping and compliance flagging
- Include a test for transitive dependencies: seed an SBOM with a dependency tree where a transitive dependency has a non-compliant license and verify it appears in the report
- Test the CI/CD gate use case (UC-2): verify the response structure allows a pipeline to programmatically check for `compliant: false` groups
- Per docs/constraints.md section 5 (Code Change Rules): changes must be scoped to listed files; inspect code before modifying
- Per CONVENTIONS.md -- Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task creates `tests/api/license_report.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — established integration test pattern for SBOM endpoints (test setup, database seeding, HTTP assertions)
- `tests/api/advisory.rs` — additional reference for endpoint integration test structure

## Acceptance Criteria
- [ ] Integration tests pass against a PostgreSQL test database
- [ ] Happy path test: valid SBOM returns 200 with grouped license data
- [ ] Edge case test: non-existent SBOM returns 404
- [ ] Compliance test: non-compliant licenses are flagged with `compliant: false`
- [ ] Transitive dependency test: transitive deps appear in the license report

## Test Requirements
- [ ] Test: GET /api/v2/sbom/{id}/license-report with a valid SBOM containing packages with MIT and GPL-3.0 licenses returns groups with correct compliance flags
- [ ] Test: GET /api/v2/sbom/{id}/license-report with a non-existent UUID returns 404
- [ ] Test: SBOM with only compliant licenses returns all groups with `compliant: true`
- [ ] Test: SBOM with transitive dependency having a non-compliant license includes that dependency in the flagged group
- [ ] Test: empty SBOM (no packages) returns an empty groups array

## Verification Commands
- `cargo test --test api license_report` — runs all license report integration tests

## Dependencies
- Depends on: Task 3 — Add license report endpoint
