## Repository
trustify-backend

## Target Branch
main

## Description
Define the license compliance report response model. The report groups packages by license type and includes a compliance flag for each group based on the license policy. This model is the response shape for the `GET /api/v2/sbom/{id}/license-report` endpoint.

## Files to Create
- `modules/fundamental/src/license/model/report.rs` — `LicenseComplianceReport` and `LicenseGroup` structs

## Files to Modify
- `modules/fundamental/src/license/model/mod.rs` — re-export the report module

## Implementation Notes
Follow the response model pattern from existing modules. Reference `modules/fundamental/src/sbom/model/summary.rs` (`SbomSummary`) for the struct and serialization pattern.

The `LicenseComplianceReport` struct should contain:
- `groups: Vec<LicenseGroup>` — packages grouped by license
- `total_packages: usize` — total package count
- `compliant: bool` — overall compliance flag (true only if all groups are compliant)

The `LicenseGroup` struct should contain:
- `license: String` — SPDX license identifier
- `packages: Vec<PackageSummary>` — packages with this license (reuse existing `PackageSummary` from `modules/fundamental/src/package/model/summary.rs`)
- `compliant: bool` — whether this license is compliant per policy

Both structs should derive `Serialize` for JSON response serialization.

Per CONVENTIONS.md §Module pattern: follow the model submodule structure established in sibling domain modules.
Applies: task creates `modules/fundamental/src/license/model/report.rs` matching the convention's Rust module scope.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reuse the existing package summary type for the packages list within each license group, rather than creating a new package representation

## Acceptance Criteria
- [ ] `LicenseComplianceReport` struct is defined with `groups`, `total_packages`, and `compliant` fields
- [ ] `LicenseGroup` struct is defined with `license`, `packages`, and `compliant` fields
- [ ] Both structs derive `Serialize` for JSON serialization
- [ ] `PackageSummary` from the package module is reused (not duplicated)

## Test Requirements
- [ ] Unit test: `LicenseComplianceReport` serializes to expected JSON shape matching the API contract `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`
- [ ] Unit test: overall `compliant` flag is false when any group is non-compliant

## Dependencies
- Depends on: Task 1 — License policy model
