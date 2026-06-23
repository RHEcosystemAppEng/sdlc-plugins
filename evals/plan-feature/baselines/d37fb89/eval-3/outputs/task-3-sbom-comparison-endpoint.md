## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the REST endpoint `GET /api/v2/sbom/compare?left={id}&right={id}` that exposes the SBOM comparison service to API consumers. The endpoint validates query parameters, delegates to `SbomCompareService`, and returns the structured diff as JSON. The response must meet the p95 < 1s latency requirement for SBOMs with up to 2000 packages each.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` -- Handler function for `GET /api/v2/sbom/compare` with `left` and `right` query parameters

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Register the comparison route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/compare?left={id}&right={id}` -- NEW: Returns `SbomComparison` JSON with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/` (see `get.rs` and `list.rs` for reference).
- Extract `left` and `right` query parameters using Axum's `Query` extractor. Return `AppError::BadRequest` if either parameter is missing.
- Delegate to `SbomCompareService::compare()` from Task 2.
- Return `Json(comparison)` on success.
- Register the route in `endpoints/mod.rs` using the same pattern as existing routes (e.g., `.route("/api/v2/sbom/compare", get(compare_sboms))`).
- The route must be registered before the `GET /api/v2/sbom/{id}` route to avoid path conflicts (Axum matches routes in registration order, and `{id}` would capture "compare" as an ID).

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` -- Pattern for single-resource GET handler with path/query extraction
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Route registration pattern
- `common/src/error.rs::AppError` -- Error response handling

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with `SbomComparison` JSON
- [ ] Returns 400 when `left` or `right` query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Route is registered and accessible via the server

## Test Requirements
- [ ] Integration test: valid comparison request returns 200 with expected diff structure
- [ ] Integration test: missing query parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 2 -- SBOM comparison model and diff service

[sdlc-workflow] Description digest: sha256-md:47f88d6e6cccc82efd641a0fdd0f5037121d0cf842e2bec23f8b480266aa7092
