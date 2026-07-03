## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the Rust model types for the SBOM comparison response. These types represent the structured diff between two SBOMs, covering added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The types will be serialized as JSON responses from the comparison endpoint.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` -- Comparison result model types (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` -- Add `pub mod comparison;` to expose the new module

## Implementation Notes
- Follow the existing model pattern in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` -- derive `Serialize`, `Deserialize`, `Clone`, `Debug` on all structs.
- The response shape must match the API contract agreed with the frontend:
  ```json
  {
    "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..." }],
    "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
    "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
  }
  ```
- Use `#[serde(rename_all = "snake_case")]` for consistent JSON field naming.
- The `direction` field in `VersionChange` should be an enum with variants `Upgrade` and `Downgrade`, serialized as lowercase strings.
- Per CONVENTIONS.md (Key Conventions) -- Module pattern: follow the `model/ + service/ + endpoints/` structure. Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's module pattern scope.
- Per docs/constraints.md SS2: commit must reference TC-9003 in footer. Per SS3: branch must be named TC-9003.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- reference for struct derive patterns and serde configuration
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- contains `license` field pattern to follow
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- contains `severity` field pattern to follow

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct defined with all six diff category fields
- [ ] All sub-types (AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange) defined with correct fields
- [ ] All types derive Serialize and Deserialize for JSON serialization
- [ ] Module properly exported from `model/mod.rs`

## Test Requirements
- [ ] Types compile and are accessible from other modules
- [ ] Serialization round-trip test: create a populated SbomComparisonResult, serialize to JSON, deserialize back, assert equality

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
