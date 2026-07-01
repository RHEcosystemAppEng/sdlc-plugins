## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the response model types for the SBOM comparison feature. These structs define the shape of the comparison result returned by the new diffing endpoint, covering added/removed packages, version changes, new/resolved vulnerabilities, and license changes.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add module declarations for the new comparison types

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — define `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, and `LicenseChange` structs with Serialize/Deserialize derives

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each struct derives `Clone, Debug, Serialize, Deserialize` and uses `utoipa::ToSchema` for OpenAPI documentation.
- The `SbomComparisonResult` struct should contain six Vec fields matching the API response shape:
  - `added_packages: Vec<PackageDiff>` — fields: name, version, license, advisory_count
  - `removed_packages: Vec<PackageDiff>` — same fields as added_packages
  - `version_changes: Vec<VersionChange>` — fields: name, left_version, right_version, direction (String: "upgrade"/"downgrade")
  - `new_vulnerabilities: Vec<VulnerabilityDiff>` — fields: advisory_id, severity, title, affected_package
  - `resolved_vulnerabilities: Vec<VulnerabilityDiff>` — fields: advisory_id, severity, title, previously_affected_package
  - `license_changes: Vec<LicenseChange>` — fields: name, left_license, right_license
- Reference `common/src/model/paginated.rs` for the pattern of deriving `utoipa::ToSchema` on response types.
- All handlers return `Result<T, AppError>` per the error handling convention — ensure the model types are compatible with this pattern.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — existing SBOM model struct demonstrating the derive pattern and field conventions
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — shows how severity field is represented in model types
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — shows how license field is represented

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff category fields
- [ ] `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, and `LicenseChange` structs are defined with correct fields
- [ ] All structs derive `Serialize`, `Deserialize`, `Clone`, `Debug`, and `ToSchema`
- [ ] Module is declared in `mod.rs` and publicly exported

## Test Requirements
- [ ] Structs compile and can be serialized to JSON matching the expected API response shape
- [ ] Round-trip serialization test: create an `SbomComparisonResult` instance, serialize to JSON, deserialize back, and assert equality

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main

## Description Digest
sha256-md:5fc6d5d68e345eb7cbea2371de6035b7ac3d0354237a7dc7dcd6e745611ce759
