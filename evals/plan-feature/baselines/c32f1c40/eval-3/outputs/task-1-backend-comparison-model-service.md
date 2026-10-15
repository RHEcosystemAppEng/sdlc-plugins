## Repository
trustify-backend

## Target Branch
main

## Description
Add SBOM comparison model types and service logic to compute a structured diff between two SBOMs. The comparison service retrieves package lists, advisory associations, and license data for both SBOMs, then produces a structured result containing added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. No new database tables are needed — the diff is computed on-the-fly from existing entity data.

## Files to Create
- `modules/fundamental/src/sbom/model/compare.rs` — Comparison result structs: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomCompareService` with a `compare(left_id, right_id)` method that computes the structured diff

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Re-export comparison types from `compare` submodule
- `modules/fundamental/src/sbom/service/mod.rs` — Re-export `SbomCompareService` from `compare` submodule
- `modules/fundamental/src/sbom/mod.rs` — Ensure model and service submodules are publicly accessible

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: Returns `SbomComparisonResult` with structured diff (endpoint handler added in Task 2)

## Implementation Notes
- Follow the existing module pattern: model types in `model/compare.rs`, service logic in `service/compare.rs`. See `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/service/sbom.rs` for the established pattern.
  Applies: task creates `modules/fundamental/src/sbom/model/compare.rs` matching the convention's Rust module file scope.
- Per CONVENTIONS.md §Error handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping on fallible operations. See `modules/fundamental/src/sbom/service/sbom.rs` for examples.
  Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's `.rs` file scope.
- The comparison response shape must match the Figma design's expected backend contract:
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
- Use `#[derive(Serialize, Deserialize, Clone, Debug)]` on all model structs, consistent with `SbomSummary` and `SbomDetails`.
- The `direction` field in `VersionChange` should be computed by comparing semver versions (upgrade vs downgrade).
- NFR: Comparison must complete in p95 < 1s for SBOMs with up to 2000 packages each. Use efficient set operations (HashSet/HashMap) for package diffing rather than nested loops.
- Use the `PackageSummary` struct's `license` field for license comparison, and `AdvisorySummary`'s `severity` field for vulnerability severity.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Fetch SBOM details and associated packages; reuse fetch logic rather than writing raw queries
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Fetch package data including license information
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Fetch advisory data for vulnerability comparison
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Existing struct with `license` field; use as basis for package comparison fields
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Existing struct with `severity` field; use for vulnerability entries
- `common/src/error.rs::AppError` — Standard error type for service methods

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- [ ] Each diff category has a dedicated struct with fields matching the expected response shape
- [ ] `SbomCompareService::compare(left_id, right_id)` correctly computes added packages (present in right but not left)
- [ ] `SbomCompareService::compare(left_id, right_id)` correctly computes removed packages (present in left but not right)
- [ ] `SbomCompareService::compare(left_id, right_id)` correctly computes version changes with upgrade/downgrade direction
- [ ] `SbomCompareService::compare(left_id, right_id)` correctly computes new vulnerabilities (advisories affecting right but not left)
- [ ] `SbomCompareService::compare(left_id, right_id)` correctly computes resolved vulnerabilities (advisories affecting left but not right)
- [ ] `SbomCompareService::compare(left_id, right_id)` correctly computes license changes (same package, different license)
- [ ] Service returns `AppError` with appropriate context for invalid SBOM IDs

## Test Requirements
- [ ] Unit test: compare two SBOMs where the right has additional packages — verify added_packages is populated correctly
- [ ] Unit test: compare two SBOMs where the left has packages not in the right — verify removed_packages is populated correctly
- [ ] Unit test: compare two SBOMs with overlapping packages at different versions — verify version_changes includes direction
- [ ] Unit test: compare two SBOMs with different advisory associations — verify new_vulnerabilities and resolved_vulnerabilities
- [ ] Unit test: compare two SBOMs with license changes on the same package — verify license_changes
- [ ] Unit test: compare with invalid SBOM ID returns appropriate error

## Dependencies
- None (first task in the chain)
