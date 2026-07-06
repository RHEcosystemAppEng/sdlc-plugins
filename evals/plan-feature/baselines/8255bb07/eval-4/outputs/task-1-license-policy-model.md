## Repository
trustify-backend

## Target Branch
main

## Description
Add the license policy configuration model and license compliance report response model to support the license compliance report feature (TC-9004). The license policy defines which licenses are allowed, denied, or flagged for review, and is stored as a JSON configuration file in the repository. The report model defines the response structure for the license report endpoint: packages grouped by license type with compliance flags.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod license_report;` to export the new license report model
- `common/src/model/mod.rs` -- add `pub mod license_policy;` to export the new license policy model

## Files to Create
- `common/src/model/license_policy.rs` -- LicensePolicy struct with `allowed_licenses: Vec<String>`, `denied_licenses: Vec<String>` fields; implement `Default` trait and a `fn load_from_file(path: &Path) -> Result<Self, AppError>` method using serde_json deserialization
- `modules/fundamental/src/sbom/model/license_report.rs` -- LicenseReport struct containing `groups: Vec<LicenseGroup>`; LicenseGroup struct with `license: String`, `packages: Vec<PackageLicenseEntry>`, `compliant: bool` fields; PackageLicenseEntry struct with `name: String`, `version: String`, `purl: Option<String>` fields; all derive Serialize, Deserialize, Clone, Debug, utoipa::ToSchema
- `license-policy.json` -- default license policy configuration file at repo root with common permissive licenses (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause) as allowed and known copyleft licenses (GPL-2.0, GPL-3.0, AGPL-3.0) as denied

## Implementation Notes
- Per Key Conventions "Module pattern": follow the established `model/ + service/ + endpoints/` structure. Place the report model under `modules/fundamental/src/sbom/model/` alongside existing `summary.rs` and `details.rs`.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's module model file scope.
- Per Key Conventions "Framework": use SeaORM-compatible types for any fields that map to database columns, and serde for JSON serialization.
  Applies: task creates `common/src/model/license_policy.rs` matching the convention's Rust source file scope.
- Use `AppError` from `common/src/error.rs` for error returns in `load_from_file`, wrapping IO and JSON parse errors with `.context()` per the Error handling convention.
  Applies: task creates `common/src/model/license_policy.rs` matching the convention's Rust source file scope.
- The license policy file path should be configurable (e.g., via environment variable or application config), with a default fallback to `license-policy.json` at the repo root.

## Reuse Candidates
- `common/src/error.rs::AppError` -- application error enum implementing IntoResponse; use for error handling in policy loading
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- existing package model that includes a license field; reference its field structure when defining PackageLicenseEntry
- `common/src/model/mod.rs` -- existing model module root; follow the same export pattern for the new license_policy module

## Acceptance Criteria
- [ ] LicensePolicy struct deserializes a JSON file with allowed_licenses and denied_licenses arrays
- [ ] LicensePolicy::load_from_file returns Result<LicensePolicy, AppError> with descriptive error context for missing or malformed files
- [ ] LicenseReport, LicenseGroup, and PackageLicenseEntry structs are serializable to JSON matching the response shape: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- [ ] Default license-policy.json is present at the repo root with a reasonable set of permissive (allowed) and copyleft (denied) licenses
- [ ] All new structs derive utoipa::ToSchema for OpenAPI documentation generation

## Test Requirements
- [ ] Unit test: LicensePolicy deserializes a valid JSON policy file correctly
- [ ] Unit test: LicensePolicy returns an error with context for a missing file
- [ ] Unit test: LicensePolicy returns an error with context for malformed JSON
- [ ] Unit test: LicenseReport serializes to the expected JSON shape with groups, packages, and compliant flags

## Dependencies
- None (first task in the sequence)
