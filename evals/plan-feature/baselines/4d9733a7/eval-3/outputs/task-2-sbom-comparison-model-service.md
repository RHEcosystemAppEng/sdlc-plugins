## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison diff model types and service logic that computes a structured diff between two SBOMs. The service queries existing package, advisory, and license data from the database to produce a comparison result containing added/removed packages, version changes, new/resolved vulnerabilities, and license changes. No new database tables are needed -- the diff is computed on-the-fly from existing `sbom_package`, `sbom_advisory`, and `package_license` join tables.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` -- Comparison result model types: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `modules/fundamental/src/sbom/service/comparison.rs` -- SbomComparisonService with compare() method that accepts two SBOM IDs and returns SbomComparisonResult

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod comparison;` to expose comparison models
- `modules/fundamental/src/sbom/service/mod.rs` -- Add `pub mod comparison;` to expose comparison service
- `modules/fundamental/Cargo.toml` -- Add any necessary dependencies if needed

## Implementation Notes
- Follow the existing module pattern: model types in `model/` and service logic in `service/`. See `modules/fundamental/src/sbom/model/summary.rs` for the SbomSummary struct pattern and `modules/fundamental/src/sbom/service/sbom.rs` for the SbomService pattern.
- The comparison service should accept two SBOM IDs (UUIDs) and:
  1. Load packages for both SBOMs via the `sbom_package` join table and `package` entity
  2. Compute set differences for added/removed packages
  3. Detect version changes for packages present in both SBOMs
  4. Load advisories for both SBOMs via the `sbom_advisory` join table and `advisory` entity
  5. Compute new/resolved vulnerabilities as set differences on advisory IDs
  6. Load license data via `package_license` and detect license changes
- Return `Result<SbomComparisonResult, AppError>` following the error handling pattern in `common/src/error.rs` with `.context()` wrapping on database queries.
- The response shape must match the Figma design contract:
  ```json
  {
    "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..." }],
    "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
    "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
  }
  ```
- Performance requirement: p95 < 1s for SBOMs with up to 2000 packages each. Use efficient set operations and minimize database round-trips by batching queries.
- Per CONVENTIONS.md: use SeaORM entities for all database queries and follow the `model/ + service/ + endpoints/` module structure.
  Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's Rust module scope.
- Per CONVENTIONS.md: return `Result<T, AppError>` with `.context()` wrapping for all service methods.
  Applies: task creates `modules/fundamental/src/sbom/service/comparison.rs` matching the convention's Rust service scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- existing service with fetch/list methods; reuse the database connection and query patterns for loading SBOM data
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- existing model struct; follow the same serde serialization pattern for comparison result types
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- contains severity field; reuse the severity representation for vulnerability entries
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- contains license field; reuse for package data in diff results
- `common/src/db/query.rs` -- shared query builder helpers for database queries
- `entity/src/sbom_package.rs` -- SBOM-Package join table entity for loading package associations
- `entity/src/sbom_advisory.rs` -- SBOM-Advisory join table entity for loading advisory associations
- `entity/src/package_license.rs` -- Package-License mapping entity for license data

## Acceptance Criteria
- [ ] SbomComparisonResult struct is defined with all six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- [ ] Each diff category has its own typed struct (AddedPackage, RemovedPackage, etc.) matching the API response shape
- [ ] compare() service method accepts two SBOM IDs and returns Result<SbomComparisonResult, AppError>
- [ ] Version change detection correctly identifies upgrade vs downgrade direction
- [ ] Vulnerability severity is included in new/resolved vulnerability entries
- [ ] Advisory count is included in added/removed package entries

## Test Requirements
- [ ] Unit test: compare two SBOMs with non-overlapping packages produces correct added/removed sets
- [ ] Unit test: compare two SBOMs with shared packages at different versions produces correct version_changes with direction
- [ ] Unit test: compare two SBOMs where right SBOM has new advisory produces correct new_vulnerabilities
- [ ] Unit test: compare two SBOMs where left SBOM advisory is absent in right produces correct resolved_vulnerabilities
- [ ] Unit test: compare two SBOMs with license changes produces correct license_changes
- [ ] Unit test: compare SBOM with itself produces empty diff (no changes in any category)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
