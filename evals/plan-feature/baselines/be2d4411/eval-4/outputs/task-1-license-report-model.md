## Repository
trustify-backend

## Target Branch
main

## Description
Add model types for the license compliance report response and a license policy configuration structure. The report response groups packages by license type and flags non-compliant licenses. The policy configuration is loaded from a JSON file that defines which licenses are allowed or denied.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — re-export the new license_report module

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseGroup and LicenseReport structs with serde Serialize derives
- `common/src/model/license_policy.rs` — LicensePolicy struct (allowed_licenses, denied_licenses vectors) with serde Deserialize and a `load_from_file` constructor

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW (model only): response shape `{ groups: [{ license: String, spdx_id: String, packages: [PackageSummary], compliant: bool }], summary: { total_packages: u32, compliant_count: u32, non_compliant_count: u32 } }`

## Implementation Notes
- Follow the existing module pattern (model/ + service/ + endpoints/) established in `modules/fundamental/src/sbom/model/`. Use `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs` as a reference for struct definition conventions (derive macros, serde attributes, field visibility).
- The `LicenseReport` struct should contain a `groups` field (Vec of `LicenseGroup`) and a `summary` field with aggregate counts.
- Each `LicenseGroup` contains `license` (display name), `spdx_id` (SPDX identifier), `packages` (Vec of `PackageSummary`), and `compliant` (bool).
- Reuse `PackageSummary` from `modules/fundamental/src/package/model/summary.rs` rather than defining a new package representation — the existing struct already includes a `license` field.
- The `LicensePolicy` struct in `common/src/model/license_policy.rs` should support loading from a JSON config file with `allowed_licenses` and `denied_licenses` lists. Include a `is_compliant(&self, license: &str) -> bool` method that checks against both lists (deny-list takes precedence over allow-list).
- Per docs/constraints.md section 5: error handling must use `Result<T, AppError>` with `.context()` wrapping for the policy file loader, following the pattern in `common/src/error.rs`.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing package summary struct with license field; reuse in LicenseGroup instead of creating a new package type
- `common/src/error.rs::AppError` — error enum for policy file loading errors
- `common/src/model/paginated.rs::PaginatedResults` — reference for response wrapper patterns (structure, not for direct reuse since the report is not paginated)

## Acceptance Criteria
- [ ] `LicenseReport` and `LicenseGroup` structs are defined with serde Serialize derives
- [ ] `LicensePolicy` struct is defined with serde Deserialize and `load_from_file` constructor
- [ ] `LicensePolicy::is_compliant` correctly checks against allowed and denied license lists
- [ ] `LicenseReport` re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] `LicensePolicy` re-exported from `common/src/model/mod.rs`
- [ ] All new types compile successfully with `cargo check`

## Test Requirements
- [ ] Unit test for `LicensePolicy::is_compliant` with allowed license returns true
- [ ] Unit test for `LicensePolicy::is_compliant` with denied license returns false
- [ ] Unit test for `LicensePolicy::is_compliant` deny-list precedence over allow-list
- [ ] Unit test for `LicensePolicy::load_from_file` with valid JSON config
- [ ] Unit test for `LicensePolicy::load_from_file` with missing file returns appropriate error

## Verification Commands
- `cargo check -p common` — compiles without errors
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p common -- license_policy` — all policy unit tests pass

## Dependencies
- None

[sdlc-workflow] Description digest: sha256-md:9c4f77396735c5299c97a7bcd4645ef41ecbd69b25a635eaeb666a1ae6149087
