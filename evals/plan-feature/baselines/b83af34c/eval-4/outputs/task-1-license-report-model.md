## Repository
trustify-backend

## Target Branch
main

## Priority
Major

## Fix Versions
RHTPA 1.5.0

## Description
Create the license compliance report response model types and the license policy configuration types. The model defines the structure of the `GET /api/v2/sbom/{id}/license-report` response: packages grouped by license type with compliance flags. The policy types define the configurable license policy that determines which licenses are compliant.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — License report response types: `LicenseGroup` (license name, package list, compliant flag), `LicenseReport` (list of groups, overall compliance status), and `LicensePolicy` (allowed/denied license lists loaded from JSON config)

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` and re-export the new types

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/`. The `summary.rs` and `details.rs` files demonstrate the struct definition pattern with `serde::Serialize` and `utoipa::ToSchema` derives for OpenAPI schema generation.

The `LicenseReport` struct should contain a `Vec<LicenseGroup>` where each `LicenseGroup` has:
- `license: String` — the SPDX license identifier
- `packages: Vec<PackageLicenseEntry>` — packages using this license
- `compliant: bool` — whether this license passes the policy check

The `LicensePolicy` struct should be deserializable from a JSON config file with:
- `allowed_licenses: Option<Vec<String>>` — allowlist (if present, only these are compliant)
- `denied_licenses: Option<Vec<String>>` — denylist (if present, these are non-compliant)

Reference `entity/src/package_license.rs` for the existing package-license mapping entity and `entity/src/package.rs` for the package entity to understand the source data model.

Per CONVENTIONS.md §Module pattern: define model structs in the model/ subdirectory following the model/ + service/ + endpoints/ structure. Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the convention's Rust module scope.

Per CONVENTIONS.md §Error handling: derive `Serialize` and `ToSchema` on response types for consistent API responses. Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's `.rs` file scope.

## Acceptance Criteria
- [ ] `LicenseReport`, `LicenseGroup`, and `PackageLicenseEntry` structs are defined with `Serialize` and `ToSchema` derives
- [ ] `LicensePolicy` struct is defined with `Deserialize` derive and can be loaded from a JSON file
- [ ] All new types are re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Response structure matches `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Test Requirements
- [ ] Unit test that `LicensePolicy` deserializes from a JSON string with allowed and denied lists
- [ ] Unit test that `LicenseReport` serializes to the expected JSON structure
- [ ] Unit test that an empty policy (no allowed/denied lists) treats all licenses as compliant
