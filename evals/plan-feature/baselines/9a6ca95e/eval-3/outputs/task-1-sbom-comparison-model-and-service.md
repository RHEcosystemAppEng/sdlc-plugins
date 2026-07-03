## Repository

trustify-backend

## Target Branch

main

## Priority

Critical

## Fix Versions

RHTPA 1.5.0

## Description

Add the data model structs and service logic for computing a structured diff between two SBOMs. This task introduces the comparison result types (added/removed packages, version changes, new/resolved vulnerabilities, license changes) and a `compare` method on `SbomService` that loads both SBOMs' package and advisory data, computes the diff in memory, and returns a typed result. No new database tables are required -- the diff is computed on-the-fly from existing package, advisory, and license data joined through the `sbom_package` and `sbom_advisory` tables.

## Acceptance Criteria

- [ ] A `SbomComparisonResult` struct exists with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] Supporting structs exist for each diff category: `PackageDiffEntry` (name, version, license, advisory_count), `VersionChangeEntry` (name, left_version, right_version, direction), `VulnerabilityDiffEntry` (advisory_id, severity, title, affected_package), `LicenseChangeEntry` (name, left_license, right_license)
- [ ] `SbomService` has a `compare(left_id, right_id)` method that returns `Result<SbomComparisonResult, AppError>`
- [ ] The comparison method loads packages for both SBOMs via existing `PackageService` queries and computes set differences by package name
- [ ] Version changes are detected for packages present in both SBOMs with differing version strings; the `direction` field is set to `"upgrade"` or `"downgrade"` based on semver comparison (fall back to lexicographic if not valid semver)
- [ ] New and resolved vulnerabilities are computed by comparing advisory sets linked to each SBOM via the `sbom_advisory` join table
- [ ] License changes are computed by comparing the `license` field on packages present in both SBOMs
- [ ] All structs derive `Serialize` and implement `utoipa::ToSchema` for OpenAPI generation
- [ ] The method returns `AppError::NotFound` if either SBOM ID does not exist

## Test Requirements

- [ ] Unit test: comparison of two SBOMs with known package sets produces the correct diff categories
- [ ] Unit test: version direction correctly identifies upgrades vs downgrades
- [ ] Unit test: requesting a non-existent SBOM ID returns `AppError::NotFound`
- [ ] Unit test: comparing an SBOM with itself returns empty diff lists

## Files to Modify

- `modules/fundamental/src/sbom/model/mod.rs` -- re-export new comparison module
- `modules/fundamental/src/sbom/service/sbom.rs` -- add `compare` method to `SbomService`

## Files to Create

- `modules/fundamental/src/sbom/model/comparison.rs` -- `SbomComparisonResult` and supporting diff structs

## Implementation Notes

- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `details.rs` for struct layout, derive macros, and `ToSchema` implementation.
- Use `common/src/error.rs` `AppError` enum for error handling, wrapping database errors with `.context()` as seen in `sbom.rs` service methods.
- Load package data using the existing query patterns in `modules/fundamental/src/package/service/mod.rs` (`PackageService`).
- Load advisory data via `modules/fundamental/src/advisory/service/advisory.rs` (`AdvisoryService`).
- Join SBOM-to-package via `entity/src/sbom_package.rs` and SBOM-to-advisory via `entity/src/sbom_advisory.rs`.
- License data is available on the `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs`.
- Severity is available on the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs`.

## Conventions

- **Error Handling**: All service methods return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's error handling scope.
- **Module pattern**: Each domain module follows `model/ + service/ + endpoints/` structure. Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's file organization scope.
