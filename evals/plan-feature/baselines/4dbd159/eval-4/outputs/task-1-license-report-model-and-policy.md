# Task 1 — Add license compliance report model and policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Define the data model structs for the license compliance report and implement a policy configuration loader. The report model represents packages grouped by license type with compliance flags. The policy loader reads a JSON configuration file that defines which licenses are allowed, denied, or flagged for review. This task provides the foundational types that the service layer (Task 2) and endpoint (Task 3) will consume.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export new license report model types
- `modules/fundamental/src/sbom/mod.rs` — add policy module declaration
- `modules/fundamental/Cargo.toml` — add serde_json dependency if not already present for policy file parsing

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — define `LicenseGroup` and `LicenseReport` structs
- `modules/fundamental/src/sbom/policy/mod.rs` — define `LicensePolicy` struct and `load_policy()` function to read and parse a JSON config file

## API Changes
- No HTTP API changes in this task (model-only)

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct organization, derive macros, and serialization attributes.
- The `LicenseReport` struct should contain a `groups` field of type `Vec<LicenseGroup>`.
- Each `LicenseGroup` should include: `license: String`, `packages: Vec<PackageLicenseEntry>`, `compliant: bool`.
- `PackageLicenseEntry` should include at minimum: package name, version, and pURL if available. Reference the `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` for the existing package model shape — specifically the `license` field.
- The `LicensePolicy` struct should define `allowed_licenses: Vec<String>` and `denied_licenses: Vec<String>` (or a single `policy_mode` enum with allowlist/denylist semantics).
- The policy JSON config file should be loaded from a configurable path (environment variable or server config). Use `serde_json::from_reader` for deserialization.
- All structs must derive `Serialize`, `Deserialize`, `Clone`, `Debug` consistent with existing model patterns.
- Per docs/constraints.md: commit messages must follow Conventional Commits format (constraint 2.2), include Jira issue reference in footer (constraint 2.1), and include `--trailer="Assisted-by: Claude Code"` (constraint 2.3).

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — demonstrates the model struct pattern with serde derives
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — demonstrates detailed model struct pattern
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains the `license` field that feeds into the compliance report
- `entity/src/package_license.rs` — the Package-License entity mapping, source of license data

## Acceptance Criteria
- [ ] `LicenseGroup` and `LicenseReport` structs are defined with proper serde derives and are publicly exported
- [ ] `PackageLicenseEntry` struct captures package identity and license information
- [ ] `LicensePolicy` struct with JSON deserialization is defined
- [ ] `load_policy()` function reads and parses a JSON policy config file from a configurable path
- [ ] Policy loading returns an appropriate error (using `AppError`) when the file is missing or malformed
- [ ] All new types are re-exported through the module hierarchy

## Test Requirements
- [ ] Unit test that `LicensePolicy` correctly deserializes from a valid JSON string
- [ ] Unit test that `load_policy()` returns an error for a missing config file
- [ ] Unit test that `load_policy()` returns an error for malformed JSON
- [ ] Unit test that `LicenseReport` serializes to the expected JSON shape (`{ groups: [{ license, packages, compliant }] }`)

## Dependencies
- None
