## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add SBOM comparison model types and diff service logic to compute a structured diff between two SBOMs. The service queries existing package, advisory, and license data for both SBOMs and computes six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. No new database tables are needed — all diffs are computed on-the-fly from existing entity relationships.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new comparison module
- `modules/fundamental/src/sbom/service/mod.rs` — re-export the new comparison service module
- `modules/fundamental/Cargo.toml` — add any needed dependencies

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — define SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, and LicenseChange structs with Serialize/Deserialize derives
- `modules/fundamental/src/sbom/service/comparison.rs` — implement SbomComparisonService with a `compare(left_id, right_id) -> Result<SbomComparisonResult, AppError>` method

## API Changes
- None (service layer only; endpoint is added in Task 3)

## Implementation Notes
- Follow the existing module pattern: model types in `model/` and service logic in `service/`. See `modules/fundamental/src/sbom/model/summary.rs` for the struct definition pattern (derive Serialize, Deserialize, Clone, Debug) and `modules/fundamental/src/sbom/service/sbom.rs` for the service pattern.
  - Per CONVENTIONS.md §Module Pattern: place model types in `model/comparison.rs` and service logic in `service/comparison.rs`, following the `model/ + service/ + endpoints/` structure.
    Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's `.rs` module scope.
- Use `Result<T, AppError>` for all service methods with `.context()` wrapping for error messages, per the existing error handling pattern in `common/src/error.rs`.
  - Per CONVENTIONS.md §Error Handling: return `Result<SbomComparisonResult, AppError>` and use `.context()` on fallible operations.
    Applies: task creates `modules/fundamental/src/sbom/service/comparison.rs` matching the convention's `.rs` handler scope.
- Query packages for each SBOM via the `sbom_package` join table (`entity/src/sbom_package.rs`) and the `package` entity (`entity/src/package.rs`). Use SeaORM queries following the patterns in `modules/fundamental/src/sbom/service/sbom.rs`.
- Query advisories for each SBOM via the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) and the `advisory` entity (`entity/src/advisory.rs`). Use the `AdvisorySummary` severity field for vulnerability severity classification.
- Query license data via the `package_license` entity (`entity/src/package_license.rs`).
- For the `direction` field in VersionChange, compare version strings to determine "upgrade" vs "downgrade" (semver comparison if applicable, lexicographic fallback).
- The comparison response shape must match the frontend's expected contract:
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
- Performance: p95 < 1s for SBOMs with up to 2000 packages each. Use efficient set-difference operations (HashSet-based) rather than nested loops.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service for fetching SBOM data; reuse its database query patterns for loading packages and advisories per SBOM
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing model struct; follow its serialization pattern for new comparison types
- `entity/src/package.rs` — Package entity with fields needed for diff comparison (name, version)
- `entity/src/advisory.rs` — Advisory entity with severity and title fields
- `common/src/db/query.rs` — shared query builder helpers for filtering and sorting

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct defined with all six diff sections (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- [ ] Each diff section struct has the fields matching the expected JSON response shape
- [ ] `SbomComparisonService::compare()` correctly computes added packages (in right but not left)
- [ ] `SbomComparisonService::compare()` correctly computes removed packages (in left but not right)
- [ ] `SbomComparisonService::compare()` correctly computes version changes (same package name, different version)
- [ ] `SbomComparisonService::compare()` correctly computes new vulnerabilities (advisories in right SBOM not in left)
- [ ] `SbomComparisonService::compare()` correctly computes resolved vulnerabilities (advisories in left SBOM not in right)
- [ ] `SbomComparisonService::compare()` correctly computes license changes (same package, different license)
- [ ] All methods return `Result<T, AppError>` with descriptive `.context()` messages
- [ ] Structs derive Serialize, Deserialize, Clone, Debug

## Test Requirements
- [ ] Unit test: compare two SBOMs with added packages produces correct AddedPackage entries
- [ ] Unit test: compare two SBOMs with removed packages produces correct RemovedPackage entries
- [ ] Unit test: compare two SBOMs with version changes produces correct VersionChange entries with direction
- [ ] Unit test: compare two SBOMs with new and resolved vulnerabilities produces correct entries
- [ ] Unit test: compare two SBOMs with license changes produces correct LicenseChange entries
- [ ] Unit test: compare identical SBOMs produces empty diff sections
- [ ] Unit test: compare with nonexistent SBOM ID returns appropriate AppError

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
