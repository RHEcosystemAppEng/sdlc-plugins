## Repository
trustify-backend

## Target Branch
main

## Description
Add the response model types for the license compliance report. These types define the structure returned by the license-report endpoint, grouping packages by license and including compliance flags derived from the license policy.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add re-export for the new license_report module

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Define `LicenseReportResponse`, `LicenseGroup`, and `PackageLicenseEntry` structs. `LicenseReportResponse` contains a `groups: Vec<LicenseGroup>` and `summary` (total packages, compliant count, non-compliant count). `LicenseGroup` contains `license: String`, `classification: LicenseClassification`, `compliant: bool`, `packages: Vec<PackageLicenseEntry>`. `PackageLicenseEntry` contains `package_id`, `name`, `version`, `is_transitive: bool`.

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/` (see `summary.rs` and `details.rs` for examples).
- All structs should derive `Serialize, Deserialize, Clone, Debug, utoipa::ToSchema` to enable OpenAPI documentation.
- The `compliant` field on `LicenseGroup` should be `true` when the classification is `Approved`, `false` for `Denied`, and configurable for `Restricted`.
- The `summary` field provides a quick overview: `{ total_packages, compliant_count, non_compliant_count, restricted_count }`.

## Acceptance Criteria
- [ ] `LicenseReportResponse` serializes to the expected JSON structure: `{ groups: [...], summary: {...} }`
- [ ] Each `LicenseGroup` includes the license name, classification, compliance flag, and list of packages
- [ ] OpenAPI schema is generated for all new types

## Test Requirements
- [ ] Unit test: construct a `LicenseReportResponse` and verify JSON serialization matches expected format
- [ ] Unit test: verify `compliant` flag logic for each classification variant

## Dependencies
- Depends on: Task 1 — License policy model (uses `LicenseClassification` enum)
