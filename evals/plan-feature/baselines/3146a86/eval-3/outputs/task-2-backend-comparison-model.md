# Task 2 — Add SBOM comparison model structs

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the Rust data model structs for the SBOM comparison response. These structs will be serialized as JSON and returned by the new comparison endpoint. The response must represent six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add module declaration for the new comparison model

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — define `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` structs

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW: returns `SbomComparisonResult` (this task defines the model; the endpoint is wired in Task 4)

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each struct derives `Serialize`, `Deserialize`, `Debug`, `Clone` at minimum.
- Per the backend key conventions: the module pattern is `model/ + service/ + endpoints/`. This task covers the `model/` portion.
- Use `serde` for serialization. Field names must use `snake_case` to match the API response shape specified in the Figma design context (e.g., `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`).
- The `direction` field on `VersionChange` should be a string enum with values `"upgrade"` and `"downgrade"`.
- The `severity` field on `NewVulnerability` and `ResolvedVulnerability` should match the severity representation used in `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs`).
- Per constraints doc section 5: code must not duplicate existing functionality. Reuse the severity representation from the advisory model rather than creating a new one.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — follow its derive macros, field naming, and serde patterns
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — follow the struct layout pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reuse the severity field type/representation
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reference for the license field representation

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
- [ ] All sub-structs (`AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) are defined with correct fields matching the API response shape
- [ ] All structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`
- [ ] The module is properly exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit tests verifying serialization of `SbomComparisonResult` to JSON matches the expected response shape
- [ ] Unit test verifying that an empty comparison (no changes) serializes to empty arrays for all fields

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
