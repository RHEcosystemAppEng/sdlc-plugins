## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add integration tests for the remediation API endpoints. Tests verify that both the summary and by-product endpoints return correct response shapes, proper aggregation results, and handle edge cases (empty data, pagination boundaries). Tests follow the established integration test pattern of hitting a real PostgreSQL test database.

## Files to Create
- `tests/api/remediation.rs` -- integration tests for GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product

## Files to Modify
- `tests/Cargo.toml` -- add remediation test module if test modules are registered explicitly

## Implementation Notes
- Follow the integration test pattern from `tests/api/sbom.rs` and `tests/api/advisory.rs`: tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` for status validation.
  - Applies: task creates `tests/api/remediation.rs` matching the convention's testing scope.
- Test setup should ingest sample SBOM and advisory data to create a known vulnerability-to-SBOM correlation state, then verify that the remediation endpoints return expected aggregation counts.
- Test cases for GET /api/v2/remediation/summary:
  - Verify response contains by_severity array with entries for each severity level
  - Verify totals (open + in_progress + resolved = total)
  - Verify response with no vulnerability data returns zero counts
- Test cases for GET /api/v2/remediation/by-product:
  - Verify response contains per-product entries with correct counts
  - Verify pagination (offset=0, limit=10 returns at most 10 items)
  - Verify total count reflects all products regardless of pagination
  - Verify response with no data returns empty items array and total=0
- Performance test: verify that the summary endpoint responds within 500ms for a dataset with seeded vulnerability records (per the p95 < 500ms non-functional requirement).

## Reuse Candidates
- `tests/api/sbom.rs` -- reference for integration test structure, test database setup, and assertion patterns
- `tests/api/advisory.rs` -- reference for advisory/vulnerability-related test data setup

## Acceptance Criteria
- [ ] Integration tests for summary endpoint verify correct severity x status grouping
- [ ] Integration tests for by-product endpoint verify per-product aggregation and pagination
- [ ] Edge case test verifies correct behavior with no vulnerability data
- [ ] All tests pass against a PostgreSQL test database
- [ ] Test for p95 < 500ms response time on summary endpoint with seeded data

## Test Requirements
- [ ] At least 6 test cases covering: summary happy path, summary empty data, summary totals consistency, by-product happy path, by-product pagination, by-product empty data
- [ ] Tests use real PostgreSQL test database (not mocks)
- [ ] Test data setup creates known vulnerability-SBOM correlations for deterministic assertions

## Verification Commands
- `cargo test --test api -- remediation` -- all remediation integration tests pass

## Dependencies
- Depends on: Task 2 -- Create remediation REST API endpoints

---
Description digest: sha256-md:49328fa73c56e6b5699d966c12547ea085b90d19ec1dd34cb84ec87f8a77e931
