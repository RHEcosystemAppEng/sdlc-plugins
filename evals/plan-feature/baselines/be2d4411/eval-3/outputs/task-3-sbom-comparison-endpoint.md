## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` REST endpoint that accepts `left` and `right` query parameters (SBOM IDs), invokes the comparison service from Task 2, and returns the structured diff as JSON. Add integration tests covering all diff categories, error responses, and edge cases.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the comparison route in the SBOM endpoint router
- `server/src/main.rs` — Verify SBOM module routes are mounted (likely no change needed, but confirm)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler for GET /api/v2/sbom/compare with query parameter parsing
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns structured diff of two SBOMs as SbomComparisonResult JSON

## Implementation Notes
- Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern used for `list.rs` and `get.rs` route registration. See existing `.route("/api/v2/sbom", get(list))` pattern.
- Handler function signature: `async fn compare(Query(params): Query<CompareParams>, ...) -> Result<Json<SbomComparisonResult>, AppError>` where `CompareParams` has `left: String` and `right: String` fields.
- Return HTTP 400 if either `left` or `right` query parameter is missing.
- Return HTTP 404 if either SBOM ID does not exist (propagated from service layer AppError::NotFound).
- Integration tests should follow the pattern in `tests/api/sbom.rs` — set up test data in a real PostgreSQL test database, call the endpoint, assert on response status and body.
- Test cases: successful comparison with all diff categories populated, missing left parameter (400), missing right parameter (400), non-existent SBOM ID (404), comparison of identical SBOMs (200 with empty diff arrays).

**Convention references:**
- Per CONVENTIONS.md §Endpoint registration: register route in `endpoints/mod.rs`; mount in `server/main.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` — note that the comparison endpoint returns a single `SbomComparisonResult`, not paginated, which is appropriate since it computes a single diff result.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust endpoint scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/sbom_compare.rs` matching the convention's test file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/mod.rs` — existing route registration pattern to follow
- `modules/fundamental/src/sbom/endpoints/get.rs` — handler function signature and error handling pattern for SBOM-by-ID lookups
- `modules/fundamental/src/sbom/endpoints/list.rs` — query parameter parsing pattern
- `common/src/error.rs::AppError` — error type with IntoResponse implementation
- `tests/api/sbom.rs` — integration test setup and assertion patterns

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with SbomComparisonResult JSON
- [ ] Missing `left` or `right` query parameter returns 400 Bad Request
- [ ] Non-existent SBOM ID returns 404 Not Found
- [ ] Response JSON shape matches the contract: added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes arrays
- [ ] Route is registered and reachable via the SBOM endpoint router

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences, verify 200 response and all six diff arrays contain expected entries
- [ ] Integration test: missing left query parameter returns 400
- [ ] Integration test: missing right query parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: comparison of identical SBOMs returns 200 with all empty arrays

## Verification Commands
- `cargo test --test api sbom_compare` — all comparison endpoint tests pass
- `cargo build` — project compiles without errors

## Documentation Updates
- `README.md` — Add the comparison endpoint to the API reference section if one exists

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model types and diff service

[sdlc-workflow] Description digest: sha256-md:b3ab8d5ee4bc9792cd2966e09b28e1e921db18bcfdf5c45b68d72bc44d8245d8
