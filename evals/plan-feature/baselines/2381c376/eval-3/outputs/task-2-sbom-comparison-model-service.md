## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison data model structs and service logic for computing a structured diff between two SBOMs. The service fetches packages, advisories, and licenses for both SBOMs from existing data and computes six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. No new database tables are needed — the diff is computed on-the-fly from existing entities.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — structs for the comparison result: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange
- `modules/fundamental/src/sbom/service/comparison.rs` — SbomComparisonService with compare(left_id, right_id) method

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod comparison;` to expose the new model module
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod comparison;` to expose the new service module
- `modules/fundamental/Cargo.toml` — add any required dependencies if needed

## Implementation Notes
The comparison service should:

1. Use the existing `SbomService` (in `modules/fundamental/src/sbom/service/sbom.rs`) to fetch SBOM details for both IDs. Follow the existing service call patterns with `.context()` error wrapping.

2. Use the existing `PackageService` (in `modules/fundamental/src/package/service/mod.rs`) to fetch packages for each SBOM. Use `PackageSummary` (from `modules/fundamental/src/package/model/summary.rs`) which includes the `license` field.

3. Use the existing `AdvisoryService` (in `modules/fundamental/src/advisory/service/advisory.rs`) to look up advisories for each SBOM. Use `AdvisorySummary` (from `modules/fundamental/src/advisory/model/summary.rs`) which includes the `severity` field.

4. Compute the diff by comparing package sets:
   - Added packages: in right but not in left (by package name)
   - Removed packages: in left but not in right
   - Version changes: in both but different versions; determine direction (upgrade/downgrade) by comparing version strings
   - New vulnerabilities: advisories linked to right SBOM's packages that are not linked to left SBOM's packages
   - Resolved vulnerabilities: advisories linked to left SBOM's packages that are not linked to right SBOM's packages
   - License changes: packages present in both SBOMs but with different license values

5. Return `SbomComparisonResult` with all six diff categories.

Model structs should derive `Serialize, Deserialize, Clone, Debug` and follow the naming pattern of existing model structs (e.g., `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs`).

**Reuse candidates:**
- `common/src/error.rs::AppError` — use for error handling; all service methods should return `Result<T, AppError>`
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — use `fetch` method to load each SBOM by ID
- `modules/fundamental/src/package/service/mod.rs::PackageService` — use `list` to retrieve packages per SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — use `list` or `search` to find advisories per SBOM

Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ structure for the new comparison module.
Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's model/ directory scope.

Per CONVENTIONS.md §Error Handling: all handlers and service methods must return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/service/comparison.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service for fetching SBOM details by ID; reuse for loading left/right SBOMs
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing service for fetching packages; reuse for loading packages per SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing service for fetching advisories; reuse for finding advisories linked to SBOM packages
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference struct for naming and derive patterns
- `common/src/error.rs::AppError` — shared error type for all service results

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct contains fields for all six diff categories: added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes
- [ ] Each diff category struct includes the fields specified in the API response shape (see Feature description and Figma context)
- [ ] `SbomComparisonService::compare(left_id, right_id)` correctly identifies added and removed packages
- [ ] Version changes include direction (upgrade/downgrade)
- [ ] New vulnerabilities include advisory_id, severity, title, and affected_package
- [ ] Resolved vulnerabilities include advisory_id, severity, title, and previously_affected_package
- [ ] License changes include package name, left_license, and right_license
- [ ] All model structs derive Serialize and Deserialize for JSON response serialization
- [ ] Service returns appropriate errors when an SBOM ID is not found

## Test Requirements
- [ ] Unit test: compare two SBOMs with identical packages returns empty diff
- [ ] Unit test: compare SBOMs where right has additional packages returns them in added_packages
- [ ] Unit test: compare SBOMs where left has packages not in right returns them in removed_packages
- [ ] Unit test: compare SBOMs where a package has a different version returns it in version_changes with correct direction
- [ ] Unit test: compare SBOMs where right has new advisory links returns them in new_vulnerabilities
- [ ] Unit test: compare SBOMs where left has advisory links not in right returns them in resolved_vulnerabilities
- [ ] Unit test: compare SBOMs where a package has a different license returns it in license_changes
- [ ] Unit test: compare with non-existent SBOM ID returns an appropriate error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
