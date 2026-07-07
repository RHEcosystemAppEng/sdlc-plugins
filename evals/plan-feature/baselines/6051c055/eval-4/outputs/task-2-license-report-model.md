## Repository
trustify-backend

## Target Branch
main

## Description
Create the response model structs for the license compliance report. These structs represent the API response shape: a top-level `LicenseReport` containing metadata, a list of `LicenseGroup` entries (packages grouped by their license), a list of `LicenseConflict` entries (packages with conflicting or dual-licensed situations), and overall compliance summary statistics.

## Files to Modify
- `modules/fundamental/src/lib.rs` — add `pub mod license_report;` to register the new module

## Files to Create
- `modules/fundamental/src/license_report/mod.rs` — module root, re-exports `model`, `service`, `endpoints` submodules
- `modules/fundamental/src/license_report/model.rs` — response structs: `LicenseReport` (sbom_id, generated_at, summary, groups, conflicts), `LicenseReportSummary` (total_packages, compliant_count, non_compliant_count, review_required_count), `LicenseGroup` (license_spdx, classification, packages list), `LicenseConflict` (package_id, package_name, licenses list, reason)

## Implementation Notes
- All response structs derive `Serialize, Deserialize, Clone, Debug, utoipa::ToSchema` for OpenAPI spec generation, following the pattern in `modules/fundamental/src/package/model/summary.rs`
- Use `chrono::DateTime<Utc>` for the `generated_at` timestamp
- The `classification` field in `LicenseGroup` reuses the `Classification` enum from task 1
- `LicenseConflict.reason` should be a human-readable string explaining why the licenses conflict (e.g., "Package has both copyleft and permissive licenses")
- Keep `mod.rs` minimal — only `pub mod model;` initially; `service` and `endpoints` submodules will be added in subsequent tasks

## Acceptance Criteria
- [ ] All response structs compile and are accessible from `modules::fundamental::license_report::model`
- [ ] Structs derive `Serialize`, `Deserialize`, and `utoipa::ToSchema`
- [ ] `LicenseReport` contains `sbom_id`, `generated_at`, `summary`, `groups`, and `conflicts` fields
- [ ] `LicenseReportSummary` contains count fields for total, compliant, non-compliant, review-required
- [ ] `LicenseGroup` groups packages under a single license with a classification
- [ ] `LicenseConflict` identifies a package with conflicting licenses

## Test Requirements
- [ ] Unit test: `LicenseReport` serializes to expected JSON structure
- [ ] Unit test: `LicenseReportSummary` counts are correct for a hand-built report
- [ ] Unit test: round-trip serialization/deserialization for all structs
