## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the data models and service-layer logic for computing structured diffs between two SBOMs. This is the core comparison engine that identifies added/removed packages, version changes, new/resolved vulnerabilities, and license changes between two SBOM versions. The service fetches package and advisory data for both SBOMs from the existing database entities and computes the diff in-memory (no new database tables required per non-functional requirements).

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` -- comparison result structs: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`
- `modules/fundamental/src/sbom/service/compare.rs` -- comparison logic: `SbomService::compare()` method implementation

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod comparison;` to expose the new comparison models
- `modules/fundamental/src/sbom/service/mod.rs` -- add `pub mod compare;` to expose the comparison service logic

## API Changes
- `SbomService::compare(left_id, right_id) -> Result<SbomComparisonResult, AppError>` -- NEW: computes diff between two SBOMs

## Implementation Notes
Per CONVENTIONS.md Module pattern: follow the established `model/ + service/ + endpoints/` structure. This task covers the model and service layers; the endpoint layer is handled by Task 3.
Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md Error handling: all service methods must return `Result<T, AppError>` and use `.context()` for error wrapping.
Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's `.rs` file scope.

**Comparison algorithm outline:**
1. Fetch all packages for `left_id` via `sbom_package` join entity and `package` entity
2. Fetch all packages for `right_id` via the same entities
3. Build `HashMap<package_name, PackageInfo>` for each side
4. Compute set difference for added/removed packages
5. For packages present in both, compare version fields for `VersionChange` entries
6. For packages present in both, compare license fields via `package_license` entity for `LicenseChange` entries
7. Fetch advisories linked to each SBOM via `sbom_advisory` join entity
8. Compute set difference for new/resolved vulnerabilities, including `severity` from `AdvisorySummary`

**Performance requirement:** p95 < 1s for SBOMs with up to 2,000 packages each. Use efficient set operations (HashMaps) rather than nested iteration.

**Response shape:**
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
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- existing service with `fetch` and `list` methods; extend with `compare` method
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- existing SBOM model; reference for struct patterns and serde derive macros
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` -- existing detail model with package/advisory data
- `entity/src/sbom_package.rs` -- SBOM-Package join entity for querying packages per SBOM
- `entity/src/package.rs` -- Package entity with name, version fields
- `entity/src/package_license.rs` -- Package-License mapping entity
- `entity/src/sbom_advisory.rs` -- SBOM-Advisory join entity for querying advisories per SBOM
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- existing advisory model with `severity` field
- `common/src/error.rs::AppError` -- existing error enum for consistent error handling

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- [ ] `SbomService::compare()` correctly identifies added and removed packages between two SBOMs
- [ ] `SbomService::compare()` correctly identifies version changes with upgrade/downgrade direction
- [ ] `SbomService::compare()` correctly identifies new and resolved vulnerabilities with severity
- [ ] `SbomService::compare()` correctly identifies license changes
- [ ] All structs derive `Serialize` and `Deserialize` for JSON response serialization
- [ ] Error cases handled: SBOM not found returns appropriate `AppError`

## Test Requirements
- [ ] Unit test: comparison of two SBOMs with known package differences produces correct added/removed lists
- [ ] Unit test: comparison of SBOMs with version changes correctly classifies upgrade vs downgrade
- [ ] Unit test: comparison with new vulnerabilities includes correct severity and affected package
- [ ] Unit test: comparison with license changes includes both left and right license values
- [ ] Unit test: comparison of identical SBOMs returns empty diff sections
- [ ] Unit test: comparison with non-existent SBOM ID returns AppError

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
