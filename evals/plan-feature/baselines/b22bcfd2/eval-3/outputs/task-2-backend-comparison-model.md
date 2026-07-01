## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the data model structs for the SBOM comparison result. These structs represent the structured diff between two SBOMs: added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The models are needed before the service and endpoint layers can be implemented.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add module declaration for the new comparison model

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — define SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange structs with Serialize/Deserialize derives

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` which define structs with `#[derive(Clone, Debug, Serialize, Deserialize)]`.

The comparison result struct should contain six Vec fields matching the API response shape:
- `added_packages: Vec<AddedPackage>` — fields: name, version, license, advisory_count
- `removed_packages: Vec<RemovedPackage>` — fields: name, version, license, advisory_count
- `version_changes: Vec<VersionChange>` — fields: name, left_version, right_version, direction (enum: Upgrade/Downgrade)
- `new_vulnerabilities: Vec<NewVulnerability>` — fields: advisory_id, severity, title, affected_package
- `resolved_vulnerabilities: Vec<ResolvedVulnerability>` — fields: advisory_id, severity, title, previously_affected_package
- `license_changes: Vec<LicenseChange>` — fields: name, left_license, right_license

Reuse the severity representation from `modules/fundamental/src/advisory/model/summary.rs` (AdvisorySummary includes a severity field).

Reference `entity/src/package.rs` for the Package entity fields (name, version) and `entity/src/package_license.rs` for the license mapping to ensure field names are consistent.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct derive patterns and serialization approach
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity field representation to reuse

## Acceptance Criteria
- [ ] SbomComparisonResult struct is defined with all six diff category fields
- [ ] All sub-structs (AddedPackage, RemovedPackage, etc.) are defined with correct fields
- [ ] Structs derive Serialize, Deserialize, Clone, Debug
- [ ] Module is declared and exported from `modules/fundamental/src/sbom/model/mod.rs`

## Test Requirements
- [ ] Structs can be serialized to JSON matching the expected API response shape
- [ ] Structs can be deserialized from JSON representing valid comparison data

## Dependencies
- Depends on: Task 1 — Create feature branch
