## Repository
trustify-backend

## Target Branch
main

## Description
Add integration tests for the remediation REST endpoints, covering the summary and by-product aggregation endpoints. Tests verify correct response structure, data accuracy, filtering behavior, and error handling against a real PostgreSQL test database.

## Files to Create
- `tests/api/remediation.rs` — integration tests for GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product

## Files to Modify
- `tests/Cargo.toml` — add remediation test module if separate test binary configuration is needed

## Implementation Notes
- Follow the integration test pattern established in `tests/api/sbom.rs` — tests hit a real PostgreSQL test database and assert on response status codes and JSON structure.
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions, consistent with existing tests.
- Set up test data by ingesting test SBOMs and advisories to create the vulnerability relationships needed for remediation aggregation.
- Test scenarios should cover: empty database (no vulnerabilities), single product with mixed severities, multiple products, and large dataset performance (verify p95 < 500ms requirement).
- Per CONVENTIONS.md §Testing: use the established integration test pattern with real PostgreSQL test database. Applies: task creates `tests/api/remediation.rs` matching the convention's test file scope.

## Reuse Candidates
- `tests/api/sbom.rs` — integration test pattern for SBOM endpoints; follow the same setup, request, and assert structure
- `tests/api/advisory.rs` — integration test pattern for advisory endpoints; reference for test data setup with advisories

## Acceptance Criteria
- [ ] Integration tests verify GET /api/v2/remediation/summary returns correct severity and status breakdowns
- [ ] Integration tests verify GET /api/v2/remediation/by-product returns correct per-product counts
- [ ] Tests verify pagination for the by-product endpoint
- [ ] Tests verify correct behavior with an empty data set (no vulnerabilities)
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Test summary endpoint with known vulnerability data and verify aggregation accuracy
- [ ] Test by-product endpoint with multiple products and verify per-product counts
- [ ] Test response format matches the expected JSON structure
- [ ] Test error scenarios (invalid parameters, database unavailability)

## Verification Commands
- `cargo test -p trustify-tests -- remediation` — all remediation integration tests pass

## Dependencies
- Depends on: Task 2 — Add remediation REST endpoints
