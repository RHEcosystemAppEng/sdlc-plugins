## Repository
trustify-backend

## Target Branch
main

## Description
Add the license compliance report model structs and license policy configuration for the SBOM license report feature (TC-9004). This task creates the data structures that represent the license report response (groups of packages by license, with compliance flags) and a configurable license policy that defines which licenses are compliant or non-compliant. The policy is loaded from a JSON configuration file in the repository.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Model structs: `LicenseGroup` (license name, list of packages, compliant flag) and `LicenseReport` (list of `LicenseGroup` entries, summary statistics)
- `common/src/license_policy.rs` — `LicensePolicy` struct with list of allowed/denied licenses, JSON deserialization, and a `check_compliance(license: &str) -> bool` method

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new model module
- `common/src/lib.rs` — Add `pub mod license_policy;` to expose the policy module
- `Cargo.toml` — Add `serde_json` dependency if not already present (for policy config loading)

## Implementation Notes
- Follow the established module pattern: each domain module uses `model/ + service/ + endpoints/` structure. The `license_report.rs` model file follows the same pattern as `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails).
  Per CONVENTIONS.md: follow the existing module pattern (model/ + service/ + endpoints/) for new domain features.
  Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's `.rs` module scope.
- The `LicenseGroup` struct should include: `license: String`, `packages: Vec<PackageSummary>`, `compliant: bool`. Reference `modules/fundamental/src/package/model/summary.rs` for the existing `PackageSummary` struct which includes the `license` field.
- The `LicensePolicy` should support both allowlist and denylist modes, loaded from a JSON config file (e.g., `license-policy.json` at the repo root or a configurable path).
- All structs must derive `Serialize` and `Deserialize` for API response serialization, following the pattern in existing model files.
- Error handling: use `Result<T, AppError>` with `.context()` wrapping per `common/src/error.rs` (AppError enum).
  Per CONVENTIONS.md: all error handling uses `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `common/src/license_policy.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Existing package summary struct that includes the `license` field; reuse as the package representation within license groups
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference implementation for model struct patterns (derive macros, field types, serialization)
- `common/src/error.rs::AppError` — Shared error type to reuse for policy loading errors

## Acceptance Criteria
- [ ] `LicenseGroup` struct exists with fields: license name, list of packages, and compliant boolean flag
- [ ] `LicenseReport` struct exists with a list of `LicenseGroup` entries
- [ ] `LicensePolicy` struct can be deserialized from a JSON configuration file
- [ ] `LicensePolicy::check_compliance()` correctly returns true for allowed licenses and false for denied licenses
- [ ] All structs derive `Serialize` and `Deserialize`
- [ ] Module exports are added to `mod.rs` and `lib.rs`

## Test Requirements
- [ ] Unit test: `LicensePolicy` loads from a valid JSON config file and correctly identifies compliant/non-compliant licenses
- [ ] Unit test: `LicensePolicy` returns an error for malformed JSON config
- [ ] Unit test: `LicenseReport` serializes to the expected JSON structure: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Verification Commands
- `cargo build` — compiles without errors
- `cargo test --lib` — all unit tests pass
