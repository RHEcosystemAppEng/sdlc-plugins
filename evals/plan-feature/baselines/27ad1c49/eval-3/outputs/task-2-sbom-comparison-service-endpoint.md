## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison capability to trustify-backend: define model types for the structured diff response, implement the comparison logic in the SBOM service layer, and expose a new REST endpoint at `GET /api/v2/sbom/compare?left={id1}&right={id2}` that returns added/removed packages, version changes, new/resolved vulnerabilities, and license changes between two SBOMs.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison result model types: SbomComparisonResult containing AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, and LicenseChange structs
- `modules/fundamental/src/sbom/service/comparison.rs` — Comparison service with diff computation logic that fetches packages and advisories for two SBOMs and computes a structured diff
- `modules/fundamental/src/sbom/endpoints/compare.rs` — GET /api/v2/sbom/compare endpoint handler with left/right query parameters
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose comparison model
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod comparison;` to expose comparison service
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the /compare route alongside existing SBOM endpoints

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns structured diff between two SBOMs including added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, and license_changes

## Implementation Notes
Follow the existing module pattern in `modules/fundamental/src/sbom/` where model types live in `model/`, business logic in `service/`, and HTTP handlers in `endpoints/`.

Model types should derive `Serialize, Deserialize, Clone, Debug` following the pattern in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails).

The comparison service should:
1. Use `SbomService` from `modules/fundamental/src/sbom/service/sbom.rs` to fetch both SBOMs and their associated packages via the `entity/src/sbom_package.rs` join table.
2. Use `PackageService` from `modules/fundamental/src/package/service/mod.rs` to get package details including license info via `entity/src/package_license.rs`.
3. Use `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs` to correlate advisories via `entity/src/sbom_advisory.rs` and identify new/resolved vulnerabilities. Use the severity field from `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`.
4. Compute diff in memory — no new database tables per non-functional requirements.

The endpoint handler should follow the pattern in `modules/fundamental/src/sbom/endpoints/get.rs`: accept query parameters via Axum extractors, call the comparison service, return `Result<Json<SbomComparisonResult>, AppError>` using `common/src/error.rs` AppError with `.context()` wrapping.

Route registration in `modules/fundamental/src/sbom/endpoints/mod.rs` should add the compare route following the existing pattern for list and get routes.

Integration tests should follow the pattern in `tests/api/sbom.rs`: set up test database with two SBOMs containing different packages, call the compare endpoint, and assert response structure and content.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — fetch SBOM data and associated packages
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — fetch advisories for vulnerability correlation
- `modules/fundamental/src/package/service/mod.rs::PackageService` — fetch package data including licenses
- `common/src/error.rs::AppError` — error handling enum with IntoResponse
- `common/src/db/query.rs` — shared query builder helpers for database queries
- `entity/src/sbom_package.rs` — SBOM-Package join table for package resolution
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table for advisory correlation
- `entity/src/package_license.rs` — Package-License mapping for license change detection

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with structured diff JSON
- [ ] Response includes all six diff categories: added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes
- [ ] Returns 404 if either SBOM ID does not exist
- [ ] Returns 400 if left or right query parameter is missing
- [ ] Response time under 1s for SBOMs with up to 2000 packages each (p95)
- [ ] No new database tables — diff computed on-the-fly from existing data

## Test Requirements
- [ ] Integration test: compare two SBOMs with known package differences, verify added/removed packages in response
- [ ] Integration test: compare SBOMs with version changes, verify version_changes array contains correct left/right versions
- [ ] Integration test: verify 404 response when one SBOM ID does not exist
- [ ] Integration test: verify 400 response when query parameters are missing
- [ ] Integration test: compare identical SBOMs, verify all diff arrays are empty
