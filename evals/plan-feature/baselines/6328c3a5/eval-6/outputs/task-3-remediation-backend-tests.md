## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the remediation REST endpoints. Tests should hit a real PostgreSQL test database following the established integration test pattern, verifying that the summary and by-product endpoints return correct aggregated data from seeded vulnerability-SBOM relationships.

## Files to Create
- `tests/api/remediation.rs` — integration tests for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`

## Files to Modify
- `tests/Cargo.toml` — add remediation test module if test modules are registered explicitly

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` and `tests/api/advisory.rs`. Tests should:
  1. Set up test database state with known vulnerability-SBOM relationships across multiple severities, statuses, and products
  2. Call the endpoint via the test HTTP client
  3. Assert response status and JSON body structure
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern per Key Conventions.
  Applies: task creates `tests/api/remediation.rs` matching the convention's `.rs` file scope.
- Seed test data that covers edge cases:
  - Products with zero vulnerabilities (should appear with all counts = 0 or be omitted)
  - All four severity levels (Critical, High, Medium, Low)
  - All three status values (Open, In Progress, Resolved)
  - Multiple products for by-product breakdown validation
- Verify the p95 < 500ms non-functional requirement is achievable by asserting reasonable response times in the test (though full performance testing is out of scope for integration tests).
- For pagination tests on the by-product endpoint: verify offset/limit query parameters work correctly.

## Reuse Candidates
- `tests/api/sbom.rs` — reference for integration test structure, database setup, and assertion patterns
- `tests/api/advisory.rs` — reference for testing endpoints that query advisory/vulnerability data

## Acceptance Criteria
- [ ] Summary endpoint test verifies correct aggregation across severity x status dimensions
- [ ] By-product endpoint test verifies correct per-product counts
- [ ] Tests seed realistic test data with multiple products, severities, and statuses
- [ ] Tests verify pagination behavior for by-product endpoint
- [ ] Tests verify error handling for invalid query parameters
- [ ] All tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Integration test for `GET /api/v2/remediation/summary` with seeded data verifying count accuracy
- [ ] Integration test for `GET /api/v2/remediation/by-product` with seeded data verifying per-product counts
- [ ] Integration test for by-product pagination (offset, limit)
- [ ] Integration test for empty state (no vulnerabilities) returning zero counts

## Verification Commands
- `cargo test --test api -- remediation` — run remediation integration tests

## Dependencies
- Depends on: Task 2 — Add remediation REST endpoints
