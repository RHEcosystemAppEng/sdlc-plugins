## Repository
trustify-backend

## Target Branch
main

## Description
Add license policy configuration and license report response models for the license compliance report feature (TC-9004). This task establishes the data foundations: a configurable license policy that defines which licenses are compliant, and the response model structs that the report endpoint will return. The license policy is stored as a JSON config file in the repository, loaded at startup by a dedicated module. The report models define the grouped-by-license response shape with compliance flags.

## Files to Create
- `config/license-policy.json` -- default license compliance policy defining allowed and denied license identifiers (e.g., MIT, Apache-2.0, GPL-3.0)
- `common/src/license_policy.rs` -- LicensePolicy struct with fields for allowed_licenses, denied_licenses, and a `load_from_file()` constructor; includes a `check_compliance(license: &str) -> bool` method
- `modules/fundamental/src/sbom/model/license_report.rs` -- LicenseGroup struct (license name, list of packages, compliant flag) and LicenseReport struct (list of LicenseGroup entries) with Serialize derives

## Files to Modify
- `common/src/lib.rs` -- add `pub mod license_policy;` to export the new module
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod license_report;` to export the new model module

## Implementation Notes
- The LicensePolicy struct should deserialize from JSON using serde. The config file path can be provided via an environment variable or a default path (`config/license-policy.json`).
- The LicenseReport struct should follow the response shape specified in the feature: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`. Map this to Rust structs with `#[derive(Serialize, Deserialize)]`.
- Per CONVENTIONS.md $Module Pattern: follow the established model/ + service/ + endpoints/ structure when placing model files under `modules/fundamental/src/sbom/model/`.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's Rust module file scope.
  See `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) for the established model struct pattern.
- Per CONVENTIONS.md $Response Types: follow the existing response type patterns for struct design and serialization derives.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's Rust model file scope.
  See `common/src/model/paginated.rs` (PaginatedResults<T>) for the established response wrapper pattern.
- Performance constraint: the model must support efficient serialization for SBOMs with up to 1000 packages (p95 < 500ms).

## Reuse Candidates
- `entity/src/package_license.rs` -- existing Package-License mapping entity; use as the data source for license information per package
- `common/src/model/paginated.rs::PaginatedResults<T>` -- established response wrapper pattern; follow its Serialize derive and struct layout conventions
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- existing model struct demonstrating the naming and derive conventions

## Acceptance Criteria
- [ ] `config/license-policy.json` exists with a default policy containing sample allowed licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) and denied licenses (GPL-3.0, AGPL-3.0)
- [ ] `LicensePolicy::load_from_file()` successfully loads and parses the JSON config
- [ ] `LicensePolicy::check_compliance()` returns true for allowed licenses and false for denied licenses
- [ ] `LicenseGroup` struct contains license name (String), packages (Vec), and compliant (bool) fields
- [ ] `LicenseReport` struct contains groups (Vec<LicenseGroup>) field
- [ ] All structs derive Serialize for JSON response serialization

## Test Requirements
- [ ] Unit test: LicensePolicy loads from a valid JSON file and returns correct compliance checks
- [ ] Unit test: LicensePolicy returns an error for a malformed or missing config file
- [ ] Unit test: LicenseReport serializes to the expected JSON shape matching the API contract

## Verification Commands
- `cargo build -p common` -- builds without errors
- `cargo build -p trustify-module-fundamental` -- builds without errors
- `cargo test -p common -- license_policy` -- all unit tests pass

## Dependencies
- None (first task in the chain)
