# Task 1 — Add license report model types and policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Add the data model types for the license compliance report and the license policy configuration system. This task establishes the foundational types that the license report service (Task 2) and endpoint (Task 3) will build upon.

The license report model defines the response structure: packages grouped by license type, each group annotated with a compliance flag. The license policy model defines the rules for determining which licenses are compliant, loaded from a JSON configuration file in the repository.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` -- Model structs: `LicenseGroup` (license name, list of packages, compliant flag) and `LicenseReport` (list of groups, overall compliance status)
- `config/license-policy.json` -- Default license policy configuration file defining allowed and denied license patterns

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod license_report;` to re-export the new model types
- `modules/fundamental/Cargo.toml` -- Add `serde_json` dependency if not already present (for policy config loading)

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails). Each model struct should derive `Serialize`, `Deserialize`, `Debug`, and `Clone`.
- The `LicenseGroup` struct should contain: `license: String`, `packages: Vec<PackageLicenseEntry>`, `compliant: bool`. Define `PackageLicenseEntry` as a lightweight struct with package name, version, and purl fields.
- The `LicenseReport` struct should contain: `groups: Vec<LicenseGroup>` and a computed `compliant: bool` field that is `true` only when all groups are compliant.
- The license policy configuration should define allowed and/or denied license identifiers using SPDX license IDs (e.g., "MIT", "Apache-2.0", "GPL-3.0-only"). Use a deny-list model: any license matching a denied pattern is non-compliant; all others are compliant by default.
- Per the Key Conventions: all structs should follow the module pattern (`model/` directory) and derive appropriate serde traits for JSON serialization.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's model directory scope.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- Contains the `license` field; use this as a reference for how license data is currently modeled per-package
- `entity/src/package_license.rs` -- Existing Package-License mapping entity in SeaORM; this is the database representation that the report will aggregate from
- `common/src/error.rs::AppError` -- Error handling enum; use for policy loading errors

## Acceptance Criteria
- [ ] `LicenseGroup` struct defined with license name, packages list, and compliant flag
- [ ] `LicenseReport` struct defined with groups list and overall compliance status
- [ ] License policy model struct defined with configurable allowed/denied license rules
- [ ] Default `config/license-policy.json` file created with a reasonable set of common open-source license rules
- [ ] Policy configuration can be deserialized from JSON using serde
- [ ] New model types are re-exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test: `LicensePolicy` correctly loads from a valid JSON config file
- [ ] Unit test: `LicensePolicy` returns an error for malformed JSON
- [ ] Unit test: `LicenseReport` computes overall `compliant` field correctly (true when all groups compliant, false when any group non-compliant)
- [ ] Unit test: `LicenseGroup` serializes to expected JSON shape (`{ "license": "MIT", "packages": [...], "compliant": true }`)

## Dependencies
- None (this is the first task)
