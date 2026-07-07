# Task 3 -- SBOM comparison endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add the GET /api/v2/sbom/compare endpoint that accepts left and right query parameters (SBOM IDs) and returns the structured diff computed by SbomService::compare(). The endpoint handles parameter validation and error cases, returning appropriate HTTP status codes.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` -- Handler function `compare_sboms(Query<CompareParams>, State<AppState>) -> Result<Json<SbomComparisonResult>, AppError>` with `CompareParams { left: String, right: String }`

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- Register the new `/compare` route alongside existing SBOM routes

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- NEW: returns SbomComparisonResult JSON with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` for route registration and handler structure.
- Extract left and right SBOM IDs from query parameters. Return AppError::BadRequest if either parameter is missing.
- Return AppError::NotFound if either SBOM ID does not exist, following the existing error pattern in the SBOM endpoints.
- Call SbomService::compare(left_id, right_id, &db) from Task 2 to compute the diff.
- Register the route in endpoints/mod.rs using the same Router builder pattern as the existing list and get endpoints.
- Per CONVENTIONS.md Error Handling: wrap all fallible operations with `.context()` and return `Result<T, AppError>`. Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` scope.

## Acceptance Criteria
- [ ] GET /api/v2/sbom/compare?left={id1}&right={id2} returns 200 with SbomComparisonResult JSON
- [ ] Returns 400 when left or right query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Response p95 latency < 1s for SBOMs with up to 2000 packages each
- [ ] Route is registered under the existing /api/v2/sbom prefix

## Test Requirements
- [ ] Handler returns correct JSON structure for valid SBOM ID pairs
- [ ] Handler returns 400 for missing query parameters

## Dependencies
- Depends on: Task 1 -- SBOM comparison data model
- Depends on: Task 2 -- SBOM comparison service
