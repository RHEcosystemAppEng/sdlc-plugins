## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM IDs), invokes the comparison service, and returns the structured diff as JSON. Also add integration tests for the endpoint covering success, error, and edge cases.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for `GET /api/v2/sbom/compare` with query parameter extraction and response serialization
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route in the SBOM endpoint router

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparisonResult` as JSON with 200 OK on success, 404 if either SBOM not found, 400 if missing query params

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure: extract query parameters, call service method, return JSON response.
- Define a `CompareQuery` struct with `left: String` and `right: String` fields, deriving `Deserialize` for Axum query parameter extraction (use `axum::extract::Query<CompareQuery>`).
- Return 400 Bad Request if either `left` or `right` query parameter is missing — Axum handles this automatically when using `Query<CompareQuery>` with non-optional fields.
- Return 404 Not Found when `SbomService::compare` returns `AppError::NotFound`.
- Route registration: add `.route("/compare", get(compare))` in the SBOM endpoint router in `modules/fundamental/src/sbom/endpoints/mod.rs`, following the pattern used for `/list` and `/{id}`.
- Integration tests should follow the pattern in `tests/api/sbom.rs`: use a real PostgreSQL test database, create test SBOMs with known differences, call the endpoint, and assert response status and body.
- Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes; follow existing pattern for route ordering.
  Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md §Response types: use the standard response pattern with `Result<Json<T>, AppError>`.
  Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task creates `tests/api/sbom_compare.rs` matching the convention's Rust test file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — demonstrates the handler pattern: query extraction, service call, JSON response
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates route registration and list endpoint pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — shows how routes are registered in the SBOM module
- `tests/api/sbom.rs` — integration test patterns for SBOM endpoints (test setup, assertion style)
- `common/src/error.rs::AppError` — error-to-response conversion (IntoResponse implementation)

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparisonResult` JSON body
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Response JSON field names match the specified shape (snake_case: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`)
- [ ] URL is shareable — the same `left` and `right` parameters produce the same comparison result

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences — verify 200 response with correct diff counts
- [ ] Integration test: compare with non-existent SBOM ID — verify 404 response
- [ ] Integration test: compare without query parameters — verify 400 response
- [ ] Integration test: compare two identical SBOMs — verify 200 response with empty diff sections
- [ ] Integration test: verify response body JSON structure matches `SbomComparisonResult` schema

## Verification Commands
- `cargo test --test sbom_compare` — all comparison endpoint integration tests pass
- `cargo clippy -- -D warnings` — no new warnings introduced

## Documentation Updates
- `README.md` — add the comparison endpoint to the API endpoint listing if one exists

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add comparison service logic

<!-- [sdlc-workflow] Description digest: sha256-md:218eb06f25ffc78d7b767d10dfd6ac4f7d281c35172f172ce16977093feccb0b -->
