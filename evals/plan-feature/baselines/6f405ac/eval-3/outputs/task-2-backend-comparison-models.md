## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the Rust structs for the SBOM comparison response. These types represent the structured diff between two SBOMs: added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The comparison endpoint (task 4) and service logic (task 3) will use these types.

## Files to Create
- `modules/fundamental/src/sbom/model/compare.rs` — Comparison response structs

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod compare;` re-export

## API Changes
- `GET /api/v2/sbom/compare?left={id}&right={id}` — NEW: Returns `SbomComparison` (this task defines the response type; the endpoint is wired in task 4)

## Implementation Notes
Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each model file defines a public struct with `serde::Serialize` and `serde::Deserialize` derives.

Define the following structs in `compare.rs`:
- `SbomComparison` — top-level response with fields: `added_packages: Vec<AddedPackage>`, `removed_packages: Vec<RemovedPackage>`, `version_changes: Vec<VersionChange>`, `new_vulnerabilities: Vec<NewVulnerability>`, `resolved_vulnerabilities: Vec<ResolvedVulnerability>`, `license_changes: Vec<LicenseChange>`
- `AddedPackage` — fields: `name`, `version`, `license`, `advisory_count`
- `RemovedPackage` — fields: `name`, `version`, `license`, `advisory_count`
- `VersionChange` — fields: `name`, `left_version`, `right_version`, `direction` (enum: upgrade/downgrade)
- `NewVulnerability` — fields: `advisory_id`, `severity`, `title`, `affected_package`
- `ResolvedVulnerability` — fields: `advisory_id`, `severity`, `title`, `previously_affected_package`
- `LicenseChange` — fields: `name`, `left_license`, `right_license`

Per CONVENTIONS.md §Module pattern: follow model/ + service/ + endpoints/ structure. Applies: task creates `modules/fundamental/src/sbom/model/compare.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md §Framework: use Axum for HTTP, SeaORM for database. Applies: convention has no file-type restriction (broadly applicable).

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct layout, serde derives, and field naming conventions
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for severity field type
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reference for license field type

## Acceptance Criteria
- [ ] `SbomComparison` struct and all nested structs are defined in `compare.rs`
- [ ] All structs derive `Serialize` and `Deserialize`
- [ ] `compare` module is re-exported from `modules/fundamental/src/sbom/model/mod.rs`
- [ ] Code compiles without errors

## Test Requirements
- [ ] Unit test verifying `SbomComparison` serializes to the expected JSON shape matching the API contract from the feature spec
- [ ] Unit test verifying `SbomComparison` deserializes from a representative JSON payload
