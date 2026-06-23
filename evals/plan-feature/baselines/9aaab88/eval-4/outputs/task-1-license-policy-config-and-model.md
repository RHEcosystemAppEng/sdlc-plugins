## Repository
trustify-backend

## Target Branch
main

## Description
Add the license policy configuration file and define the Rust model types for the license compliance report. The policy file defines which licenses are allowed, denied, or flagged for review. The model types represent the structured report response with packages grouped by license and compliance status flags.

## Files to Create
- `license-policy.json` — Default license policy configuration defining allowed and denied license identifiers (e.g., MIT, Apache-2.0 as allowed; GPL-3.0 as denied)
- `modules/fundamental/src/sbom/model/license_report.rs` — Rust structs: `LicenseReport`, `LicenseGroup` (license name, list of packages, compliant flag), `LicensePolicyConfig` (deserialization target for the JSON policy file)

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new model module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct layout and derive macros.
- The `LicenseReport` struct should contain a `groups` field of type `Vec<LicenseGroup>`.
- `LicenseGroup` should include: `license: String`, `packages: Vec<PackageLicenseEntry>`, `compliant: bool`.
- `PackageLicenseEntry` should be a lightweight struct with package name, version, and purl.
- `LicensePolicyConfig` should use `serde::Deserialize` with fields for `allowed: Vec<String>`, `denied: Vec<String>`, and optionally `review: Vec<String>`.
- Reference the existing `PackageSummary` struct in `modules/fundamental/src/sbom/model/../../../package/model/summary.rs` which already includes a `license` field — reuse this field's type/format for consistency.
- Per CONVENTIONS.md §Module pattern: follow model/ + service/ + endpoints/ structure for the new license report domain code. Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the convention's `.rs` module scope.
- Per CONVENTIONS.md §Error handling: derive or implement error conversions compatible with `AppError` from `common/src/error.rs`. Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's `.rs` file scope.

## Acceptance Criteria
- [ ] `license-policy.json` exists at the repository root with a valid schema containing allowed and denied license lists
- [ ] `LicenseReport`, `LicenseGroup`, and `LicensePolicyConfig` structs are defined with appropriate serde derives
- [ ] Model module compiles and is exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Policy config can be deserialized from the JSON file in a unit test

## Test Requirements
- [ ] Unit test that deserializes `license-policy.json` into `LicensePolicyConfig` and verifies allowed/denied lists
- [ ] Unit test that serializes a `LicenseReport` to JSON and verifies the expected structure matches `{ groups: [{ license, packages, compliant }] }`

[sdlc-workflow] Description digest: sha256-md:1ae04cb7ee3449289eaf27f92e0bbac896c4ce5870339afb81553122540aa12c
