## Repository
trustify-backend

## Target Branch
main

## Description
Create the license policy configuration model and service that loads a JSON-based license policy file and evaluates whether a given license identifier is compliant. The policy defines lists of allowed and/or denied SPDX license identifiers. This is the foundation for the license compliance report feature (TC-9004).

## Files to Create
- `config/license-policy.json` — Default license policy configuration with allowed/denied license lists
- `modules/fundamental/src/sbom/license_report/mod.rs` — Module declaration for the license_report submodule
- `modules/fundamental/src/sbom/license_report/model/mod.rs` — LicensePolicy struct (deserializable from JSON), LicenseComplianceResult enum
- `modules/fundamental/src/sbom/license_report/service/mod.rs` — LicensePolicyService: load policy from config file, evaluate a license string against the policy

## Files to Modify
- `modules/fundamental/src/sbom/mod.rs` — Add `pub mod license_report;` submodule declaration
- `modules/fundamental/Cargo.toml` — Add `serde_json` dependency if not already present

## Implementation Notes
Follow the existing module pattern of `model/ + service/ + endpoints/` as seen in `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/`.

The LicensePolicy struct should be a simple serde-deserializable struct loaded from a JSON config file at service initialization. The PackageSummary struct in `modules/fundamental/src/package/model/summary.rs` already includes a `license` field -- use this as the license identifier to evaluate against the policy.

For error handling, follow the pattern in `common/src/error.rs` -- return `Result<T, AppError>` with `.context()` wrapping for all fallible operations.

Per CONVENTIONS.md §Module pattern: follow `model/ + service/ + endpoints/` structure. Applies: task creates `modules/fundamental/src/sbom/license_report/model/mod.rs` and `modules/fundamental/src/sbom/license_report/service/mod.rs` matching the convention's module directory scope.

Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/license_report/service/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Framework: use SeaORM for database access. Applies: task creates `modules/fundamental/src/sbom/license_report/service/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/error.rs::AppError` — Error type for Result returns; reuse for all fallible operations in the new service
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Contains the `license` field that will be evaluated against the policy

## Acceptance Criteria
- [ ] LicensePolicy struct can be deserialized from a JSON configuration file
- [ ] LicensePolicyService can load the default policy from `config/license-policy.json`
- [ ] LicensePolicyService can evaluate a license identifier and return compliant/non-compliant status
- [ ] Default policy file includes reasonable defaults (e.g., MIT, Apache-2.0 as allowed)
- [ ] Errors during policy loading are wrapped with AppError and context

## Test Requirements
- [ ] Unit test: LicensePolicy deserialization from valid JSON
- [ ] Unit test: policy evaluation returns compliant for an allowed license
- [ ] Unit test: policy evaluation returns non-compliant for a denied license
- [ ] Unit test: policy loading fails gracefully with a descriptive error for malformed JSON
