## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the SBOM comparison model types and service logic that computes a structured diff between two SBOMs. The service loads package lists, advisory associations, and license data for both SBOMs, then computes added/removed packages, version changes, new/resolved vulnerabilities, and license changes. No new database tables are needed -- the diff is computed on-the-fly from existing entity data.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` -- Structs for the comparison result: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `modules/fundamental/src/sbom/service/compare.rs` -- `SbomService::compare()` method that accepts two SBOM IDs and returns `SbomComparison`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod comparison;` to expose comparison types
- `modules/fundamental/src/sbom/service/mod.rs` -- Add `pub mod compare;` to expose comparison service logic

## Implementation Notes
Follow the existing model/service module pattern established in `modules/fundamental/src/sbom/`. The `SbomComparison` struct should be serializable with `serde::Serialize` and `utoipa::ToSchema` for OpenAPI generation, matching the conventions used by `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` and `SbomDetails` in `modules/fundamental/src/sbom/model/details.rs`.

The comparison service method should:
1. Use `SbomService` methods in `modules/fundamental/src/sbom/service/sbom.rs` to load both SBOMs
2. Use `PackageService` in `modules/fundamental/src/package/service/mod.rs` to load package lists for each SBOM via the `sbom_package` join entity in `entity/src/sbom_package.rs`
3. Use `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` to load advisories linked to each SBOM via the `sbom_advisory` join entity in `entity/src/sbom_advisory.rs`
4. Use the `package_license` entity in `entity/src/package_license.rs` to resolve license data for license change detection
5. Return `Result<SbomComparison, AppError>` following the error handling pattern in `common/src/error.rs` with `.context()` wrapping

The `direction` field in `VersionChange` should be an enum with `Upgrade` and `Downgrade` variants determined by semver comparison.

The comparison must meet the p95 < 1s requirement for SBOMs with up to 2000 packages. Use HashMaps keyed by package name for O(n) diffing rather than nested iteration.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- Existing service with fetch/list methods for loading SBOM data
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- Existing service for loading package lists
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- Existing service for loading advisory data
- `common/src/error.rs::AppError` -- Standard error type for Result returns
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- Pattern reference for struct definition with serde/utoipa derives
- `entity/src/sbom_package.rs` -- Join entity for SBOM-to-Package relationships
- `entity/src/sbom_advisory.rs` -- Join entity for SBOM-to-Advisory relationships
- `entity/src/package_license.rs` -- Entity for package license mappings

## Acceptance Criteria
- [ ] `SbomComparison` struct contains all six diff categories: added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes
- [ ] Each diff category struct includes all fields specified in the feature requirements
- [ ] `SbomService::compare()` returns a correct diff for two SBOMs with known differences
- [ ] Version change direction correctly distinguishes upgrades from downgrades
- [ ] Comparison completes within 1 second for SBOMs with up to 2000 packages each

## Test Requirements
- [ ] Unit test: comparing two identical SBOMs returns empty diff categories
- [ ] Unit test: added and removed packages are correctly identified
- [ ] Unit test: version changes detect upgrade vs. downgrade direction
- [ ] Unit test: new and resolved vulnerabilities are correctly identified across SBOM boundaries
- [ ] Unit test: license changes are detected when package license differs between SBOMs

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main

[sdlc-workflow] Description digest: sha256-md:b3f4a5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4
