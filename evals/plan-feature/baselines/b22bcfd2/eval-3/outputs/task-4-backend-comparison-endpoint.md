## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the REST endpoint GET /api/v2/sbom/compare that accepts left and right SBOM IDs as query parameters and returns the structured comparison result. This endpoint delegates to SbomService::compare and follows the existing endpoint patterns.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new comparison route
- `server/src/main.rs` — no changes needed if sbom module routes are already mounted (verify)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler for GET /api/v2/sbom/compare

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns SbomComparisonResult JSON with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes

## Implementation Notes
Create `modules/fundamental/src/sbom/endpoints/compare.rs` following the pattern in `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`.

The handler function signature should follow the Axum pattern:
```rust
pub async fn compare(
    Query(params): Query<CompareParams>,
    State(service): State<SbomService>,
    // ... database connection
) -> Result<Json<SbomComparisonResult>, AppError>
```

Define `CompareParams` struct with `left: Uuid` and `right: Uuid` fields, deriving `Deserialize`.

Register the route in `modules/fundamental/src/sbom/endpoints/mod.rs` alongside existing routes like list and get. The route registration follows the pattern: `.route("/compare", get(compare::compare))`.

Validate that both left and right params are provided and are valid UUIDs (Axum's Query extractor handles this automatically with proper error messages).

Return appropriate HTTP status codes:
- 200 with SbomComparisonResult on success
- 404 if either SBOM ID doesn't exist
- 400 if query params are missing or malformed

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — pattern for single-SBOM endpoint handler
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern
- `common/src/error.rs::AppError` — error response handling

## Acceptance Criteria
- [ ] GET /api/v2/sbom/compare?left={id1}&right={id2} returns 200 with comparison JSON
- [ ] Missing or malformed query params return 400
- [ ] Non-existent SBOM IDs return 404
- [ ] Route is registered in the sbom endpoints module
- [ ] Response shape matches the expected JSON structure from figma-context.md

## Test Requirements
- [ ] Integration test: valid comparison returns 200 with correct diff structure
- [ ] Integration test: missing left param returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: both params missing returns 400

## Verification Commands
- `cargo test --test api sbom::compare` — expected: all comparison endpoint tests pass

## Dependencies
- Depends on: Task 3 — Backend comparison service
