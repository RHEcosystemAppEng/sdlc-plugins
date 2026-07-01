## Repository
trustify-backend

## Target Branch
main

## Description
Create the response model structs for the license compliance report. These structs define the shape of the JSON response returned by the license report endpoint, grouping packages by license with compliance flags.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Structs: `LicenseReport { sbom_id, generated_at, groups, summary }`, `LicenseGroup { license: String, packages: Vec<PackageLicenseInfo>, compliant: bool }`, `PackageLicenseInfo { name, version, purl }`, `ComplianceSummary { total_packages, compliant_count, non_compliant_count }`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new module

## Implementation Notes
Follow the model struct conventions from `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs`. Use `#[derive(Clone, Debug, Serialize, Deserialize)]` and `utoipa::ToSchema` if the project uses OpenAPI generation. The `compliant` field on `LicenseGroup` should be derived from the license policy check, not stored. Reference `entity/src/package.rs` for the `Package` entity fields and `entity/src/package_license.rs` for the license mapping.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Pattern reference for struct layout and serde derives
- `common/src/model/paginated.rs::PaginatedResults` — Pattern reference for response wrapper conventions

## Acceptance Criteria
- [ ] `LicenseReport` struct serializes to JSON matching the format: `{ sbom_id, generated_at, groups: [{ license, packages: [...], compliant }], summary: { total_packages, compliant_count, non_compliant_count } }`
- [ ] All structs implement Serialize, Deserialize, Clone, and Debug

## Test Requirements
- [ ] Unit test: LicenseReport serializes to expected JSON structure
- [ ] Unit test: LicenseGroup with compliant=false is correctly represented

## Dependencies
- Depends on: Task 1 — License policy configuration (uses LicenseCompliance enum)
