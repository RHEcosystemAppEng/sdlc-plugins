## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add SBOM comparison model types and diff computation service logic for the SBOM comparison view feature (TC-9003). This task creates the data structures that represent a structured diff between two SBOMs and implements the on-the-fly comparison logic that computes added/removed packages, version changes, new/resolved vulnerabilities, and license changes. No new database tables are introduced -- the diff is computed from existing package, advisory, and license data.

## Files to Modify
- `modules/fundamental/src/sbom/mod.rs` -- add comparison submodule declaration
- `modules/fundamental/src/sbom/model/mod.rs` -- re-export comparison model types
- `modules/fundamental/src/sbom/service/mod.rs` -- re-export comparison service

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` -- SbomComparisonResult struct with sub-structs: AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `modules/fundamental/src/sbom/service/comparison.rs` -- comparison diff computation logic: load packages and advisories for both SBOMs, compute set differences, detect version changes, identify new/resolved vulnerabilities, detect license changes

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct definitions, derive macros, and serialization.
- The comparison service should accept two SBOM IDs, load their associated packages via the `sbom_package` join entity (`entity/src/sbom_package.rs`), and compute the diff.
- For vulnerability diff: use the `sbom_advisory` join entity (`entity/src/sbom_advisory.rs`) to find advisories associated with each SBOM. New vulnerabilities are advisories present in the right SBOM but not the left; resolved vulnerabilities are the inverse.
- For license changes: use the `package_license` entity (`entity/src/package_license.rs`) to compare license assignments for packages present in both SBOMs.
- Version change direction (upgrade/downgrade) should be computed by comparing semver strings where possible.
- Performance target: p95 < 1s for SBOMs with up to 2000 packages each. Consider using HashSet-based lookups for efficient set operations on package names.
- Use `common/src/error.rs::AppError` for error handling with `.context()` wrapping.
- The response shape must match the Figma design contract:
  ```json
  {
    "added_packages": [{"name": "...", "version": "...", "license": "...", "advisory_count": 0}],
    "removed_packages": [{"name": "...", "version": "...", "license": "...", "advisory_count": 0}],
    "version_changes": [{"name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade"}],
    "new_vulnerabilities": [{"advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..."}],
    "resolved_vulnerabilities": [{"advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..."}],
    "license_changes": [{"name": "...", "left_license": "...", "right_license": "..."}]
  }
  ```

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- existing SBOM model struct; follow its derive macros and serialization patterns
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- existing service for fetching SBOM data; extend or compose with for comparison logic
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- package model with license field; reference for package data shape
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- advisory model with severity field; reference for vulnerability data shape
- `entity/src/sbom_package.rs` -- SBOM-Package join table entity for loading packages per SBOM
- `entity/src/sbom_advisory.rs` -- SBOM-Advisory join table entity for loading advisories per SBOM
- `entity/src/package_license.rs` -- Package-License mapping entity for license comparison
- `common/src/db/query.rs` -- shared query builder helpers for filtering and sorting

## Acceptance Criteria
- [ ] SbomComparisonResult struct is defined with all six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- [ ] Each diff category uses a dedicated sub-struct with the fields specified in the API contract
- [ ] Comparison service correctly computes added packages (in right but not left)
- [ ] Comparison service correctly computes removed packages (in left but not right)
- [ ] Comparison service correctly detects version changes with upgrade/downgrade direction
- [ ] Comparison service correctly identifies new vulnerabilities (advisories in right but not left)
- [ ] Comparison service correctly identifies resolved vulnerabilities (advisories in left but not right)
- [ ] Comparison service correctly detects license changes for packages present in both SBOMs
- [ ] No new database tables or migrations are created

## Test Requirements
- [ ] Unit test: comparison of two identical SBOMs returns empty diff (all categories have zero items)
- [ ] Unit test: comparison with added packages returns correct added_packages list
- [ ] Unit test: comparison with removed packages returns correct removed_packages list
- [ ] Unit test: comparison with version changes returns correct version_changes with direction
- [ ] Unit test: comparison with new vulnerabilities returns correct new_vulnerabilities with severity
- [ ] Unit test: comparison with resolved vulnerabilities returns correct resolved_vulnerabilities
- [ ] Unit test: comparison with license changes returns correct license_changes
- [ ] Unit test: performance test with 2000 packages per SBOM completes in < 1s

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
