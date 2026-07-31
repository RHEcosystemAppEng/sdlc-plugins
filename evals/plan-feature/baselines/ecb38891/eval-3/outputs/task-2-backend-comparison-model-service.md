## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the SBOM comparison model types and service logic to compute a structured diff between two SBOMs. The comparison service loads two SBOMs by ID, collects their associated packages (with license info) and linked advisories (with severity), and produces a structured diff with six categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

This task provides the core domain logic that the comparison endpoint (Task 3) will expose via the REST API.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod comparison;` to register the new model module
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare` method to `SbomService` that takes two SBOM IDs and returns `SbomComparisonResult`

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — define `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` structs with serde serialization

## Implementation Notes
- Follow the existing module pattern (model/ + service/ + endpoints/) established by the sbom, advisory, and package modules.
- The `SbomComparisonResult` struct should mirror the response shape from the Figma design context:
  ```
  added_packages: Vec<AddedPackage>       — packages in right but not left
  removed_packages: Vec<RemovedPackage>   — packages in left but not right
  version_changes: Vec<VersionChange>     — packages in both with different versions
  new_vulnerabilities: Vec<NewVulnerability> — advisories affecting right but not left
  resolved_vulnerabilities: Vec<ResolvedVulnerability> — advisories affecting left but not right
  license_changes: Vec<LicenseChange>     — packages in both with different licenses
  ```
- The `compare` method in `SbomService` should:
  1. Fetch both SBOMs using the existing `SbomService::fetch` method (see `modules/fundamental/src/sbom/service/sbom.rs`)
  2. Load packages for each SBOM using `PackageService` (see `modules/fundamental/src/package/service/mod.rs`) via the `sbom_package` join table (see `entity/src/sbom_package.rs`)
  3. Load advisories for each SBOM using `AdvisoryService` (see `modules/fundamental/src/advisory/service/advisory.rs`) via the `sbom_advisory` join table (see `entity/src/sbom_advisory.rs`)
  4. Compute diff by comparing package sets (by name) and advisory sets (by ID)
  5. For version changes, determine direction (upgrade/downgrade) by comparing semver-parsed versions
- Use `Result<SbomComparisonResult, AppError>` return type with `.context()` wrapping for error handling, consistent with existing service methods (see `common/src/error.rs`)
- No new database tables — compute diff on-the-fly from existing `sbom_package`, `sbom_advisory`, `package`, `advisory`, and `package_license` entities
- Performance: the comparison must handle SBOMs with up to 2000 packages each within p95 < 1s. Use batch queries to load packages/advisories rather than N+1 queries. Use the query helpers from `common/src/db/query.rs` for efficient filtering.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list methods; extend with compare method
- `modules/fundamental/src/package/service/mod.rs::PackageService` — loads packages with license info; reuse for loading packages per SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — loads advisories with severity; reuse for loading advisories per SBOM
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct patterns with serde derive macros
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains license field, reference for package model shape
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains severity field, reference for advisory model shape
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for loading packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for loading advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for license lookups

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct and its sub-type structs are defined in `modules/fundamental/src/sbom/model/comparison.rs`
- [ ] All model structs derive `Serialize`, `Deserialize`, and `Debug`
- [ ] `SbomService::compare` method accepts two SBOM IDs and returns `Result<SbomComparisonResult, AppError>`
- [ ] Diff correctly identifies added packages (in right, not in left)
- [ ] Diff correctly identifies removed packages (in left, not in right)
- [ ] Diff correctly identifies version changes with upgrade/downgrade direction
- [ ] Diff correctly identifies new vulnerabilities (advisories affecting right but not left)
- [ ] Diff correctly identifies resolved vulnerabilities (advisories affecting left but not right)
- [ ] Diff correctly identifies license changes (same package, different license)
- [ ] Returns appropriate error when either SBOM ID is not found

## Test Requirements
- [ ] Unit test: comparison of two SBOMs with known package differences produces correct added/removed/changed lists
- [ ] Unit test: comparison of identical SBOMs produces empty diff in all categories
- [ ] Unit test: comparison with non-existent SBOM ID returns appropriate AppError
- [ ] Unit test: version change direction correctly classifies upgrades vs downgrades
- [ ] Unit test: advisory diff correctly identifies new and resolved vulnerabilities

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
