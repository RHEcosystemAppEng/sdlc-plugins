# Task 1 — Add SBOM comparison diff endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add a new `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint that computes a structured diff between two SBOMs. The diff includes added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The comparison is computed on-the-fly from existing package, advisory, and license data without requiring new database tables.

This endpoint supports the SBOM comparison feature (TC-9003), enabling security analysts to quickly identify what changed between two SBOM versions instead of manually comparing two detail pages.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare` method to SbomService that computes the structured diff between two SBOMs
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the new comparison route under `/api/v2/sbom/compare`
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new comparison model types
- `server/src/main.rs` — no changes needed if sbom module routes are already mounted (verify)

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — define `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` structs
- `modules/fundamental/src/sbom/endpoints/compare.rs` — handler for `GET /api/v2/sbom/compare` that parses `left`/`right` query params, calls `SbomService::compare`, and returns the result
- `tests/api/sbom_compare.rs` — integration tests for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: accepts two SBOM IDs as query parameters, returns a `SbomComparisonResult` JSON response containing `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, and `license_changes` arrays

## Implementation Notes
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/get.rs` for handler structure: extract query params, call service, return `Result<Json<T>, AppError>` with `.context()` error wrapping.
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` for struct definitions with serde derive macros.
- The comparison logic should query the `sbom_package` join table (`entity/src/sbom_package.rs`) to get packages for each SBOM, then compute set differences. Use `entity/src/package_license.rs` for license data and `entity/src/sbom_advisory.rs` for advisory data.
- Use `common/src/db/query.rs` query helpers for any database queries needed during diff computation.
- All handlers return `Result<T, AppError>` using the error type from `common/src/error.rs`.
- Do NOT create new database tables — the Feature requirement explicitly states the diff must be computed on-the-fly from existing data.
- Performance requirement: p95 response time < 1s for SBOMs with up to 2000 packages each. Consider efficient set operations (HashSet-based diffing) rather than nested loops.
- The `direction` field in `VersionChange` should be computed by comparing semver versions: "upgrade" when right > left, "downgrade" when right < left.
- The `severity` field in vulnerability types should use the severity from `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`).
- Integration tests should follow the pattern in `tests/api/sbom.rs`: hit a real PostgreSQL test database, use `assert_eq!(resp.status(), StatusCode::OK)` pattern.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service to extend with the comparison method; follow fetch/list method patterns for database access
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying packages belonging to each SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for querying advisories affecting each SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for license comparison
- `common/src/error.rs::AppError` — error handling enum implementing IntoResponse for consistent error responses
- `modules/fundamental/src/sbom/endpoints/get.rs` — endpoint handler pattern demonstrating Axum handler structure with SeaORM queries

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns 200 with a structured diff JSON response
- [ ] Response includes `added_packages` (packages in right but not left) with name, version, license, advisory_count fields
- [ ] Response includes `removed_packages` (packages in left but not right) with name, version, license, advisory_count fields
- [ ] Response includes `version_changes` (packages in both with different versions) with name, left_version, right_version, direction fields
- [ ] Response includes `new_vulnerabilities` (advisories affecting right but not left) with advisory_id, severity, title, affected_package fields
- [ ] Response includes `resolved_vulnerabilities` (advisories affecting left but not right) with advisory_id, severity, title, previously_affected_package fields
- [ ] Response includes `license_changes` (packages whose license changed) with name, left_license, right_license fields
- [ ] Endpoint returns 404 when either SBOM ID does not exist
- [ ] Endpoint returns 400 when left or right query parameter is missing
- [ ] No new database tables or migrations are created

## Test Requirements
- [ ] Integration test: compare two SBOMs with known package differences and verify the correct added/removed packages in the response
- [ ] Integration test: compare two SBOMs with overlapping packages at different versions and verify version_changes with correct direction
- [ ] Integration test: compare two SBOMs with different advisory associations and verify new/resolved vulnerabilities
- [ ] Integration test: compare two SBOMs with packages whose licenses changed and verify license_changes
- [ ] Integration test: compare an SBOM with itself and verify all diff arrays are empty
- [ ] Integration test: request with non-existent SBOM ID returns 404
- [ ] Integration test: request with missing query parameters returns 400

## Dependencies
None — this is the first task in the feature.
