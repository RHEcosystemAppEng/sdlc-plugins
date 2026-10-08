## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the REST endpoint `GET /api/v2/sbom/compare` that accepts `left` and `right` SBOM ID query parameters and returns the structured diff computed by the comparison service. This task wires the comparison service to an Axum handler, registers the route, and adds integration tests against a real PostgreSQL test database.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the new `/compare` route alongside existing SBOM routes

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` -- Axum handler for `GET /api/v2/sbom/compare?left={id1}&right={id2}`, calls SbomCompareService and returns JSON response
- `tests/api/sbom_compare.rs` -- integration tests for the comparison endpoint covering success, missing params, invalid IDs, and large SBOM comparisons

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- NEW: returns `SbomComparison` JSON with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure: extract query params, call service, map errors to AppError, return JSON.
- Register the `/compare` route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes (`list.rs`, `get.rs`). The route must be registered before the `/{id}` route to avoid path conflicts.
- Use `axum::extract::Query<CompareParams>` for the `left` and `right` query parameters. Define `CompareParams` with `left: String` and `right: String` fields.
- Return 400 Bad Request if either `left` or `right` parameter is missing. Return 404 Not Found if either SBOM ID does not exist.
- The handler should call `SbomCompareService::compare(left_id, right_id)` and return the result as JSON with `StatusCode::OK`.
- Integration tests should follow the pattern in `tests/api/sbom.rs`: use the test database setup, ingest test SBOMs, then call the endpoint and assert the response.
- Consider adding cache headers via `tower-http` caching middleware for comparison results, since the same pair of SBOMs will always produce the same diff.
- Per CONVENTIONS.md §Endpoint registration: register routes in endpoints/mod.rs and mount in server/main.rs.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint registration file scope.
- Per CONVENTIONS.md §Testing: follow integration test patterns in tests/api/ using real PostgreSQL test database.
  Applies: task creates `tests/api/sbom_compare.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- existing SBOM GET handler; follow the same pattern for extracting parameters, calling service, and returning JSON
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- route registration example; add the compare route here
- `common/src/error.rs::AppError` -- error type for handler responses; use for 400/404 error cases
- `tests/api/sbom.rs` -- existing SBOM integration tests; follow the same test database setup and assertion patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with correct SbomComparison JSON
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Response shape matches the API contract with all six diff categories
- [ ] Route is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`
- [ ] Integration tests pass against the PostgreSQL test database

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences, verify response contains correct added/removed packages
- [ ] Integration test: compare two SBOMs with version changes, verify upgrade/downgrade direction
- [ ] Integration test: request with missing `left` parameter returns 400
- [ ] Integration test: request with missing `right` parameter returns 400
- [ ] Integration test: request with non-existent SBOM ID returns 404
- [ ] Integration test: response Content-Type is application/json
- [ ] Integration test: comparing identical SBOMs returns empty diff categories

## Verification Commands
- `cargo test --test sbom_compare` -- run comparison endpoint integration tests
- `curl -s "http://localhost:8080/api/v2/sbom/compare?left=<id1>&right=<id2>" | jq .` -- verify endpoint returns structured diff JSON

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 2 -- Add SBOM comparison model types and diff service
