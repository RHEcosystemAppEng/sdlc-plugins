## Repository
trustify-backend

## Target Branch
main

## Description
Add the response model types for the license compliance report and the license policy configuration model with its JSON file loader. The license compliance report groups packages by license type and flags non-compliant licenses based on a configurable policy. The policy is stored as a JSON config file in the repository and loaded at service initialization.

This task establishes the data layer that the license report service (Task 2) and endpoint (Task 3) will consume.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` -- license compliance report response types: `LicenseGroup` (license name, list of packages, compliant flag) and `LicenseComplianceReport` (list of `LicenseGroup` entries, summary statistics)
- `common/src/model/license_policy.rs` -- license policy configuration model: `LicensePolicy` struct (allowed/denied license lists), JSON deserialization, and file loader function

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- add `pub mod license_report;` and re-export types
- `common/src/model/mod.rs` -- add `pub mod license_policy;` and re-export types

## Implementation Notes
- Follow the existing module pattern in `modules/fundamental/src/sbom/model/`: see `summary.rs` for `SbomSummary` and `details.rs` for `SbomDetails` as structural references for defining serializable response types.
- The `LicenseGroup` struct should contain: `license: String`, `packages: Vec<PackageRef>`, `compliant: bool`. Define `PackageRef` as a lightweight struct with package name, version, and purl.
- The `LicenseComplianceReport` struct should contain: `groups: Vec<LicenseGroup>`, plus optional summary fields (total packages, compliant count, non-compliant count).
- Both structs must derive `Serialize` and `Deserialize` (serde) for JSON responses.
- The `LicensePolicy` should support an `allowed_licenses` list (allowlist mode) or a `denied_licenses` list (denylist mode), plus a `policy_mode` enum to select between them.
- Use `serde_json::from_reader` for loading the policy from a JSON file path.
- The `PackageSummary` struct in `modules/fundamental/src/sbom/model/../../../package/model/summary.rs` already includes a `license` field -- reuse this type or reference its structure for consistency.
- Per docs/constraints.md S5.4: do not duplicate existing functionality. Check `entity/src/package_license.rs` for the existing Package-License mapping entity and reuse its field naming conventions.
- Per docs/constraints.md S4.6: all file paths listed here are real paths from the repository structure.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- reference for struct layout and serde derives in the SBOM model layer
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` -- reference for detailed response type patterns
- `entity/src/package_license.rs` -- existing Package-License entity mapping; reuse field names for consistency

## Acceptance Criteria
- [ ] `LicenseGroup` struct exists with `license`, `packages`, and `compliant` fields, all serializable
- [ ] `LicenseComplianceReport` struct exists with a `groups` field containing `Vec<LicenseGroup>`
- [ ] `LicensePolicy` struct exists with allowed/denied license configuration and JSON deserialization
- [ ] Policy loader function reads and parses a JSON policy file from a given path
- [ ] All new types are re-exported from their respective module `mod.rs` files
- [ ] Response shape matches the feature specification: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Test Requirements
- [ ] Unit test: `LicensePolicy` deserializes from a valid JSON string with allowed licenses
- [ ] Unit test: `LicensePolicy` deserializes from a valid JSON string with denied licenses
- [ ] Unit test: `LicenseComplianceReport` serializes to JSON matching the expected response shape
- [ ] Unit test: policy loader returns an error for a non-existent file path
- [ ] Unit test: policy loader returns an error for malformed JSON

## Dependencies
- None (this is the first task in the sequence)
