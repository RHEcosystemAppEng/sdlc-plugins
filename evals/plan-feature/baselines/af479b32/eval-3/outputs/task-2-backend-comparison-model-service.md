## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add SBOM comparison model types and diff service logic to support structured comparison between two SBOM versions. The comparison computes the diff on-the-fly from existing package, advisory, and license data without new database tables, as specified in the feature NFRs. This is the foundation for the comparison endpoint added in Task 3.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` -- SbomComparisonResult struct and sub-structs for each diff category (AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
- `modules/fundamental/src/sbom/service/compare.rs` -- comparison logic: fetch packages and advisories for both SBOMs, compute added/removed packages, version changes, new/resolved vulnerabilities, license changes

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod comparison;` to expose the new comparison model
- `modules/fundamental/src/sbom/service/mod.rs` -- add `pub mod compare;` to expose the new comparison service
- `modules/fundamental/src/lib.rs` -- ensure sbom module re-exports comparison types if needed

## Implementation Notes

The comparison service must:
1. Fetch all packages for both SBOMs via the existing `sbom_package` join table and `PackageSummary` model (see `modules/fundamental/src/package/model/summary.rs`).
2. Fetch all advisories for both SBOMs via the existing `sbom_advisory` join table and `AdvisorySummary` model (see `modules/fundamental/src/advisory/model/summary.rs`).
3. Compute diff categories:
   - **Added packages**: packages in the right SBOM not in the left (by package name)
   - **Removed packages**: packages in the left SBOM not in the right (by package name)
   - **Version changes**: packages in both SBOMs with different versions; determine direction (upgrade/downgrade) using semver comparison
   - **New vulnerabilities**: advisories affecting the right SBOM not affecting the left
   - **Resolved vulnerabilities**: advisories affecting the left SBOM not affecting the right
   - **License changes**: packages in both SBOMs with different license values (from `package_license` entity)
4. Return `SbomComparisonResult` containing all diff categories.

**Performance requirement (NFR):** p95 < 1s for SBOMs with up to 2000 packages each. Use efficient set operations (HashSet/HashMap lookups) for diff computation rather than nested iteration.

Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ structure for the comparison feature. See `modules/fundamental/src/sbom/` for the established module layout.
Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` with `.context()` wrapping for all service methods. See `modules/fundamental/src/sbom/service/sbom.rs` for existing error handling patterns.
Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's `.rs` module scope.

**Backend API contracts (response shape):**
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
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- existing service with fetch and list methods; extend or compose for comparison logic
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- existing package model with name, version, and license fields; use for diff input
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- existing advisory model with severity field; use for vulnerability diff
- `entity/src/sbom_package.rs` -- SBOM-Package join table entity for querying packages per SBOM
- `entity/src/sbom_advisory.rs` -- SBOM-Advisory join table entity for querying advisories per SBOM
- `entity/src/package_license.rs` -- Package-License mapping entity for license diff
- `common/src/error.rs::AppError` -- error type for Result returns

## Acceptance Criteria
- [ ] SbomComparisonResult struct and all sub-structs are defined with serde Serialize/Deserialize derives
- [ ] Comparison service correctly identifies added, removed, and version-changed packages
- [ ] Comparison service correctly identifies new and resolved vulnerabilities
- [ ] Comparison service correctly identifies license changes
- [ ] Diff computation uses efficient set operations (no O(n^2) nested loops)
- [ ] No new database tables or migrations are introduced

## Test Requirements
- [ ] Unit tests for diff computation logic with known input sets
- [ ] Test that added packages are correctly identified (present in right, absent in left)
- [ ] Test that removed packages are correctly identified (present in left, absent in right)
- [ ] Test that version changes detect upgrade vs downgrade direction
- [ ] Test that new and resolved vulnerabilities are correctly classified
- [ ] Test that license changes are detected when package exists in both SBOMs with different licenses
- [ ] Test with empty SBOMs (both empty, one empty, no differences)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
