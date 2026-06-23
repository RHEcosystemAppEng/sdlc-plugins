## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Create the SBOM comparison model structs and diff service that computes structured differences between two SBOMs. The service loads package lists, advisory associations, and license data for both SBOMs, then computes six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. No new database tables are needed -- the diff is computed on-the-fly from existing entity data.

## Files to Create
- `modules/fundamental/src/sbom/model/compare.rs` -- Response structs: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`
- `modules/fundamental/src/sbom/service/compare.rs` -- `SbomCompareService` with `compare(left_id, right_id)` method that queries existing package, advisory, and license data to compute the diff

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod compare;` re-export
- `modules/fundamental/src/sbom/service/mod.rs` -- Add `pub mod compare;` re-export

## Implementation Notes
- Follow the existing module pattern in `modules/fundamental/src/sbom/` where `model/` contains response structs and `service/` contains business logic.
- Reuse `PackageSummary` fields from `modules/fundamental/src/sbom/../package/model/summary.rs` for the `license` field in package diff structs.
- Reuse `AdvisorySummary` from `modules/fundamental/src/advisory/model/summary.rs` for the `severity` field in vulnerability diff structs.
- The `SbomComparison` struct must serialize to the JSON shape expected by the frontend (see feature spec): `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`.
- Use `SbomService` from `modules/fundamental/src/sbom/service/sbom.rs` to fetch SBOM details for both IDs.
- Use `PackageService` from `modules/fundamental/src/sbom/../package/service/mod.rs` to load package lists per SBOM.
- Use `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs` to load advisory associations per SBOM.
- Compute version change direction (upgrade vs downgrade) using semver comparison where possible; fall back to string comparison for non-semver versions.
- All handlers return `Result<T, AppError>` with `.context()` wrapping per `common/src/error.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- Fetch SBOM details by ID; reuse to load left and right SBOMs
- `modules/fundamental/src/sbom/../package/service/mod.rs::PackageService` -- Load package list for an SBOM; reuse to get package sets for diffing
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- Load advisories linked to an SBOM; reuse to compute vulnerability diff
- `common/src/error.rs::AppError` -- Standard error type for service-layer errors

## Acceptance Criteria
- [ ] `SbomComparison` struct serializes to the expected JSON shape with all six diff categories
- [ ] `SbomCompareService::compare()` returns correct diff for two SBOMs with known package differences
- [ ] `SbomCompareService::compare()` returns empty diff when both SBOMs are identical
- [ ] `SbomCompareService::compare()` returns `AppError::NotFound` when either SBOM ID does not exist
- [ ] Version change direction correctly identifies upgrades and downgrades

## Test Requirements
- [ ] Unit tests for `SbomCompareService::compare()` with mock data covering: added packages, removed packages, version changes (upgrade and downgrade), new vulnerabilities, resolved vulnerabilities, license changes
- [ ] Unit test for empty diff when comparing an SBOM to itself
- [ ] Unit test for error case when SBOM ID does not exist

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main

[sdlc-workflow] Description digest: sha256-md:6b8caf66157f4de25297619997f7a166b07302ffd5b517e90abf6aecec7fe539
