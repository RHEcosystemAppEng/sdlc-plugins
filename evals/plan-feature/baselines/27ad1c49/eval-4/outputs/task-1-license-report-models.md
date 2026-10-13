## Repository
trustify-backend

## Target Branch
main

## Description
Add the model types and policy configuration needed for the license compliance report feature. This includes the response structs for the license report endpoint (LicenseGroup and LicenseComplianceReport) and a LicensePolicy type that loads compliance rules from a JSON configuration file.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod license_report;` to expose the new model module
- `common/src/model/mod.rs` — add `pub mod license_policy;` to expose the policy configuration module
- `modules/fundamental/Cargo.toml` — add `serde_json` dependency if not already present for policy deserialization

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — define LicenseGroup struct (license name, list of packages, compliant flag) and LicenseComplianceReport struct (list of LicenseGroup items)
- `common/src/model/license_policy.rs` — define LicensePolicy struct that holds allowed and denied license lists, with a method to load from a JSON config file path

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: response type `LicenseComplianceReport { groups: Vec<LicenseGroup> }` where `LicenseGroup { license: String, packages: Vec<PackageLicenseInfo>, compliant: bool }`

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` for struct layout and serde derives.
- The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` already has a `license` field — reference its type for consistency.
- Derive `Serialize`, `Deserialize`, `Debug`, and `Clone` on all new structs.
- The LicensePolicy struct should support loading from a JSON file with `allowed_licenses` and `denied_licenses` string arrays. A license is compliant if it is not in the denied list (or if an allowed list is specified, it must be in the allowed list).

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains the `license` field type to reuse for consistency in the report structs
- `common/src/model/paginated.rs::PaginatedResults` — reference as an example of response wrapper patterns, though the report uses a non-paginated response

## Acceptance Criteria
- [ ] LicenseGroup struct has fields: license (String), packages (Vec), compliant (bool)
- [ ] LicenseComplianceReport struct has field: groups (Vec<LicenseGroup>)
- [ ] Both structs derive Serialize and Deserialize
- [ ] LicensePolicy can load allowed/denied license lists from a JSON file
- [ ] Module declarations added to both mod.rs files
- [ ] Code compiles with `cargo check`

## Verification Commands
- `cargo check -p trustify-common` — compiles without errors
- `cargo check -p trustify-fundamental` — compiles without errors

## Dependencies
- None — this is the first task in the chain
