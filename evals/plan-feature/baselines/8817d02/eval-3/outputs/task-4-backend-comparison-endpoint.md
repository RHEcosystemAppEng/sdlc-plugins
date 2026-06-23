# Task 4 — Add GET /api/v2/sbom/compare endpoint

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the REST endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}` that accepts two SBOM IDs as query parameters and returns a structured JSON diff using the comparison service. The endpoint validates both IDs, invokes the comparison service, and returns the SbomComparisonResult as the response body. This is the primary backend API consumed by the frontend comparison view.

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — Handler function for GET /api/v2/sbom/compare, query parameter extraction, validation, and response serialization

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the compare route alongside existing SBOM routes (/api/v2/sbom)
- `server/src/main.rs` — No changes expected if routes are auto-mounted via module registration, but verify

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns SbomComparisonResult JSON with six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Implementation Notes
- Follow the existing endpoint pattern from `modules/fundamental/src/sbom/endpoints/get.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`:
  - Handler function signature returns `Result<Json<SbomComparisonResult>, AppError>`
  - Use Axum query parameter extraction for `left` and `right` SBOM IDs
  - Register routes in `endpoints/mod.rs` following the same pattern as existing GET routes
- Validate both query parameters are present — return 400 Bad Request with descriptive error if either is missing.
- Validate both SBOM IDs exist — return 404 Not Found if either SBOM does not exist.
- Validate both SBOMs are from the same product/project for meaningful comparison — return 400 if they differ (per Customer Considerations).
- Call the comparison service from Task 3 to compute the diff.
- Per docs/constraints.md §3.3: `gh pr create` must specify `--base <target-branch>` matching Target Branch value.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/get.rs` — Follow the same handler pattern for SBOM ID extraction and error responses
- `modules/fundamental/src/sbom/endpoints/list.rs` — Follow the same route registration pattern
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Extend existing route registration
- `common/src/error.rs::AppError` — Use for consistent error responses (400, 404)

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with valid SbomComparisonResult JSON
- [ ] Returns 400 when left or right query parameter is missing
- [ ] Returns 404 when either SBOM ID does not exist
- [ ] Response JSON shape matches the structure defined in the feature specification
- [ ] Endpoint is registered and accessible via the existing route mounting in server/main.rs

## Test Requirements
- [ ] Integration test: valid comparison request returns 200 with correct diff structure
- [ ] Integration test: missing query parameter returns 400
- [ ] Integration test: non-existent SBOM ID returns 404
- [ ] Integration test: response JSON contains all six diff category fields

## Verification Commands
- `cargo test --test api` — Run integration tests against test database

## Documentation Updates
- `README.md` — Add comparison endpoint to API reference if API documentation exists in the backend repo

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison diff model types
- Depends on: Task 3 — Implement SBOM comparison service logic

sha256-md:5b3b4af63d6a745c53d8db7706686c6ddf7bf227908f983ffd482ba7dd5b0992
