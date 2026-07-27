# Task 3: Add GET /api/v2/sbom/compare endpoint with integration tests

**Summary**: Add comparison REST endpoint and integration tests

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the HTTP endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that exposes the SBOM comparison service (implemented in Task 2) via the REST API. Include integration tests that validate the endpoint's behavior against a real PostgreSQL test database.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for the comparison endpoint; extracts `left` and `right` query parameters and delegates to `SbomService::compare`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the comparison route: `GET /api/v2/sbom/compare`
- `tests/api/sbom.rs` — Add integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparisonResult` as JSON. Query parameters `left` and `right` are required SBOM IDs. Returns 400 if either parameter is missing, 404 if either SBOM does not exist.

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `list.rs` for handler structure, error handling, and response serialization.
- Register the compare route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes. Ensure the `/compare` path is registered before the `/{id}` path to avoid route conflicts (Axum matches routes in registration order).
- The handler should:
  1. Extract `left` and `right` from query parameters (use Axum's `Query` extractor with a `CompareParams` struct)
  2. Call `SbomService::compare(left, right)`
  3. Return `Json(result)` on success or `AppError` on failure
- Return HTTP 400 with a descriptive message if either `left` or `right` is missing or empty.
- Return HTTP 404 if either SBOM ID does not exist (propagated from the service layer's AppError).
- Integration tests should follow the pattern in `tests/api/sbom.rs` — use a real PostgreSQL test database, ingest two test SBOMs with known package sets, then call the comparison endpoint and assert on the response structure.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing GET endpoint handler; follow its structure for the compare handler
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `common/src/error.rs::AppError` — standard error type, already implements IntoResponse for Axum
- `tests/api/sbom.rs` — existing SBOM integration tests; follow the same test setup and assertion patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with a valid `SbomComparisonResult` JSON response
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] The endpoint response matches the contract: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] Integration tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Integration test: ingest two SBOMs with different package sets, call compare endpoint, assert response contains correct added/removed packages
- [ ] Integration test: call compare with a nonexistent SBOM ID, assert 404 response
- [ ] Integration test: call compare with missing query parameters, assert 400 response
- [ ] Integration test: ingest two identical SBOMs, call compare, assert all diff sections are empty arrays

## Verification Commands
- `cargo test --test api sbom::compare` — runs the comparison endpoint integration tests; all tests should pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model and diff service
