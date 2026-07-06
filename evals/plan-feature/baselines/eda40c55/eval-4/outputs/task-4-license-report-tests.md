## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the license compliance report endpoint. Tests verify the full request-response cycle against a real PostgreSQL test database, covering compliant SBOMs, non-compliant SBOMs, transitive dependency inclusion, edge cases (empty SBOMs, missing license data), and the 404 response for non-existent SBOM IDs.

## Files to Create
- `tests/api/license_report.rs` — integration tests for GET /api/v2/sbom/{id}/license-report covering the full range of compliance scenarios

## Files to Modify
- `tests/Cargo.toml` — add the license_report test module if test modules require explicit registration

## Implementation Notes
- Follow the existing test pattern in `tests/api/sbom.rs` for:
  - Test database setup and teardown
  - HTTP client configuration
  - Response assertion patterns using `assert_eq!(resp.status(), StatusCode::OK)`
- Test scenarios to cover:
  1. SBOM with all packages under compliant licenses — verify all groups have `compliant: true`
  2. SBOM with packages under a denied license — verify the group has `compliant: false`
  3. SBOM with transitive dependencies — verify transitive packages appear in the report
  4. SBOM with packages missing license data — verify they are handled gracefully
  5. Non-existent SBOM ID — verify 404 response
  6. Empty SBOM (no packages) — verify empty groups array
- Set up test fixture data: ingest a test SBOM with known packages and licenses before running report tests
- Use a test license policy JSON file with known allowed/denied lists
- Per CONVENTIONS.md: integration tests hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/license_report.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — existing SBOM endpoint integration tests; follow the same setup, teardown, and assertion patterns
- `tests/api/advisory.rs` — additional reference for integration test structure and database fixture setup

## Acceptance Criteria
- [ ] All integration tests pass against a PostgreSQL test database
- [ ] Tests cover compliant, non-compliant, transitive, and edge case scenarios
- [ ] Tests verify correct HTTP status codes (200 for success, 404 for missing SBOM)
- [ ] Tests verify response body structure matches the LicenseReport schema

## Test Requirements
- [ ] Integration test: SBOM with compliant licenses returns all groups with compliant=true
- [ ] Integration test: SBOM with denied license returns group with compliant=false
- [ ] Integration test: transitive dependencies appear in report groups
- [ ] Integration test: packages with no license data are handled without error
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: SBOM with no packages returns empty groups array

## Verification Commands
- `cargo test --test api -- license_report` — run all license report integration tests

## Dependencies
- Depends on: Task 1 — Add license policy configuration model
- Depends on: Task 2 — Add license report model and service
- Depends on: Task 3 — Add license report REST endpoint
