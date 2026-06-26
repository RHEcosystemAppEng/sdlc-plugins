## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Wire the SBOM comparison service into an Axum HTTP endpoint at `GET /api/v2/sbom/compare?left={id1}&right={id2}`. This endpoint accepts two SBOM IDs as query parameters, invokes the comparison service, and returns the structured diff as JSON.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Axum handler for `GET /api/v2/sbom/compare` with query parameter extraction

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the comparison route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparison` JSON response. Both `left` and `right` are required query parameters (UUIDs). Returns 400 if either parameter is missing, 404 if either SBOM is not found.

## Implementation Notes
Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` for handler structure and error handling.

Define a query parameter struct:
```
#[derive(Deserialize)]
pub struct CompareQuery {
    left: Uuid,
    right: Uuid,
}
```

The handler should:
1. Extract `CompareQuery` from the request query string using Axum's `Query` extractor
2. Call `SbomCompareService::compare(query.left, query.right, &db)` from `modules/fundamental/src/sbom/service/compare.rs`
3. Return `Ok(Json(result))` on success
4. Let `AppError` propagate for error cases (404, 500)

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside the existing `/api/v2/sbom` and `/api/v2/sbom/{id}` routes. Use `.route("/api/v2/sbom/compare", get(compare::handler))` — register it before the `/{id}` route to avoid path conflicts.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — handler pattern with Axum extractors and error propagation
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `common/src/error.rs::AppError` — error type implementing `IntoResponse`

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparison` JSON
- [ ] Missing `left` or `right` query parameter returns 400
- [ ] Non-existent SBOM ID returns 404
- [ ] Route is registered in the SBOM endpoints module
- [ ] Route does not conflict with existing `/api/v2/sbom/{id}` route

## Test Requirements
- [ ] Integration test: valid comparison returns 200 with expected JSON structure
- [ ] Integration test: missing query parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404

## Verification Commands
- `cargo build -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental compare` — endpoint tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch
- Depends on: Task 3 — Backend comparison service

[sdlc-workflow] Description digest: sha256-md:680fc537b7ec3af4b2146dee132446a1146085a6abd0bf3f6d9c085228df3ac2
