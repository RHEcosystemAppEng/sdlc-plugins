## Repository
trustify-backend

## Target Branch
main

## Description
Add comprehensive integration tests for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. These tests verify the full request-response cycle against a real PostgreSQL test database, covering success cases, error cases, severity counting accuracy, deduplication, caching headers, and threshold filtering.

## Files to Create
- `tests/api/advisory_summary.rs` — integration tests for the advisory-summary endpoint

## Files to Modify
- `tests/Cargo.toml` — add any additional test dependencies if needed (likely none — existing test infrastructure should suffice)

## Implementation Notes
Follow the existing integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`:

1. Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for response status checks
2. Tests run against a real PostgreSQL test database (not mocks)
3. Test setup should:
   - Create a test SBOM
   - Ingest test advisories with known severities (e.g., 2 critical, 3 high, 1 medium, 0 low)
   - Link advisories to the SBOM via `sbom_advisory` join records

Test cases to implement:
- **Success case**: GET with valid SBOM ID returns 200 with correct severity counts
- **404 case**: GET with non-existent SBOM ID returns 404
- **Deduplication**: Link same advisory twice, verify it counts as 1
- **Empty case**: SBOM with zero advisories returns all zeros
- **Threshold filter**: `?threshold=high` returns only critical + high counts (medium and low are 0)
- **Cache headers**: Response includes `cache-control` header with max-age=300

Reference the test file structure in `tests/api/sbom.rs` for test setup boilerplate (database connection, test app initialization).

## Reuse Candidates
- `tests/api/sbom.rs` — test setup patterns for SBOM-related endpoint tests
- `tests/api/advisory.rs` — test setup patterns for advisory data creation

## Acceptance Criteria
- [ ] All test cases pass against a PostgreSQL test database
- [ ] Tests cover: success (200), not found (404), deduplication, empty SBOM, threshold filtering, cache headers
- [ ] Test file follows existing test organization in `tests/api/`
- [ ] Tests are deterministic and can run in CI

## Test Requirements
- [ ] Integration test: valid SBOM returns 200 with correct `{ critical, high, medium, low, total }` counts
- [ ] Integration test: non-existent SBOM returns 404
- [ ] Integration test: duplicate advisory links are deduplicated (counted once)
- [ ] Integration test: SBOM with no advisories returns `{ critical: 0, high: 0, medium: 0, low: 0, total: 0 }`
- [ ] Integration test: `?threshold=high` returns critical and high counts with medium and low as 0
- [ ] Integration test: response contains cache-control header with 300-second max-age

## Dependencies
- Depends on: Task 3 — Add advisory-summary endpoint with caching

## additional_fields
- priority: Major
- fixVersions: RHTPA 1.5.0