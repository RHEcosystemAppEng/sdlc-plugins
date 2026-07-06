## Repository
trustify-backend

## Target Branch
main

## Description
Add a license policy configuration model that defines which licenses are compliant and which are non-compliant for a given project. The policy is stored as a JSON configuration file in the repository and loaded at runtime. This provides the compliance rules used by the license report service (Task 2) to flag non-compliant packages.

## Files to Create
- `modules/fundamental/src/sbom/model/license_policy.rs` — LicensePolicy struct with fields for allowed licenses, denied licenses, and default compliance behavior; includes deserialization from JSON and a method to check whether a given SPDX license identifier is compliant

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod license_policy;` to expose the new module
- `Cargo.toml` — add `serde_json` dependency if not already present (for JSON config loading)

## Implementation Notes
- Define a `LicensePolicy` struct with:
  - `allowed: Vec<String>` — SPDX identifiers explicitly allowed
  - `denied: Vec<String>` — SPDX identifiers explicitly denied
  - `default_policy: PolicyDefault` — enum (`Allow` or `Deny`) for licenses not in either list
- Implement `LicensePolicy::from_file(path: &Path) -> Result<Self, AppError>` to load and deserialize the JSON config
- Implement `LicensePolicy::is_compliant(&self, license_id: &str) -> bool` to check a license against the policy
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` for struct definition and derive macros
- Use `serde::Deserialize` for JSON deserialization, consistent with the existing SeaORM entity patterns
- Per CONVENTIONS.md: follow the module pattern (model/ + service/ + endpoints/) — this task adds the model layer only.
  Applies: task creates `modules/fundamental/src/sbom/model/license_policy.rs` matching the convention's `.rs` module scope.
- Error handling: wrap deserialization errors using `AppError` with `.context()` per `common/src/error.rs` pattern.
  Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the convention's `.rs` error handling scope.

## Reuse Candidates
- `common/src/error.rs::AppError` — use AppError for error handling in the policy loader, consistent with all other modules
- `entity/src/package_license.rs` — reference the existing package-license entity to understand the license identifier format stored in the database

## Acceptance Criteria
- [ ] `LicensePolicy` struct is defined with allowed, denied, and default_policy fields
- [ ] `LicensePolicy::from_file` correctly loads and parses a JSON policy file
- [ ] `LicensePolicy::is_compliant` correctly classifies licenses as compliant or non-compliant based on the policy
- [ ] Policy with `default_policy: Allow` permits unlisted licenses
- [ ] Policy with `default_policy: Deny` rejects unlisted licenses

## Test Requirements
- [ ] Unit test: load a valid JSON policy file and verify fields are populated correctly
- [ ] Unit test: `is_compliant` returns true for allowed licenses
- [ ] Unit test: `is_compliant` returns false for denied licenses
- [ ] Unit test: `is_compliant` respects default_policy for licenses not in either list
- [ ] Unit test: `from_file` returns AppError for invalid JSON input

## Dependencies
- None
