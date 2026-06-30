## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the `GET /api/v2/sbom/compare` endpoint that accepts `left` and `right` query parameters (SBOM IDs) and returns the structured comparison result. The endpoint delegates to `SbomComparisonService` and returns the `SbomComparison` model as JSON. This completes the backend API surface for the SBOM comparison feature.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for `GET /api/v2/sbom/compare` with query parameters `left` and `right`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route and add `pub mod compare;`

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparison` JSON with added/removed packages, version changes, new/resolved vulnerabilities, and license changes

## Implementation Notes
Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `list.rs`. The handler should:

1. Define a `CompareQuery` struct with `left: String` and `right: String` fields, deriving `Deserialize` for Axum query extraction
2. Extract query parameters using Axum's `Query<CompareQuery>` extractor
3. Validate both parameters are present and non-empty; return 400 Bad Request if missing
4. Call `SbomComparisonService::compare(left, right, &db)` from Task 3
5. Return `Json(comparison)` with status 200 on success
6. Let `AppError` handle error responses (404 for missing SBOMs, 500 for internal errors)

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` following the existing pattern where `list.rs` and `get.rs` are registered. The compare endpoint should be mounted at `.route("/compare", get(compare::handler))` before the `/{id}` route to avoid path conflicts.

Per CONVENTIONS.md §Endpoint registration: register routes in `endpoints/mod.rs`; `server/main.rs` mounts all modules.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `endpoints/mod.rs` scope.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference for single-resource handler pattern with path extraction
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for query parameter extraction pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `common/src/error.rs::AppError` — error response handling

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparison` JSON
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Response JSON shape matches the contract defined in figma-context.md
- [ ] Route is registered in `endpoints/mod.rs` and accessible via the server

## Test Requirements
- [ ] Verify 200 response with valid SBOM IDs returns correctly shaped comparison JSON
- [ ] Verify 400 response when query parameters are missing
- [ ] Verify 404 response when a non-existent SBOM ID is provided

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental -- compare` — endpoint unit tests pass

## Dependencies
- Depends on: Task 1 — create-branch
- Depends on: Task 3 — backend-comparison-service

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

[sdlc-workflow] Description digest: sha256-md:84e2d0d81153f77d93da815acfa2211e084882bc68f932b5e52810573f5ea823
