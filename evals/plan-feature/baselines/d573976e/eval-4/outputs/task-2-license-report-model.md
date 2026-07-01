# Task 2 — Add license report response model

## Repository
trustify-backend

## Target Branch
main

## Description
Add the response model structs for the license compliance report. The report groups packages by license type and includes compliance flags based on the license policy. These structs define the API response shape for the license report endpoint.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `license_report` module declaration

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseReportSummary (top-level response with groups vec), LicenseGroup (license identifier, list of packages, compliant flag)

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs`
- The response shape must match the feature specification:
  ```json
  {
    "groups": [
      {
        "license": "MIT",
        "packages": [{ "name": "...", "version": "..." }],
        "compliant": true
      }
    ]
  }
  ```
- Derive `Serialize` for API response serialization
- The package entry within each group should reference the existing `PackageSummary` struct from `modules/fundamental/src/package/model/summary.rs` or include a minimal subset (name, version, purl) to keep the response lightweight
- Consider including a top-level `compliant` boolean on LicenseReportSummary that is true only when all groups are compliant — this enables the CI/CD gate use case (UC-2)

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — follow struct and serialization patterns
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reuse or reference for package data within license groups
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — follow response model conventions

## Acceptance Criteria
- [ ] LicenseReportSummary struct serializes to the specified JSON response shape
- [ ] LicenseGroup contains license identifier, package list, and compliant boolean
- [ ] Top-level compliant flag correctly reflects aggregate compliance state
- [ ] Model structs are accessible from the sbom model module

## Test Requirements
- [ ] Unit test: serialize a LicenseReportSummary with mixed compliant/non-compliant groups and verify JSON output shape
- [ ] Unit test: verify top-level compliant flag is false when any group is non-compliant

## Dependencies
- None
