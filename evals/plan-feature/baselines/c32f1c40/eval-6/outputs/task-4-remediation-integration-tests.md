## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Add integration tests for both remediation REST endpoints (`GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`). These tests verify the full request-response cycle against a real PostgreSQL test database, following the established integration test pattern in the trustify-backend repository.

## Files to Create
- `tests/api/remediation.rs` -- integration tests for both remediation endpoints

## Files to Modify
- `tests/Cargo.toml` -- add remediation test module if test modules are declared explicitly

## Implementation Notes
- Per backend conventions: integration tests in `tests/api/` hit a real PostgreSQL test database. Follow the existing test patterns in `tests/api/sbom.rs` and `tests/api/advisory.rs`.
- Per backend conventions: use `assert_eq!(resp.status(), StatusCode::OK)` pattern for status code assertions.
- Test both endpoints with: (a) empty database -- verify empty results without errors, (b) seeded test data -- verify correct aggregation counts, (c) pagination for by-product endpoint.
- Seed test data by creating advisory entities with different severities and statuses, linked to SBOMs via the sbom_advisory join table. Use the existing test helpers from the advisory and SBOM integration tests.
- Verify the response JSON structure matches the API contract: summary returns entries grouped by severity/status, by-product returns PaginatedResults<ProductRemediation>.
- Constraints: per docs/constraints.md section 2, commit messages must follow Conventional Commits format and reference TC-9006. Per section 5, changes must be scoped to the files listed.

## Reuse Candidates
- `tests/api/sbom.rs` -- SBOM endpoint integration tests. Follow the same test setup and assertion patterns.
- `tests/api/advisory.rs` -- advisory endpoint integration tests. Reference for test data seeding with severity fields.

## Acceptance Criteria
- [ ] Integration tests exist for GET /api/v2/remediation/summary
- [ ] Integration tests exist for GET /api/v2/remediation/by-product
- [ ] Tests verify correct aggregation with seeded vulnerability data across multiple severities and statuses
- [ ] Tests verify empty results when no data exists
- [ ] Tests verify by-product pagination
- [ ] All tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Test summary endpoint returns correct severity x status breakdown for seeded data
- [ ] Test by-product endpoint returns correct per-product counts for seeded data
- [ ] Test by-product endpoint pagination returns correct page sizes and totals
- [ ] Test both endpoints handle empty data gracefully (200 with empty results)
- [ ] Test by-product sorting by product name and by vulnerability count

## Verification Commands
- `cargo test -p trustify-tests -- api::remediation` -- all integration tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 3 -- Add remediation summary and by-product REST endpoints
