## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the remediation REST endpoints (GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product) introduced in Task 2. The tests validate endpoint responses, pagination, error handling, and correctness of aggregation logic against a real PostgreSQL test database, following the established integration test patterns.

## Files to Create
- `tests/api/remediation.rs` — Integration tests for both remediation endpoints

## Files to Modify
- `tests/Cargo.toml` — Add test module reference if needed for the new remediation test file

## Implementation Notes
- Per CONVENTIONS.md §Testing: integration tests live in `tests/api/` and hit a real PostgreSQL test database; use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/remediation.rs` matching the convention's `.rs` test file scope.
- Reference `tests/api/advisory.rs` for the established integration test structure: test setup, data seeding, HTTP request execution, and response assertion patterns.
- Reference `tests/api/sbom.rs` for paginated endpoint test patterns.
- Tests should seed the database with known vulnerability and SBOM data to verify aggregation correctness:
  - Seed advisories with mixed severities (Critical, High, Medium, Low) and statuses (Open, In Progress, Resolved)
  - Seed multiple products with SBOMs linked to advisories
  - Verify summary counts match expected aggregation
  - Verify by-product breakdowns match per-product totals
- Test edge cases: empty database (no vulnerabilities), single product, all vulnerabilities resolved.

## Reuse Candidates
- `tests/api/advisory.rs` — Integration test patterns for advisory endpoints; reference for test setup and assertion style
- `tests/api/sbom.rs` — Integration test patterns for SBOM endpoints; reference for paginated response testing

## Acceptance Criteria
- [ ] Integration tests for GET /api/v2/remediation/summary verify correct aggregation by severity and status
- [ ] Integration tests for GET /api/v2/remediation/by-product verify correct per-product breakdown
- [ ] Integration tests for by-product endpoint verify pagination behavior
- [ ] Edge case test: empty database returns zero counts (not an error)
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Test summary endpoint returns correct severity x status matrix for seeded data
- [ ] Test by-product endpoint returns correct product-level counts for seeded data
- [ ] Test by-product endpoint pagination with offset and limit parameters
- [ ] Test summary endpoint with no vulnerability data returns empty/zero counts
- [ ] Test error handling for invalid query parameters

## Verification Commands
- `cargo test -p trustify-tests -- api::remediation` — All remediation integration tests pass

## Dependencies
- Depends on: Task 2 — Add remediation REST endpoints
