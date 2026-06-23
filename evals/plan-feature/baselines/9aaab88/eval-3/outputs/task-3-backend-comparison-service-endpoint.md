## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the SBOM comparison service logic and HTTP endpoint. The service method loads both SBOMs' package and advisory data, computes the diff across all six categories, and returns an `SbomComparisonDiff`. The endpoint registers `GET /api/v2/sbom/compare?left={id1}&right={id2}` and delegates to the service.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare(left_id, right_id)` method to `SbomService`
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new comparison route
- `server/src/main.rs` — no changes needed if SBOM module routes are already mounted (verify)

## Files to Create
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler for `GET /api/v2/sbom/compare` that extracts query params, calls `SbomService::compare`, and returns JSON response
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparisonDiff` JSON with added/removed packages, version changes, new/resolved vulnerabilities, and license changes

## Implementation Notes
The `compare` service method should:
1. Load packages for both SBOMs using `PackageService` in `modules/fundamental/src/package/service/mod.rs`
2. Load advisories for both SBOMs using `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`
3. Compute set differences for packages (by name) to find added/removed
4. Compare versions for packages present in both to find version changes
5. Compute advisory differences to find new/resolved vulnerabilities
6. Compare license fields for packages present in both to find license changes

Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure — extract query params, call service, return `Result<Json<SbomComparisonDiff>, AppError>`.

The query parameter extraction should follow the pattern used in `modules/fundamental/src/sbom/endpoints/list.rs` for `Query<>` extractors.

Use `common/src/db/query.rs` helpers if filtering is needed for the package/advisory lookups.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md §Endpoint registration: each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task creates `tests/api/sbom_compare.rs` matching the convention's test file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — add comparison method here alongside existing `fetch` and `list` methods
- `modules/fundamental/src/sbom/endpoints/get.rs` — handler pattern for extracting path/query params and calling service
- `modules/fundamental/src/sbom/endpoints/list.rs` — `Query<>` extractor pattern for query parameters
- `common/src/error.rs::AppError` — error type for handler return type
- `modules/fundamental/src/package/service/mod.rs::PackageService` — fetch packages for an SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — fetch advisories for an SBOM

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with valid `SbomComparisonDiff` JSON
- [ ] Returns 404 if either SBOM ID does not exist
- [ ] Returns 400 if `left` or `right` query parameter is missing
- [ ] Response includes all six diff categories with correct data
- [ ] p95 response time < 1s for SBOMs with up to 2000 packages each (per NFR)

## Test Requirements
- [ ] Integration test: compare two SBOMs with known package differences, assert correct added/removed packages
- [ ] Integration test: compare two SBOMs with version changes, assert correct left/right versions and direction
- [ ] Integration test: compare two SBOMs with different advisory associations, assert correct new/resolved vulnerabilities
- [ ] Integration test: request with missing query parameter returns 400
- [ ] Integration test: request with non-existent SBOM ID returns 404
- [ ] Integration test: compare identical SBOMs returns empty diff arrays

## Verification Commands
- `cargo test -p tests -- sbom_compare` — integration tests pass
- `curl "http://localhost:8080/api/v2/sbom/compare?left=1&right=2"` — returns JSON diff response

## Dependencies
- Depends on: Task 1 — Create feature branch
- Depends on: Task 2 — Backend comparison models

sha256-md:f962ca5f2d89537ea2e28aa781c04d336fd441bb4131fcd2c3b3e4fd057bb81d
