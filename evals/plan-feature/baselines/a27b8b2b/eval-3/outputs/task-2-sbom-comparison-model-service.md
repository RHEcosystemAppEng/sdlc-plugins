# Task 2: Add SBOM comparison model and diff service

**Summary**: Add SBOM comparison model structs and diff service logic

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the data model structs for SBOM comparison results and implement the diff computation logic in SbomService. The comparison service method computes an on-the-fly diff between two SBOMs by querying existing package, advisory, and license data — no new database tables are required. The diff identifies added/removed packages, version changes, new/resolved vulnerabilities, and license changes between two SBOM versions.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison result structs: `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new comparison module
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `compare` method to `SbomService` that takes two SBOM IDs and returns `SbomComparisonResult`

## API Changes
- Internal service API only — no HTTP endpoint in this task. The `SbomService::compare(left_id, right_id)` method returns `Result<SbomComparisonResult, AppError>`.

## Implementation Notes
- Follow the existing module pattern: model structs in `model/`, service logic in `service/`. Reference `modules/fundamental/src/sbom/model/summary.rs` for struct conventions (derive Serialize, Deserialize, Clone, Debug).
- The comparison method should:
  1. Fetch package lists for both SBOMs using the `sbom_package` join table (`entity/src/sbom_package.rs`)
  2. Compute set differences for added/removed packages
  3. Compare versions for packages present in both SBOMs
  4. Fetch advisories for both SBOMs using the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) and compute new/resolved vulnerabilities
  5. Compare licenses for packages present in both using `package_license` entity (`entity/src/package_license.rs`)
- Use `AppError` from `common/src/error.rs` with `.context()` wrapping for error handling, consistent with existing service methods in `modules/fundamental/src/sbom/service/sbom.rs`.
- The `direction` field in `VersionChange` should be computed by comparing semver strings (upgrade vs downgrade). Consider using the `semver` crate if available in `Cargo.toml`, or string comparison as fallback.
- Performance constraint: p95 < 1s for SBOMs with up to 2000 packages each. Use efficient set operations (HashSet/HashMap-based lookups) rather than nested iteration.
- The response shape must match the contract specified in the feature description:
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

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list/ingest methods; add the compare method here
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — use to fetch advisory details (severity, title) for vulnerability diff entries
- `modules/fundamental/src/package/service/mod.rs::PackageService` — use to fetch package details (license) for package diff entries
- `common/src/db/query.rs` — shared query builder helpers for filtering
- `common/src/error.rs::AppError` — standard error type for Result returns
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for querying advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for license comparison

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct and all sub-structs are defined with Serialize/Deserialize derives
- [ ] `SbomService::compare(left_id, right_id)` method correctly computes added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes
- [ ] The method returns an error with appropriate context when either SBOM ID does not exist
- [ ] Performance: the comparison completes within 1 second for SBOMs with 2000 packages each (validated by test or benchmark)

## Test Requirements
- [ ] Unit test: compare two SBOMs where left has packages A, B, C and right has B, C, D — verify A is removed, D is added, B and C appear in version changes only if versions differ
- [ ] Unit test: compare two SBOMs with different advisory sets — verify new and resolved vulnerabilities are correctly identified
- [ ] Unit test: compare two SBOMs with license changes — verify license diff entries are generated
- [ ] Unit test: passing a nonexistent SBOM ID returns AppError with appropriate message
- [ ] Unit test: comparing an SBOM with itself returns empty diff lists

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
