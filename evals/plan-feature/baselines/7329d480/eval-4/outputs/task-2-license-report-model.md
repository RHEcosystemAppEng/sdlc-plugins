## Repository
trustify-backend

## Target Branch
main

## Description
Create the response model structs for the license compliance report endpoint. The report groups packages by license type and includes a compliance flag per group indicating whether the license is approved, restricted, or prohibited according to the configured policy.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Response structs: `LicenseReport`, `LicenseGroup`, and compliance status types

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` re-export

## API Changes
- `GET /api/v2/sbom/{id}/license-report` — NEW: Returns `LicenseReport` with structure `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/` where `summary.rs` defines `SbomSummary` and `details.rs` defines `SbomDetails`. The `license_report.rs` module should define serializable response structs.
- `LicenseReport` should contain a `Vec<LicenseGroup>` field named `groups`.
- `LicenseGroup` should contain: `license: String` (SPDX identifier), `packages: Vec<PackageLicenseInfo>`, `compliant: bool`, and `policy_category: String` (approved/restricted/prohibited/unknown).
- `PackageLicenseInfo` should contain: `name: String`, `version: String`, `purl: Option<String>`, `transitive: bool` (whether this is a direct or transitive dependency).
- Derive `serde::Serialize` on all response structs for JSON serialization.
- Per CONVENTIONS.md §Error handling: any fallible conversions or builder methods should return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's .rs scope.
- Per CONVENTIONS.md §Module pattern: place the model in the `model/` subdirectory of the sbom module following the established model/service/endpoints structure. Applies: task creates `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's module organization scope.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Existing package model that includes a `license` field; use as reference for field naming and structure
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Pattern reference for how SBOM-related models are structured and serialized

## Acceptance Criteria
- [ ] `LicenseReport` struct serializes to the specified JSON shape: `{ groups: [{ license, packages, compliant }] }`
- [ ] `PackageLicenseInfo` includes name, version, purl, and transitive flag
- [ ] Each `LicenseGroup` includes the policy category (approved/restricted/prohibited/unknown)
- [ ] Module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Unit test: `LicenseReport` serializes to expected JSON structure
- [ ] Unit test: empty report (no groups) serializes correctly

## Dependencies
- None (model structs are self-contained; policy evaluation is in the service layer)

## additional_fields
```json
{ "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```
