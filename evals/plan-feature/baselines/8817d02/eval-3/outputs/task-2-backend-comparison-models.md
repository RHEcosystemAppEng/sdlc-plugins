# Task 2 — Add SBOM comparison diff model types

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Define the Rust structs for the SBOM comparison response. These models represent the structured diff between two SBOMs: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. The models will be serialized as JSON by the comparison endpoint.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Comparison result structs: SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new module

## Implementation Notes
- Follow the existing model pattern established in `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/model/details.rs` — each struct derives `Clone, Debug, Serialize, Deserialize` and uses `serde` for JSON serialization.
- The `SbomComparisonResult` struct should contain six `Vec` fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`.
- The `VersionChange` struct needs a `direction` field — use a string enum (`"upgrade"` / `"downgrade"`) or a dedicated `ChangeDirection` enum.
- The `NewVulnerability` struct needs a `severity` field — reuse the severity type from `modules/fundamental/src/advisory/model/summary.rs` (AdvisorySummary includes a severity field).
- Per docs/constraints.md §4.6: File paths must be real paths discovered during repository analysis.
- Per docs/constraints.md §4.7: Implementation Notes must reference existing patterns found in the code.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Follow the same struct pattern (derive macros, serde attributes)
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reuse or reference the severity field type for vulnerability severity
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Reference license field type for license representation

## Acceptance Criteria
- [ ] `SbomComparisonResult` struct is defined with all six diff category fields
- [ ] All sub-structs (AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange) are defined with fields matching the API response shape from the feature specification
- [ ] All structs derive Serialize and Deserialize for JSON serialization
- [ ] Module is publicly exported from `sbom/model/mod.rs`

## Test Requirements
- [ ] Structs can be instantiated and serialized to JSON matching the expected response shape
- [ ] Deserialization round-trip test: serialize then deserialize produces identical struct

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main

sha256-md:9241f5ca1daac9aa69e0d81bc0d5dd3c6d4f45146a7919644458b43193c17d41
