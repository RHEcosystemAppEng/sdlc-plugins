## Repository
trustify-backend

## Target Branch
main

## Description
Wire up the `GET /api/v2/sbom/compare?left={id1}&right={id2}` REST endpoint that exposes the SBOM comparison service created in Task 1. The endpoint accepts two SBOM IDs as query parameters, invokes the comparison service, and returns the structured diff as JSON. This task also adds integration tests that verify the endpoint through the full HTTP stack against a PostgreSQL test database.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Endpoint handler: parse `left` and `right` query parameters, validate as UUIDs, call SbomService::compare(), return JSON response. Return 400 for missing/invalid parameters, 404 for non-existent SBOMs.
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint covering success, error, and edge cases

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the comparison route at `/api/v2/sbom/compare` alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns SbomComparisonResult JSON with six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes). Returns 400 for missing/invalid parameters, 404 for non-existent SBOM IDs.

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` for handler structure, Axum extractor usage, and error response patterns.
- Register the comparison route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing SBOM routes. The compare route must be registered BEFORE the `/{id}` wildcard route to avoid path conflicts (Axum matches routes in registration order).
- Use Axum's `Query` extractor to parse `left` and `right` parameters. Define a `CompareParams` struct with `left: Uuid` and `right: Uuid` fields.
- Return `Result<Json<SbomComparisonResult>, AppError>` from the handler, consistent with other endpoint response patterns.
- Return 400 Bad Request when `left` or `right` query parameters are missing or not valid UUIDs, using the AppError pattern from `common/src/error.rs`.
- Return 404 Not Found when either SBOM ID does not exist.
- Follow the integration test pattern in `tests/api/sbom.rs`: test against a real PostgreSQL test database, use `assert_eq!(resp.status(), StatusCode::OK)` assertion pattern.
- Per CONVENTIONS.md §Endpoint Registration: register the route in the module's `endpoints/mod.rs`; `server/main.rs` mounts all modules.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database with `StatusCode` assertions.
  Applies: task creates `tests/api/sbom_compare.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — existing SBOM get handler showing Axum extractor pattern, error handling, and JSON response structure
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing SBOM list handler showing query parameter extraction pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration showing how to add new routes to the SBOM module
- `tests/api/sbom.rs` — existing SBOM integration tests showing test setup, fixture insertion, and assertion patterns
- `common/src/error.rs::AppError` — error handling for 400/404 responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with SbomComparisonResult JSON
- [ ] Returns 400 when `left` query parameter is missing
- [ ] Returns 400 when `right` query parameter is missing
- [ ] Returns 400 when either parameter is not a valid UUID
- [ ] Returns 404 when either SBOM ID does not exist in the database
- [ ] Response JSON structure includes all six diff category arrays
- [ ] Integration tests pass against PostgreSQL test database

## Test Requirements
- [ ] Integration test: compare two existing SBOMs with known package/advisory differences — verify response contains correct diff items in each category
- [ ] Integration test: request with missing `left` parameter — verify 400 response
- [ ] Integration test: request with missing `right` parameter — verify 400 response
- [ ] Integration test: request with non-existent SBOM ID — verify 404 response
- [ ] Integration test: request with invalid UUID format — verify 400 response
- [ ] Integration test: compare two identical SBOMs — verify all diff arrays are empty

## Verification Commands
- `cargo test --test sbom_compare` — all integration tests pass
- `cargo run` then `curl 'http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=<id2>'` — endpoint returns valid JSON

## Dependencies
- Depends on: Task 1 — Implement SBOM comparison diff service and model types
