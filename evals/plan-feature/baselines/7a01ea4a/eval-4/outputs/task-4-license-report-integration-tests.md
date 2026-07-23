# Task 4 — Add integration tests for license report endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. The tests verify the complete request-response cycle against a real PostgreSQL test database, covering the happy path, policy violation detection, transitive dependency inclusion, error handling, and performance characteristics for large SBOMs.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for the license report endpoint covering all acceptance criteria

## Files to Modify
- `tests/Cargo.toml` — Add the test module if not auto-discovered; ensure test dependencies include the fundamental and common crates

## Implementation Notes
- Follow the established integration test pattern in `tests/api/sbom.rs` for test structure: set up test database, seed SBOM and package data, make HTTP requests, assert response status and body.
  Applies: task creates `tests/api/license_report.rs` matching the convention's `.rs` file scope.
- Per project conventions (§Testing): use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status assertions. Tests hit a real PostgreSQL test database.
  Applies: task creates `tests/api/license_report.rs` matching the convention's integration test scope.
- Test scenarios should include:
  1. **Happy path**: SBOM with packages under MIT, Apache-2.0 licenses — all compliant per default policy
  2. **Policy violation**: SBOM with a package under a denied license (e.g., GPL-3.0 on a deny list) — verify `compliant: false` flag
  3. **Transitive dependencies**: SBOM with a package that has transitive dependencies with their own licenses — verify all are included in the report
  4. **Mixed compliance**: SBOM with both compliant and non-compliant license groups — verify each group has the correct flag
  5. **Empty SBOM**: SBOM with no packages — verify empty groups array
  6. **Non-existent SBOM**: Request with invalid ID — verify 404 response
  7. **Performance**: SBOM with 1000 packages — verify response time is under 500ms (p95 target from NFR)

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM integration tests; follow the same test setup, database seeding, and assertion patterns
- `tests/api/advisory.rs` — Additional reference for integration test patterns with related entities

## Acceptance Criteria
- [ ] All test scenarios pass against the PostgreSQL test database
- [ ] Tests verify the complete request-response cycle (HTTP request to JSON response)
- [ ] Tests cover both success (200) and error (404) responses
- [ ] Tests validate the JSON response shape matches the `LicenseReport` contract
- [ ] Tests verify compliance flags are correctly set based on the license policy
- [ ] Tests verify transitive dependency licenses are included

## Test Requirements
- [ ] Integration test: happy path — valid SBOM returns 200 with correct license groups
- [ ] Integration test: policy violation — denied license is flagged as non-compliant
- [ ] Integration test: transitive dependencies — all dependency licenses appear in the report
- [ ] Integration test: mixed compliance — groups have correct individual compliance flags
- [ ] Integration test: empty SBOM — returns 200 with empty groups array
- [ ] Integration test: non-existent SBOM — returns 404
- [ ] Performance test: SBOM with 1000 packages completes within 500ms

## Verification Commands
- `cargo test -p tests --test license_report` — all integration tests pass
- `cargo test -p tests` — full test suite passes (no regressions)

## Dependencies
- Depends on: Task 1 — Add license policy configuration file and loader
- Depends on: Task 2 — Create license report model structs and service with transitive dependency resolution
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/license-report endpoint
