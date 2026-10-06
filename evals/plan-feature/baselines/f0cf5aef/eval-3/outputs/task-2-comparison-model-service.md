## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the data model structs and diff computation service for SBOM comparison. This task creates the `SbomComparisonResult` model with all six diff categories (added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, license changes) and adds a `compare` method to `SbomService` that fetches both SBOMs' packages, advisories, and licenses, then computes a structured diff.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — defines `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` structs with Serialize/Deserialize derives

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod comparison;` to export the new model module
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare(left_id, right_id) -> Result<SbomComparisonResult, AppError>` method to `SbomService`

## Implementation Notes
Per the backend module pattern (CONVENTIONS.md equivalent): each domain module follows `model/ + service/ + endpoints/` structure. The comparison model goes into the existing `sbom/model/` directory, and the service method goes into the existing `SbomService`.
Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's model directory scope.

Per the backend error handling convention: all service methods return `Result<T, AppError>` with `.context()` wrapping on database operations.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service scope.

**Diff computation approach:**
1. Load left SBOM's packages via `PackageService` (join through `sbom_package` entity)
2. Load right SBOM's packages via `PackageService`
3. Compute set difference for added/removed packages using package name as the key
4. For packages present in both, compare versions to populate `version_changes`
5. Load advisories for each SBOM via `AdvisoryService` (join through `sbom_advisory` entity)
6. Compute advisory set difference for new/resolved vulnerabilities
7. Compare license fields on shared packages for `license_changes`

**Response shape** (per feature requirements and Figma design):
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

The `direction` field in `VersionChange` should be computed by comparing semver versions: "upgrade" when right > left, "downgrade" when right < left.

**Performance:** The NFR requires p95 < 1s for SBOMs with up to 2000 packages each. Use efficient set operations (HashSet/HashMap by package name) rather than nested iteration. No new database tables — compute diff on-the-fly from existing data.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with `fetch` and `list` methods; add the `compare` method here
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing model struct to reference for serialization patterns
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — existing detail model with package/advisory relationships
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — has `severity` field needed for vulnerability diff entries
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — has `license` field needed for license change detection
- `entity/src/sbom_package.rs` — SBOM-Package join entity for loading packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join entity for loading advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping for license comparison

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct contains all six diff categories with correct field types
- [ ] All model structs derive `Serialize` and `Deserialize`
- [ ] `SbomService::compare` accepts two SBOM IDs and returns `Result<SbomComparisonResult, AppError>`
- [ ] `compare` returns `AppError` with appropriate context when either SBOM ID is not found
- [ ] `version_changes` entries correctly compute the `direction` field (upgrade/downgrade)
- [ ] Diff computation uses efficient set operations (not O(n^2) nested loops)

## Test Requirements
- [ ] Unit test: `compare` with two identical SBOMs returns all empty diff categories
- [ ] Unit test: `compare` with disjoint SBOMs returns all packages in added/removed
- [ ] Unit test: `compare` with overlapping packages correctly classifies version changes, added, and removed
- [ ] Unit test: `compare` correctly detects new and resolved vulnerabilities
- [ ] Unit test: `compare` correctly detects license changes
- [ ] Unit test: `compare` with nonexistent SBOM ID returns appropriate error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
