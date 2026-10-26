# Task 1 — Add license report model types and policy configuration

## Repository
trustify-backend

## Target Branch
main

## Description
Define the data model types for the license compliance report and the license policy configuration schema. The license report groups all packages in an SBOM by their license type and flags each group as compliant or non-compliant based on a configurable policy. The policy is stored as a JSON configuration file in the repository, listing denied and allowed license identifiers (SPDX format).

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new `license_report` module

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — define `LicenseReport`, `LicenseReportGroup`, and `LicensePolicy` structs with serde Serialize/Deserialize
- `config/license-policy.json` — default license policy configuration file with example denied/allowed license lists

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: response shape `LicenseReport { groups: Vec<LicenseReportGroup> }` where `LicenseReportGroup { license: String, packages: Vec<PackageLicenseInfo>, compliant: bool }`

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `details.rs` for struct layout and derive macros (`Serialize`, `Deserialize`, `Debug`, `Clone`).
- `LicenseReport` should contain a `groups` field of type `Vec<LicenseReportGroup>`.
- `LicenseReportGroup` should contain: `license: String` (SPDX identifier), `packages: Vec<PackageLicenseInfo>` (package name, version, purl), `compliant: bool`.
- `PackageLicenseInfo` is a lightweight struct with the package identifiers needed for the report (name, version, purl).
- `LicensePolicy` should define: `denied_licenses: Vec<String>` (SPDX IDs that are non-compliant), `allowed_licenses: Option<Vec<String>>` (if present, only these are compliant — allowlist mode).
- The policy loader should read from a configurable file path, defaulting to `config/license-policy.json`.
- The `package_license.rs` entity (`entity/src/package_license.rs`) already maps packages to licenses — the service (Task 2) will query this.
- Per CONVENTIONS.md §Module Pattern: follow the `model/ + service/ + endpoints/` structure within the SBOM domain module.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's model directory scope.
- Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for the policy file loader.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing model struct demonstrating the derive macro pattern and serde configuration
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains the `license` field that the report will reference
- `entity/src/package_license.rs` — SeaORM entity for the package-license mapping; the service will query this relation
- `common/src/error.rs::AppError` — error type for the policy loader

## Acceptance Criteria
- [ ] `LicenseReport`, `LicenseReportGroup`, `PackageLicenseInfo`, and `LicensePolicy` structs are defined with appropriate serde derives
- [ ] `LicensePolicy` can be deserialized from a JSON file with `denied_licenses` and optional `allowed_licenses` fields
- [ ] A default `config/license-policy.json` file exists with a documented example policy
- [ ] The `license_report` module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] All structs implement `Serialize` and `Deserialize` for API response serialization

## Test Requirements
- [ ] Unit test: `LicensePolicy` deserializes correctly from valid JSON with denied licenses list
- [ ] Unit test: `LicensePolicy` deserializes correctly with both denied and allowed license lists
- [ ] Unit test: `LicensePolicy` deserialization fails gracefully on invalid JSON
- [ ] Unit test: `LicenseReport` serializes to expected JSON shape matching the API contract

## Verification Commands
- `cargo build -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental -- license` — model unit tests pass

## Dependencies
- None (this is the first task)
