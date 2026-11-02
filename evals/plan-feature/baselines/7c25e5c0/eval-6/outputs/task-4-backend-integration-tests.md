## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add integration tests for the remediation endpoints. Tests should exercise both `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` against a real PostgreSQL test database with seeded vulnerability and SBOM data. Tests verify correct aggregation logic, empty dataset handling, and response structure.

## Files to Create
- `tests/api/remediation.rs` — integration tests for remediation endpoints

## Files to Modify
- `tests/api/mod.rs` — add `mod remediation;` declaration (if mod.rs pattern is used for test organization)

## Implementation Notes
Follow the integration test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`:

- Tests hit a real PostgreSQL test database — no mocking
- Use the `assert_eq!(resp.status(), StatusCode::OK)` pattern established in existing tests
- Seed test data by ingesting sample SBOMs and advisories through the existing ingestor service (see `tests/api/advisory.rs` for the advisory ingestion test setup pattern)
- Test the full request-response cycle through the Axum server
- Verify JSON response shapes match the model structs from Task 1

Test scenarios:
1. Summary endpoint with multiple severities and statuses — verify correct grouping
2. By-product endpoint with multiple products — verify correct per-product counts
3. Empty database — verify zero counts returned (not error)
4. Single SBOM with multiple advisories — verify no double-counting
5. Advisory correlated with multiple SBOMs — verify correct aggregation

## Acceptance Criteria
- [ ] Integration tests pass against real PostgreSQL test database
- [ ] Summary endpoint test verifies correct severity × status grouping
- [ ] By-product endpoint test verifies correct per-product aggregation
- [ ] Empty dataset test returns zero counts without errors
- [ ] Tests use existing test infrastructure patterns (no new test utilities)

## Test Requirements
- [ ] At least 5 test cases covering: multi-severity summary, multi-product breakdown, empty dataset, deduplication, multi-SBOM advisory aggregation
- [ ] Tests follow the StatusCode assertion pattern from existing tests
- [ ] Test data setup uses existing ingestor service for realistic data

## Dependencies
- Depends on: Task 3 — Remediation endpoints
