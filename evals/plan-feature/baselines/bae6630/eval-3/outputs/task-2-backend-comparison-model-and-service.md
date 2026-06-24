# Task 2 — Backend comparison model and diff service

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the SBOM comparison data model and implement the diff computation service. The service loads two SBOMs by ID, retrieves their associated packages (with license info) and advisories, then computes the structured diff: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new comparison model module
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to expose the new comparison service module
- `modules/fundamental/src/sbom/mod.rs` — Re-export comparison types for downstream usage

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Define structs: `SbomComparison` (top-level diff result), `AddedPackage` (name, version, license, advisory_count), `RemovedPackage` (same fields), `VersionChange` (name, left_version, right_version, direction), `NewVulnerability` (advisory_id, severity, title, affected_package), `ResolvedVulnerability` (advisory_id, severity, title, previously_affected_package), `LicenseChange` (name, left_license, right_license). All structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`.
- `modules/fundamental/src/sbom/service/compare.rs` — Implement `SbomService::compare(left_id, right_id)` method. Use `PackageService` to fetch packages for each SBOM. Use `AdvisoryService` to fetch advisories for each SBOM. Compute set differences for added/removed packages, detect version changes via package name matching, compute advisory diffs, and detect license changes. Return `Result<SbomComparison, AppError>`.

## Implementation Notes
- Follow the existing module pattern in `modules/fundamental/src/sbom/`: model structs in `model/`, service logic in `service/`.
- Use `SbomService::fetch()` from `modules/fundamental/src/sbom/service/sbom.rs` to load each SBOM by ID.
- Use `PackageService` from `modules/fundamental/src/package/service/mod.rs` to retrieve packages for each SBOM.
- Use `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs` to retrieve advisories linked to each SBOM.
- The `direction` field in `VersionChange` should be "upgrade" or "downgrade" based on semver comparison.
- All errors should be wrapped with `.context()` as per the project convention in `common/src/error.rs`.
- No new database tables are needed; the diff is computed on-the-fly from existing entity data.

## Acceptance Criteria
- [ ] `SbomComparison` struct and all sub-structs are defined with Serialize/Deserialize derives
- [ ] `SbomService::compare()` correctly computes added packages (in right but not left)
- [ ] `SbomService::compare()` correctly computes removed packages (in left but not right)
- [ ] `SbomService::compare()` correctly detects version changes for same-name packages
- [ ] `SbomService::compare()` correctly computes new and resolved vulnerabilities
- [ ] `SbomService::compare()` correctly detects license changes
- [ ] All errors use `.context()` wrapping and return `AppError`

## Test Requirements
- [ ] Unit test: comparing two identical SBOMs returns empty diff in all categories
- [ ] Unit test: comparing SBOMs with non-overlapping packages produces correct added/removed lists
- [ ] Unit test: version change detection correctly identifies upgrade vs downgrade
- [ ] Unit test: license change detection finds packages with differing licenses

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003

## Digest
[sdlc-workflow] Description digest: sha256-md:cc672c04f8a2fbb59dae91e4487c526b73ce3b75b8d41da8f89eaea25a174332
