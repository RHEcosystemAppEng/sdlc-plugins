## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison model types and service logic that computes a structured diff between two SBOMs. The comparison service queries packages, advisories, and licenses for both SBOM IDs and produces a diff result containing: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. This is the core computation layer consumed by the comparison endpoint (Task 3).

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` -- SbomComparisonResult struct and sub-types (PackageDiff, VersionChange, VulnerabilityDiff, LicenseDiff) with Serialize derives
- `modules/fundamental/src/sbom/service/compare.rs` -- compare() method implementation that fetches package/advisory/license data for two SBOM IDs and computes the diff

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod comparison;` to export the new model module
- `modules/fundamental/src/sbom/service/mod.rs` -- add `pub mod compare;` to export the comparison service module

## Implementation Notes
Follow the existing module pattern in the sbom domain: model types in `model/` directory, service logic in `service/` directory. The comparison result struct should be serializable to JSON using serde.

Per CONVENTIONS.md module pattern: follow the established `model/ + service/ + endpoints/` structure used by the existing sbom, advisory, and package modules.
Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's `.rs` module file scope.

Per CONVENTIONS.md error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping for error propagation. See `modules/fundamental/src/sbom/service/sbom.rs` for the established error handling pattern.
Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's `.rs` file scope.

**Model type design:**
- `SbomComparisonResult` should contain six Vec fields corresponding to the six diff categories: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- `PackageDiff` fields: `name: String`, `version: String`, `license: Option<String>`, `advisory_count: i32`
- `VersionChange` fields: `name: String`, `left_version: String`, `right_version: String`, `direction: String` (values: "upgrade" or "downgrade")
- `VulnerabilityDiff` fields: `advisory_id: String`, `severity: String`, `title: String`, `affected_package: String`
- `LicenseDiff` fields: `name: String`, `left_license: String`, `right_license: String`

**Service logic:**
- Use `SbomService::fetch()` to load both SBOM entities by ID (see `modules/fundamental/src/sbom/service/sbom.rs`)
- Query the `sbom_package` join table (see `entity/src/sbom_package.rs`) to get packages for each SBOM
- Query the `sbom_advisory` join table (see `entity/src/sbom_advisory.rs`) to get advisories for each SBOM
- Query the `package_license` mapping (see `entity/src/package_license.rs`) for license data
- Compute set differences for added/removed packages, version comparisons for changed packages, and advisory cross-referencing for vulnerability diffs
- Performance consideration: the comparison must complete in p95 < 1s for SBOMs with up to 2000 packages each -- batch database queries rather than N+1 lookups

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- existing service with fetch/list methods for loading SBOM entities
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- advisory fetch/search methods for resolving vulnerability data
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- package fetch/list methods
- `common/src/model/paginated.rs::PaginatedResults` -- reference for response struct patterns with Serialize
- `common/src/error.rs::AppError` -- error type to use in Result returns

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct and all sub-types are defined with serde Serialize derives
- [ ] Comparison service correctly identifies added packages (in right SBOM but not left)
- [ ] Comparison service correctly identifies removed packages (in left SBOM but not right)
- [ ] Comparison service correctly identifies version changes with upgrade/downgrade direction
- [ ] Comparison service correctly identifies new vulnerabilities (advisories in right but not left)
- [ ] Comparison service correctly identifies resolved vulnerabilities (advisories in left but not right)
- [ ] Comparison service correctly identifies license changes between the two SBOMs
- [ ] Service returns AppError when either SBOM ID does not exist

## Test Requirements
- [ ] Unit test: comparing two empty SBOMs returns empty diff
- [ ] Unit test: comparing SBOM with packages against empty SBOM returns all packages as added/removed
- [ ] Unit test: version change detection correctly classifies upgrade vs downgrade using semver comparison
- [ ] Unit test: vulnerability diff correctly cross-references advisories across the two SBOMs
- [ ] Unit test: license change detection identifies packages with changed license strings
- [ ] Unit test: service returns error for non-existent SBOM ID

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
