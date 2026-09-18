## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison diff model structs and implement the SbomComparisonService that computes a structured diff between two SBOMs. The service compares packages, advisory associations, and license mappings to produce a result containing added/removed packages, version changes, new/resolved vulnerabilities, and license changes.

## Files to Modify
- `modules/fundamental/src/sbom/mod.rs` — add `pub mod compare;` to expose the new comparison submodule
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod compare;` to expose the comparison service
- `modules/fundamental/Cargo.toml` — add any new dependencies if needed for diffing logic

## Files to Create
- `modules/fundamental/src/sbom/model/compare.rs` — SbomComparisonResult, PackageDiff, VersionChange, VulnerabilityDiff, LicenseChange structs with Serialize derive
- `modules/fundamental/src/sbom/service/compare.rs` — SbomComparisonService with `compare(left_id, right_id) -> Result<SbomComparisonResult, AppError>` method

## API Changes
- None (this task adds the model and service layer only; the endpoint is added in Task 3)

## Implementation Notes
- Follow the established module pattern: model structs in `model/compare.rs`, service logic in `service/compare.rs`. See existing `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/service/sbom.rs` for the pattern.
- The comparison service should:
  1. Fetch both SBOMs using the existing `SbomService::fetch` method
  2. Fetch packages for each SBOM using `PackageService` (via `sbom_package` join table)
  3. Compute set differences for packages (by package identifier)
  4. For packages in both SBOMs, compare versions and licenses
  5. Fetch advisory associations for each SBOM (via `sbom_advisory` join table)
  6. Compute new/resolved vulnerabilities by comparing advisory sets
- All error handling must use `Result<T, AppError>` with `.context()` wrapping per project convention.
- Per CONVENTIONS.md: follow the model/ + service/ + endpoints/ module pattern for the comparison domain. Applies: task creates `modules/fundamental/src/sbom/model/compare.rs` matching the convention's Rust module file scope.
- Per CONVENTIONS.md: use `Result<T, AppError>` with `.context()` for all error paths. Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's `.rs` error handling scope.
- The SbomComparisonResult struct should match the API response shape specified in the Figma design context:
  ```
  SbomComparisonResult {
    added_packages: Vec<PackageDiff>,
    removed_packages: Vec<PackageDiff>,
    version_changes: Vec<VersionChange>,
    new_vulnerabilities: Vec<VulnerabilityDiff>,
    resolved_vulnerabilities: Vec<VulnerabilityDiff>,
    license_changes: Vec<LicenseChange>,
  }
  ```
- The non-functional requirement specifies no new database tables — compute diff on-the-fly from existing entity data.
- Performance target: p95 < 1s for SBOMs with up to 2000 packages each. Consider fetching package lists in parallel (tokio::join!) and using HashSet-based diffing for O(n) comparison.

**Relevant constraints from docs/constraints.md:**
- Commit rules (section 2): every commit must reference TC-9003 in the footer, follow Conventional Commits, include --trailer="Assisted-by: Claude Code"
- PR rules (section 3): branch named after Jira issue ID, PR link posted to Jira task
- Code change rules (section 5): changes scoped to listed files, inspect code before modifying, follow referenced patterns, no duplication

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing SBOM fetch/list logic to retrieve SBOM data for comparison
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM summary struct for reference on serialization patterns
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing package model with license field, reference for PackageDiff struct design
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing advisory model with severity field, reference for VulnerabilityDiff struct design
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error type to use for all fallible operations

## Acceptance Criteria
- [ ] SbomComparisonResult struct is defined with fields for added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes
- [ ] PackageDiff struct includes name, version, license, and advisory_count fields
- [ ] VersionChange struct includes name, left_version, right_version, and direction (upgrade/downgrade) fields
- [ ] VulnerabilityDiff struct includes advisory_id, severity, title, and affected_package fields
- [ ] LicenseChange struct includes name, left_license, and right_license fields
- [ ] SbomComparisonService.compare() correctly identifies added packages (in right but not left)
- [ ] SbomComparisonService.compare() correctly identifies removed packages (in left but not right)
- [ ] SbomComparisonService.compare() correctly identifies version changes with upgrade/downgrade direction
- [ ] SbomComparisonService.compare() correctly identifies new vulnerabilities (advisories affecting right but not left)
- [ ] SbomComparisonService.compare() correctly identifies resolved vulnerabilities (advisories affecting left but not right)
- [ ] SbomComparisonService.compare() correctly identifies license changes between matching packages
- [ ] All structs derive Serialize for JSON response serialization
- [ ] Error handling uses Result<T, AppError> with .context() wrapping

## Test Requirements
- [ ] Unit test: compare two SBOMs with identical packages returns empty diff
- [ ] Unit test: compare SBOMs where right has an additional package returns it in added_packages
- [ ] Unit test: compare SBOMs where left has a package not in right returns it in removed_packages
- [ ] Unit test: compare SBOMs where a package version differs returns it in version_changes with correct direction
- [ ] Unit test: compare SBOMs where right has a new advisory returns it in new_vulnerabilities
- [ ] Unit test: compare SBOMs where left has an advisory not in right returns it in resolved_vulnerabilities
- [ ] Unit test: compare SBOMs where a package license changed returns it in license_changes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main (trustify-backend)
