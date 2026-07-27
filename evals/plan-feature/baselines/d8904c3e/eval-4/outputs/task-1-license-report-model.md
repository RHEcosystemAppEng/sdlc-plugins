## Repository
trustify-backend

## Target Branch
main

## Description
Add model types for the license compliance report feature. This includes the
response structs for the license report endpoint (`LicenseGroup`, `LicenseReport`)
and the license policy configuration struct (`LicensePolicy`, `PolicyRule`) used
to define which licenses are compliant or non-compliant.

The license policy is stored as a JSON configuration file in the repository and
loaded at startup or on-demand. The policy struct defines a list of allowed and
denied license identifiers (SPDX IDs), with a default-allow or default-deny mode.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` -- Defines `LicenseGroup` (license name, list of packages, compliant flag), `LicenseReport` (list of `LicenseGroup`s), `LicensePolicy` (allowed/denied lists, default mode), and `PolicyRule` (individual license rule)

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod license_report;` to expose the new module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs`
  and `modules/fundamental/src/sbom/model/details.rs` -- each model file defines a
  struct with `#[derive(Serialize, Deserialize, Debug, Clone)]` and any necessary
  trait implementations.
- Per CONVENTIONS.md Section "Module pattern": place model types under
  `modules/fundamental/src/sbom/model/` following the `model/ + service/ + endpoints/`
  structure.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching
  the convention's module structure scope.
- Per CONVENTIONS.md Section "Error handling": implement `From<serde_json::Error>` for
  `AppError` if not already present, to handle policy file parsing errors.
  Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the
  convention's `.rs` module file scope.
- The `LicenseReport` response shape must match the API contract:
  `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- The `LicensePolicy` struct should support serde deserialization from a JSON file
  with fields: `allowed_licenses: Vec<String>`, `denied_licenses: Vec<String>`,
  `default_mode: PolicyMode` (enum: `Allow`, `Deny`).
- Use SPDX license identifiers as the standard for license names.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- demonstrates the
  established struct pattern with serde derives used in this module
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- contains the
  `license` field that the report will reference; understand its type for compatibility
- `common/src/error.rs::AppError` -- the error enum all service/handler results use;
  may need a variant for policy loading errors

## Acceptance Criteria
- [ ] `LicenseGroup` struct defined with fields: `license` (String), `packages` (Vec of package references), `compliant` (bool)
- [ ] `LicenseReport` struct defined with field: `groups` (Vec of `LicenseGroup`)
- [ ] `LicensePolicy` struct defined with fields for allowed/denied license lists and default mode
- [ ] All structs derive `Serialize`, `Deserialize`, `Debug`, `Clone`
- [ ] Module is publicly exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Policy struct can be deserialized from a JSON file

## Test Requirements
- [ ] Unit test: `LicensePolicy` deserializes correctly from a valid JSON string with allowed and denied license lists
- [ ] Unit test: `LicensePolicy` deserialization fails gracefully with a clear error for malformed JSON
- [ ] Unit test: `LicenseReport` serializes to the expected JSON shape matching the API contract

## Verification Commands
- `cargo check -p trustify-module-fundamental` -- compiles without errors
- `cargo test -p trustify-module-fundamental -- license_report` -- all unit tests pass

## Dependencies
- No dependencies on other tasks
