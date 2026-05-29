## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the data model structs and service logic for SBOM comparison. This introduces the diff computation that compares two SBOMs by their packages, advisories, and licenses, producing a structured result with added/removed packages, version changes, new/resolved vulnerabilities, and license changes.

## Files to Modify
- `modules/fundamental/src/sbom/mod.rs` — add `comparison` submodule declaration
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare` method to `SbomService`

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — define `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange` structs
- `modules/fundamental/src/sbom/service/comparison.rs` — implement diff logic: load packages for both SBOMs, compute set differences, correlate advisories, detect license changes

## API Changes
- No endpoint changes in this task (endpoint added in Task 4)

## Implementation Notes
- Follow the existing module pattern in `modules/fundamental/src/sbom/`: model structs in `model/`, service logic in `service/`.
- The `SbomComparisonResult` struct should be serializable with `serde::Serialize` and contain fields: `added_packages: Vec<PackageDiff>`, `removed_packages: Vec<PackageDiff>`, `version_changes: Vec<VersionChange>`, `new_vulnerabilities: Vec<VulnerabilityDiff>`, `resolved_vulnerabilities: Vec<VulnerabilityDiff>`, `license_changes: Vec<LicenseChange>`.
- Reuse `PackageSummary` from `modules/fundamental/src/sbom/model/summary.rs` as a reference for package fields (name, version, license).
- Reuse `AdvisorySummary` from `modules/fundamental/src/advisory/model/summary.rs` for advisory fields (advisory_id, severity, title).
- The compare method in `SbomService` should accept two SBOM IDs, load their package lists via the existing `PackageService` in `modules/fundamental/src/package/service/mod.rs`, and compute set differences by package name.
- For vulnerability diff: query advisories linked to packages in each SBOM using the `sbom_advisory` join entity in `entity/src/sbom_advisory.rs` and the `sbom_package` join entity in `entity/src/sbom_package.rs`.
- All service methods should return `Result<T, AppError>` using the error type from `common/src/error.rs` with `.context()` wrapping for error messages.
- The diff computation must be done in-memory (no new database tables per NFR). Load packages for both SBOMs, then compute differences using HashSet operations on package names.
- Target p95 < 1s for SBOMs with up to 2000 packages each — use efficient set operations rather than nested loops.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for serializable SBOM model struct patterns
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reuse field definitions for package name, version, license
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reuse field definitions for advisory_id, severity, title
- `common/src/error.rs::AppError` — standard error handling pattern for all service methods

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
- [ ] `SbomService::compare` method accepts two SBOM IDs and returns `Result<SbomComparisonResult, AppError>`
- [ ] Diff correctly identifies packages present in right but not left as "added"
- [ ] Diff correctly identifies packages present in left but not right as "removed"
- [ ] Diff correctly identifies packages with same name but different versions as "version_changes" with upgrade/downgrade direction
- [ ] Diff correctly identifies new and resolved vulnerabilities by comparing advisory associations
- [ ] Diff correctly identifies license changes for packages present in both SBOMs

## Test Requirements
- [ ] Unit test: comparing two SBOMs with known package differences returns correct added/removed counts
- [ ] Unit test: comparing identical SBOMs returns empty diff (all arrays empty)
- [ ] Unit test: version change detection correctly classifies upgrade vs downgrade direction
- [ ] Unit test: vulnerability diff correctly identifies new advisories on added packages
- [ ] Unit test: license change detection finds packages where license field differs

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main (trustify-backend)

[sdlc-workflow] Description digest: sha256:69f84139515be6d78eb8242b1b7d20bb9b3361e11db589a0ab36ab53cf6fc15a
