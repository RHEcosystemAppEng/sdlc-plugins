# Task 2 — Add SBOM comparison diff model and service logic

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the data model structs and service method for computing a structured diff between two SBOMs. The comparison is computed on-the-fly from existing package and advisory data without requiring new database tables. The service loads both SBOMs with their associated packages, advisories, and licenses, then computes the diff across six categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new comparison model types
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare()` method to SbomService

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange structs

## API Changes
- Internal service API: `SbomService::compare(left_id: Uuid, right_id: Uuid) -> Result<SbomComparisonResult, AppError>` — NEW: computes structured diff between two SBOMs

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/`: each struct gets Serialize/Deserialize derives and lives in its own file, re-exported from `mod.rs`. See `summary.rs` and `details.rs` for the established pattern.
- The `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` already has `fetch` and `list` methods. Add a `compare` method following the same error handling pattern with `Result<T, AppError>` and `.context()` wrapping.
- Use the existing `PackageSummary` struct from `modules/fundamental/src/package/model/summary.rs` which includes the `license` field needed for license change detection.
- Use the existing `AdvisorySummary` struct from `modules/fundamental/src/advisory/model/summary.rs` which includes the `severity` field needed for vulnerability categorization.
- Load packages via `PackageService` in `modules/fundamental/src/package/service/mod.rs` and advisories via `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`.
- Use the `sbom_package` join entity (`entity/src/sbom_package.rs`) to find packages belonging to each SBOM, and `sbom_advisory` join entity (`entity/src/sbom_advisory.rs`) to find advisories for each SBOM.
- The comparison response must match this shape for the frontend:
  ```json
  {
    "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade|downgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical|high|medium|low", "title": "...", "affected_package": "..." }],
    "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
    "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
  }
  ```
- Non-functional requirement: p95 < 1s for SBOMs with up to 2000 packages each. Use efficient set operations (HashSet/HashMap) for diffing rather than nested loops.
- No new database tables are required — compute the diff from existing package, advisory, sbom_package, and sbom_advisory data.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains name, version, and license fields needed for package diff entries
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains advisory_id, severity, and title fields needed for vulnerability diff entries
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination, useful for loading packages and advisories efficiently
- `common/src/error.rs::AppError` — error type for consistent error handling in the new service method

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct and sub-structs are defined with Serialize/Deserialize
- [ ] `SbomService::compare()` correctly identifies added, removed, and version-changed packages
- [ ] `SbomService::compare()` correctly identifies new and resolved vulnerabilities
- [ ] `SbomService::compare()` correctly identifies license changes
- [ ] Direction field for version changes correctly classifies upgrades vs downgrades
- [ ] Comparison returns appropriate error when either SBOM ID is not found

## Test Requirements
- [ ] Unit test: comparison of two SBOMs with known added and removed packages
- [ ] Unit test: comparison detecting version upgrades and downgrades
- [ ] Unit test: comparison detecting new and resolved vulnerabilities
- [ ] Unit test: comparison detecting license changes
- [ ] Unit test: error case when left SBOM ID does not exist
- [ ] Unit test: error case when right SBOM ID does not exist

## Verification Commands
- `cargo test --package trustify-fundamental -- sbom::service::compare` — all comparison service tests pass
- `cargo check --package trustify-fundamental` — no compilation errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
