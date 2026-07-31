## Repository
trustify-backend

## Target Branch
main

## Priority
Major

## Fix Versions
RHTPA 1.5.0

## Description
Add integration tests for the `GET /api/v2/sbom/{id}/license-report` endpoint. Tests verify end-to-end behavior against a real PostgreSQL test database, covering successful report generation, compliance policy enforcement, transitive dependency inclusion, and error cases.

## Files to Create
- `tests/api/license_report.rs` — Integration tests for the license report endpoint covering: basic report generation, policy-based compliance flagging, transitive dependency inclusion, missing SBOM 404 response, and performance characteristics

## Files to Modify
- `tests/Cargo.toml` — Add any necessary test dependencies if not already present

## Implementation Notes
Follow the integration test pattern in `tests/api/sbom.rs`. Tests should:

1. Set up test data by ingesting an SBOM with known packages and licenses
2. Optionally configure a license policy file for compliance-checking tests
3. Call `GET /api/v2/sbom/{id}/license-report` against the test server
4. Assert response status using `assert_eq!(resp.status(), StatusCode::OK)` pattern
5. Deserialize the response body and validate the report structure

Test cases:
- SBOM with packages under different licenses produces correct grouping
- Policy with denied licenses marks matching groups as non-compliant
- Report includes transitive dependency licenses (not just direct)
- Non-existent SBOM ID returns 404
- SBOM with no packages returns empty groups array

Per CONVENTIONS.md §Testing: use integration tests in `tests/api/` with real PostgreSQL test database and `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern. Applies: task creates `tests/api/license_report.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — Reference for test setup pattern, database fixtures, and HTTP client usage for SBOM-related endpoint tests

## Acceptance Criteria
- [ ] All integration tests pass against the PostgreSQL test database
- [ ] Tests cover successful report generation with correct license grouping
- [ ] Tests cover policy-based compliance flagging (both allow-list and deny-list)
- [ ] Tests cover transitive dependency inclusion
- [ ] Tests cover 404 response for non-existent SBOM
- [ ] Tests cover empty SBOM (no packages) edge case

## Test Requirements
- [ ] Integration test: SBOM with 3 packages under 2 licenses produces 2 groups with correct package counts
- [ ] Integration test: deny-list policy with "GPL-3.0" marks GPL-3.0 group as non-compliant
- [ ] Integration test: SBOM with transitive dependencies includes indirect package licenses
- [ ] Integration test: request for non-existent SBOM ID returns HTTP 404
- [ ] Integration test: SBOM with zero packages returns `{ "groups": [] }`

## Dependencies
- Depends on: Task 3 — Add license report endpoint
