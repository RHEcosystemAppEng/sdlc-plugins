# Task 5 — Add integration tests for the SBOM comparison endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/compare` endpoint. These tests hit a real PostgreSQL test database and verify the full request-response cycle including correct diff computation, error handling for invalid inputs, and performance characteristics for large SBOMs.

## Files to Create
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## Files to Modify
- `tests/api/mod.rs` — Add `mod sbom_compare;` if a module declaration file exists (check existing test structure)

## Implementation Notes
- Follow the existing integration test pattern in `tests/api/sbom.rs` — use the same test database setup, HTTP client construction, and `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
- Set up test fixtures by ingesting two SBOMs with known differences:
  - SBOM A: packages [pkg-a@1.0, pkg-b@2.0, pkg-c@1.0] with advisories [ADV-001 affecting pkg-a]
  - SBOM B: packages [pkg-a@1.1, pkg-c@1.0, pkg-d@1.0] with advisories [ADV-002 affecting pkg-d]
  - Expected diff: added=[pkg-d], removed=[pkg-b], version_changes=[pkg-a 1.0->1.1 upgrade], new_vulnerabilities=[ADV-002], resolved_vulnerabilities=[ADV-001], license_changes=[] (if licenses are same)
- Test edge cases: identical SBOMs, completely disjoint SBOMs, single empty SBOM, non-existent IDs.
- Tests should verify the response body JSON structure matches `SbomComparisonResult` fields.

## Reuse Candidates
- `tests/api/sbom.rs` — Existing SBOM endpoint integration tests; follow the same setup and assertion patterns
- `tests/api/advisory.rs` — Advisory endpoint integration tests; reference for advisory test data setup

## Acceptance Criteria
- [ ] All integration tests pass against the test PostgreSQL database
- [ ] Tests cover the normal diff scenario with all six diff categories
- [ ] Tests cover error scenarios (missing params, non-existent IDs)
- [ ] Tests verify the JSON response shape matches the expected contract

## Test Requirements
- [ ] Test: compare SBOMs with added, removed, and version-changed packages — verify correct categorization
- [ ] Test: compare SBOMs with new and resolved vulnerabilities — verify correct advisory diff
- [ ] Test: compare SBOMs with license changes — verify license diff detection
- [ ] Test: compare identical SBOMs — verify all diff categories return empty arrays
- [ ] Test: call with missing query parameters — verify 400 status
- [ ] Test: call with non-existent SBOM ID — verify 404 status

## Verification Commands
- `cargo test --test api sbom_compare` — expected: all tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add GET /api/v2/sbom/compare endpoint
