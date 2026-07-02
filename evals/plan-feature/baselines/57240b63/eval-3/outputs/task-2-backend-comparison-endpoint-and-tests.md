## Repository
trustify-backend

## Target Branch
main

## Description
Add the HTTP endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that invokes the comparison service and returns the structured diff as JSON. Register the route in the SBOM endpoint module and add integration tests covering success, error, and edge cases.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` -- Handler for `GET /api/v2/sbom/compare` with query parameter extraction and JSON response
- `tests/api/sbom_compare.rs` -- Integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Register the `/compare` route in the SBOM router

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- NEW: Accepts two SBOM IDs as query parameters, returns `SbomComparisonResult` JSON with six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Implementation Notes
- Follow the existing endpoint handler pattern in `modules/fundamental/src/sbom/endpoints/get.rs` (single resource GET) and `modules/fundamental/src/sbom/endpoints/list.rs` (query parameter extraction) for handler structure.
- Define a query parameter struct for Axum's `Query` extractor:
  ```rust
  #[derive(Deserialize)]
  pub struct CompareParams {
      pub left: Uuid,  // or the ID type used in sbom.rs entity
      pub right: Uuid,
  }
  ```
- The handler function signature should follow the existing pattern:
  ```rust
  pub async fn compare(
      Query(params): Query<CompareParams>,
      service: Extension<SbomService>,  // or however DI is done in the codebase
  ) -> Result<Json<SbomComparisonResult>, AppError> {
      let result = service.compare(params.left, params.right).await.context("comparing SBOMs")?;
      Ok(Json(result))
  }
  ```
- Return `400 Bad Request` if either `left` or `right` is missing or not a valid ID (Axum's `Query` extractor handles this automatically with a deserialization error mapped to 400).
- Return `404 Not Found` if either SBOM ID does not exist (propagated from the service layer via `AppError`).
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing route registration pattern. Add `.route("/compare", get(compare))` to the SBOM router, alongside the existing `/` (list) and `/{id}` (get) routes.
- Integration tests should follow the pattern in `tests/api/sbom.rs`: set up test SBOMs with known packages and advisories in the test database, call the endpoint via HTTP, and assert the response status code and JSON body.
- Per CONVENTIONS.md section Endpoint registration: register routes in endpoints/mod.rs; server/main.rs mounts all modules.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint registration scope.
- Per CONVENTIONS.md section Testing: integration tests in tests/api/ hit a real PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/sbom_compare.rs` matching the convention's `.rs` test scope.
- p95 response time target is < 1s for SBOMs with up to 2000 packages each (per NFR). If initial implementation exceeds this, consider batching database queries or adding indexes on the `sbom_package` and `sbom_advisory` join tables.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- Reference for single-SBOM GET handler pattern (parameter extraction, error handling, JSON response)
- `modules/fundamental/src/sbom/endpoints/list.rs` -- Reference for query parameter extraction with Axum `Query` extractor
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Existing route registration; follow the same `.route()` pattern for the compare endpoint
- `common/src/db/query.rs` -- Shared query builder helpers for filtering and sorting; may be useful if comparison results need optional filtering
- `common/src/error.rs::AppError` -- Error type with `IntoResponse` implementation; use for all error responses
- `tests/api/sbom.rs` -- Existing SBOM integration tests; follow setup, request, and assertion patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON body
- [ ] Response includes all six diff categories: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] Returns 400 when `left` or `right` query parameter is missing or malformed
- [ ] Returns 404 when either SBOM ID does not exist in the database
- [ ] Route is registered in the SBOM endpoint module at path `/compare`
- [ ] URL is shareable -- calling the endpoint with the same query params produces the same result (stateless)

## Test Requirements
- [ ] Integration test: compare two SBOMs with known package/advisory differences, verify all six diff categories contain expected items
- [ ] Integration test: compare two identical SBOMs, verify all diff arrays are empty
- [ ] Integration test: request with missing `left` parameter returns 400 status
- [ ] Integration test: request with missing `right` parameter returns 400 status
- [ ] Integration test: request with non-existent SBOM ID returns 404 status
- [ ] Integration test: response content-type is `application/json`

## Verification Commands
- `cargo test --test sbom_compare` -- run comparison endpoint integration tests
- `cargo clippy -- -D warnings` -- verify no Rust lint warnings in new code

## Dependencies
- Depends on: Task 1 -- Add SBOM comparison model and service

---
sha256-md:3af9fa953603f20eff4b41ea6924cfe54298fc644953ad577044471ac644e6d2
