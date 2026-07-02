## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the REST endpoint `GET /api/v2/sbom/compare` that accepts `left` and `right` query parameters (SBOM IDs), delegates to the comparison service, and returns the structured diff as JSON. Include integration tests that exercise the endpoint against a real PostgreSQL test database.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler for the comparison endpoint; extracts query params, validates both IDs, calls SbomService::compare, returns Json<SbomComparison>

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/compare` route in the SBOM router
- `tests/api/sbom.rs` — add integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns structured diff between two SBOMs as JSON with fields: added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes

## Implementation Notes
Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs`:

```rust
pub async fn compare(
    Query(params): Query<CompareParams>,
    State(service): State<SbomService>,
    State(db): State<DbConn>,
) -> Result<Json<SbomComparison>, AppError> {
    let result = service.compare(&db, params.left, params.right).await
        .context("comparing SBOMs")?;
    Ok(Json(result))
}
```

Define `CompareParams` struct with `left: Uuid` and `right: Uuid` fields, derive `Deserialize`.

Register the route in `endpoints/mod.rs` following the existing pattern where `list.rs` and `get.rs` routes are registered:
```rust
.route("/compare", get(compare::compare))
```

Integration tests should follow the existing pattern in `tests/api/sbom.rs`:
- Set up test database with two SBOMs containing different packages and advisories
- Call `GET /api/v2/sbom/compare?left={id1}&right={id2}`
- Assert `resp.status() == StatusCode::OK`
- Deserialize response and verify diff categories

Per CONVENTIONS.md §Endpoint registration: register route in `endpoints/mod.rs`, mount in `server/main.rs`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint scope.

Per CONVENTIONS.md §Error handling: handler returns `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` using real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/sbom.rs` matching the convention's `.rs` test scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — endpoint handler pattern (query extraction, service delegation, JSON response)
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `common/src/error.rs::AppError` — error type for handler return
- `tests/api/sbom.rs` — existing integration test patterns for SBOM endpoints

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with correct JSON diff structure
- [ ] Missing `left` or `right` query param returns 400 Bad Request
- [ ] Non-existent SBOM ID returns 404 Not Found with descriptive error message
- [ ] Response time p95 < 1s for SBOMs with up to 2000 packages each
- [ ] Route is registered under `/api/v2/sbom/compare` and accessible

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences, verify all six diff categories in response
- [ ] Integration test: compare two identical SBOMs, verify empty arrays in all categories
- [ ] Integration test: request with missing query parameter returns 400
- [ ] Integration test: request with non-existent SBOM ID returns 404

## Verification Commands
- `cargo test --test api sbom_compare` — run comparison endpoint integration tests
- `curl -s "http://localhost:8080/api/v2/sbom/compare?left={id1}&right={id2}" | jq .` — verify endpoint returns structured JSON

## Dependencies
- Depends on: Task 1 — Create feature branch (create-branch bookend)
- Depends on: Task 2 — Backend comparison model and service
