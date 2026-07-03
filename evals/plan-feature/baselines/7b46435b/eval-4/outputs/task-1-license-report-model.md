# Task 1 — Add license report model and policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Add the model structs and policy configuration needed for the license compliance report feature. This includes the response types (`LicenseReportGroup`, `LicenseReport`) that represent grouped license data with compliance flags, and a configurable license policy system that determines which licenses are non-compliant. The policy is stored as a JSON configuration file in the repository and loaded at service startup.

This is the foundational layer for TC-9004 — subsequent tasks build the service logic and endpoint on top of these types.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — license report response structs: `LicenseReportGroup` (license name, package list, compliant flag) and `LicenseReport` (list of groups)
- `config/license-policy.json` — default license policy configuration listing non-compliant license identifiers (e.g., GPL-3.0-only, AGPL-3.0-only) and configurable policy rules

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod license_report;` and re-export types
- `modules/fundamental/Cargo.toml` — add `serde_json` dependency if not already present for policy deserialization

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/`: see `summary.rs` (SbomSummary) and `details.rs` (SbomDetails) for struct definition conventions including Serde derive macros, field naming, and documentation comments.
- The `LicenseReportGroup` struct should contain: `license: String` (SPDX identifier), `packages: Vec<PackageLicenseEntry>`, `compliant: bool`. Create a `PackageLicenseEntry` struct with package identifiers (name, version, purl).
- The `LicenseReport` struct should contain: `groups: Vec<LicenseReportGroup>`.
- The `LicensePolicy` struct should deserialize from the JSON config: a list of non-compliant SPDX license identifiers and optional policy metadata.
- Use `#[derive(Clone, Debug, Serialize, Deserialize)]` consistent with existing model types.
- The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` already includes a `license` field — the report model should reference compatible types.
- Per CONVENTIONS.md: follow the module pattern where each domain concept has its own file within `model/`. Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's model directory scope.
- Per docs/constraints.md section 2: commits must follow Conventional Commits format and reference TC-9004.
- Per docs/constraints.md section 5: do not duplicate existing model patterns — reuse Serde derives and naming conventions from sibling model files.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains the `license` field; reference its type for license data representation
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — follow the same struct pattern (derives, field documentation, module registration)
- `entity/src/package_license.rs` — Package-License mapping entity; understand the data schema for license association

## Acceptance Criteria
- [ ] `LicenseReportGroup` struct exists with `license`, `packages`, and `compliant` fields
- [ ] `LicenseReport` struct exists with a `groups` field containing `Vec<LicenseReportGroup>`
- [ ] `LicensePolicy` struct can deserialize from a JSON configuration file
- [ ] Default `config/license-policy.json` file exists with a sample set of non-compliant license identifiers
- [ ] All types are re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] All types implement `Serialize` and `Deserialize`

## Test Requirements
- [ ] Unit test verifying `LicensePolicy` deserialization from a JSON string
- [ ] Unit test verifying `LicenseReport` serialization produces the expected JSON structure: `{ "groups": [{ "license": "MIT", "packages": [...], "compliant": true }] }`
- [ ] Unit test verifying `LicensePolicy` correctly identifies a license as non-compliant

## Dependencies
- None (this is the first task in the implementation chain)
