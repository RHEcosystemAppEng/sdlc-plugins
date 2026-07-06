## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison service logic and REST endpoint that computes a structured diff between two SBOMs. The service retrieves packages, advisories, and licenses for both SBOMs from existing data and computes the diff on-the-fly (no new database tables). The endpoint is `GET /api/v2/sbom/compare?left={id1}&right={id2}` and returns an `SbomComparison` response body. Integration tests verify the endpoint behavior.

## Files to Create
- `modules/fundamental/src/sbom/service/comparison.rs` -- comparison diff logic (impl block on SbomService or standalone functions)
- `modules/fundamental/src/sbom/endpoints/compare.rs` -- GET /api/v2/sbom/compare endpoint handler
- `tests/api/sbom_compare.rs` -- integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` -- add `pub mod comparison;` to export the comparison service module
- `modules/fundamental/src/sbom/endpoints/mod.rs` -- register the `/compare` route and add `pub mod compare;`
- `tests/api/mod.rs` -- add `mod sbom_compare;` (if tests use a module index)

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- NEW: Returns `SbomComparison` JSON with six diff sections (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)

## Implementation Notes
- **Service layer** (`comparison.rs`):
  - Fetch both SBOMs by ID using the existing `SbomService::fetch` method in `modules/fundamental/src/sbom/service/sbom.rs`.
  - For each SBOM, query related packages via `PackageService` (in `modules/fundamental/src/package/service/mod.rs`) and related advisories via `AdvisoryService` (in `modules/fundamental/src/advisory/service/advisory.rs`).
  - Compute the diff by comparing package lists: packages in right but not left are "added", packages in left but not right are "removed", packages in both with different versions are "version changes".
  - Determine version change direction by comparing semver (or lexicographic fallback): if right > left, it is an "upgrade"; otherwise "downgrade".
  - For vulnerabilities: advisories linked to right SBOM but not left are "new", advisories linked to left but not right are "resolved".
  - For license changes: packages in both SBOMs with different license values.
  - Use `HashMap` for O(n) set-difference operations on package names.
  - Return `Result<SbomComparison, AppError>` following the error handling pattern.
- **Endpoint handler** (`compare.rs`):
  - Define query params struct: `#[derive(Deserialize)] struct CompareParams { left: Uuid, right: Uuid }`.
  - Handler signature: `async fn compare(Query(params): Query<CompareParams>, ...) -> Result<Json<SbomComparison>, AppError>`.
  - Validate both IDs exist; return 404 with a descriptive message if either SBOM is not found.
  - Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` and use `.context()` wrapping on all fallible operations. Applies: task creates `modules/fundamental/src/sbom/endpoints/compare.rs` matching the convention's `.rs` endpoint file scope.
  - Per CONVENTIONS.md §Endpoint Registration: register the `/compare` route in `endpoints/mod.rs` following the pattern used by `list.rs` and `get.rs`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's endpoint registration scope.
- **Route registration**: Add `.route("/compare", get(compare::compare))` in `modules/fundamental/src/sbom/endpoints/mod.rs` following the pattern of existing route registrations for `list` and `get`.
- **Performance**: The feature requires p95 < 1s for SBOMs with up to 2000 packages each. Use efficient set operations (HashMaps) and avoid N+1 queries -- batch-load packages and advisories for each SBOM in single queries.
- **Integration tests**: Follow the test pattern in `tests/api/sbom.rs` using a real PostgreSQL test database. Test cases:
  - Compare two SBOMs with known diff (added, removed, changed packages)
  - Compare identical SBOMs (expect empty diff)
  - Compare with non-existent SBOM ID (expect 404)
  - Per CONVENTIONS.md §Testing: use `assert_eq!(resp.status(), StatusCode::OK)` pattern in integration tests. Applies: task creates `tests/api/sbom_compare.rs` matching the convention's test file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- existing service with `fetch` and `list` methods for loading SBOM data
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- package query service for loading packages by SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- advisory query service for loading advisories by SBOM
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` -- error type implementing `IntoResponse`
- `modules/fundamental/src/sbom/endpoints/get.rs` -- existing endpoint handler demonstrating the handler pattern and error handling

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with a valid `SbomComparison` JSON body
- [ ] Response contains all six diff sections: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] Returns 404 when either `left` or `right` SBOM ID does not exist
- [ ] Comparison is computed on-the-fly from existing package, advisory, and license data -- no new database tables
- [ ] Integration tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences and verify each diff category contains the expected entries
- [ ] Integration test: compare two identical SBOMs and verify all diff categories are empty arrays
- [ ] Integration test: request with a non-existent SBOM ID returns 404
- [ ] Integration test: verify the JSON response field names match the API contract (`added_packages`, `removed_packages`, etc.)

## Verification Commands
- `cargo test -p trustify-tests sbom_compare` -- integration tests pass
- `cargo check -p trustify-module-fundamental` -- compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 2 -- Add SBOM comparison model types
