## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add integration tests for the remediation REST endpoints. Tests should hit the actual endpoints against a real PostgreSQL test database, following the existing integration test patterns in the project. Cover both the summary and by-product endpoints with various data scenarios.

## Files to Create
- `tests/api/remediation.rs` -- integration tests for remediation endpoints

## Files to Modify
- `tests/Cargo.toml` -- add remediation test module if needed

## Implementation Notes
- Follow the integration test pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs`: tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
- Set up test data by ingesting sample SBOMs and advisories with known severity levels and remediation statuses through the existing ingestion service.
- Test scenarios should cover: empty database (zero counts), single product with mixed severities, multiple products with varying remediation progress.
- Verify response JSON shapes match the model structs (RemediationSummary, ProductRemediation) defined in Task 1.
- Test pagination on the by-product endpoint for portfolios exceeding the default page size.

## Reuse Candidates
- `tests/api/sbom.rs` -- reference pattern for endpoint integration tests with test database setup
- `tests/api/advisory.rs` -- reference pattern for advisory-related test data setup
- `modules/ingestor/src/service/mod.rs::IngestorService` -- use for setting up test data (ingest sample SBOMs and advisories)

## Acceptance Criteria
- [ ] Integration tests pass against a real PostgreSQL test database
- [ ] Tests cover GET /api/v2/remediation/summary with various data scenarios
- [ ] Tests cover GET /api/v2/remediation/by-product with pagination
- [ ] Tests verify correct aggregation counts match ingested test data
- [ ] Tests verify response JSON structure matches model definitions

## Test Requirements
- [ ] Test summary endpoint with empty database returns zero counts
- [ ] Test summary endpoint with known dataset returns expected severity/status counts
- [ ] Test by-product endpoint returns correct per-product breakdown
- [ ] Test by-product endpoint pagination with >50 products
- [ ] Test both endpoints return proper error responses for invalid requests

## Verification Commands
- `cargo test --test api -- remediation` -- run remediation integration tests

## Dependencies
- Depends on: Task 2 -- Add remediation REST endpoints
