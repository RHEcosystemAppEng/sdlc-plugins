## Repository
trustify-backend

## Target Branch
main

## Description
Create a `LicensePolicy` model struct that represents a configurable license compliance policy. The policy defines which licenses are allowed, denied, or flagged for review. It is loaded from a JSON configuration file in the repository and used by the license report service to determine compliance status for each package.

## Files to Create
- `modules/fundamental/src/sbom/model/license_policy.rs` — LicensePolicy struct with fields for allowed_licenses, denied_licenses, and review_required_licenses; includes deserialization from JSON
- `license-policy.json` — Default license policy configuration file at the repository root

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_policy;` to export the new module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/model/details.rs` (SbomDetails) for struct definition and serde derives.
- The struct should derive `Debug, Clone, Serialize, Deserialize` to match existing model conventions.
- Include a `LicensePolicy::load(path: &Path) -> Result<Self>` method for loading from a JSON file.
- Reference `common/src/error.rs` for `AppError` usage in error handling.
- Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` structure for the new domain. Applies: task modifies `modules/fundamental/src/sbom/model/mod.rs` matching the convention's module structure scope.

## Acceptance Criteria
- [ ] `LicensePolicy` struct is defined with `allowed_licenses`, `denied_licenses`, and `review_required_licenses` fields (each a `Vec<String>` of SPDX identifiers)
- [ ] `LicensePolicy` can be deserialized from a JSON file
- [ ] A default `license-policy.json` configuration file exists at the repo root
- [ ] The policy model is exported via `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test: deserialize a valid license policy JSON into the struct
- [ ] Unit test: deserialize handles missing optional fields gracefully
- [ ] Unit test: `LicensePolicy::load` returns an error for a non-existent file path

## Dependencies
- None (first task)
