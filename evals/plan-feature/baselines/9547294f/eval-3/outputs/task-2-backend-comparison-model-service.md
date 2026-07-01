# Task 2 — Add SBOM comparison diff model and service

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the data model types and service logic for computing a structured diff between two SBOMs. The service queries existing package, advisory, and license data to produce a comparison result without creating new database tables. This is the core diffing logic that the comparison endpoint (Task 3) will expose via REST.

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — Define SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange structs with Serialize derives
- `modules/fundamental/src/sbom/service/compare.rs` — Implement the compare method on SbomService that takes two SBOM IDs and returns SbomComparisonResult

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new comparison model module
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to expose the new comparison service module

## API Changes
- None (this task adds internal service logic only; the REST endpoint is in Task 3)

## Implementation Notes

### Model design

The comparison result struct should follow the response shape specified by the feature requirements:

```rust
pub struct SbomComparisonResult {
    pub added_packages: Vec<AddedPackage>,
    pub removed_packages: Vec<RemovedPackage>,
    pub version_changes: Vec<VersionChange>,
    pub new_vulnerabilities: Vec<NewVulnerability>,
    pub resolved_vulnerabilities: Vec<ResolvedVulnerability>,
    pub license_changes: Vec<LicenseChange>,
}
```

Each sub-struct should derive `Serialize` and `Clone`. Use `#[serde(rename_all = "snake_case")]` for consistent JSON field naming.

### Service implementation

The `compare` method should:
1. Fetch packages for both SBOMs using existing `PackageService` queries via the `sbom_package` join table
2. Compute set differences for added/removed packages
3. Detect version changes by matching on package name across both sets
4. Fetch advisories linked to each SBOM via the `sbom_advisory` join table and compute new/resolved vulnerabilities
5. Detect license changes by comparing the `license` field on packages present in both SBOMs

Follow the existing `SbomService` patterns in `modules/fundamental/src/sbom/service/sbom.rs` — use `Result<T, AppError>` return types with `.context()` wrapping on all DB queries.

### Performance considerations

- The NFR requires p95 < 1s for SBOMs with up to 2000 packages each. Use batch queries rather than per-package lookups.
- Compute the diff in memory after fetching both package sets — do not use N+1 query patterns.

### Reuse candidates

- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service struct to extend with the `compare` method
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing package model with `license` field
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — existing advisory model with `severity` field
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for querying advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping for license comparison
- `common/src/error.rs::AppError` — error type for Result returns

Per CONVENTIONS.md: follow the `model/ + service/ + endpoints/` module pattern for the SBOM domain.
Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` and `modules/fundamental/src/sbom/service/compare.rs` matching the convention's Rust module structure scope.

## Acceptance Criteria
- [ ] SbomComparisonResult and all sub-structs compile and serialize to JSON matching the expected response shape
- [ ] SbomService::compare(left_id, right_id) returns a correctly computed diff for two SBOMs
- [ ] Added packages (in right but not left) are detected
- [ ] Removed packages (in left but not right) are detected
- [ ] Version changes for packages present in both SBOMs are detected with upgrade/downgrade direction
- [ ] New vulnerabilities (advisories affecting right but not left) are detected with severity
- [ ] Resolved vulnerabilities (advisories affecting left but not right) are detected
- [ ] License changes between the two SBOMs are detected

## Test Requirements
- [ ] Unit test for diff computation with known package sets (added, removed, version changed)
- [ ] Unit test for vulnerability diff with known advisory sets (new, resolved)
- [ ] Unit test for license change detection
- [ ] Unit test for empty diff (identical SBOMs)
- [ ] Unit test for one or both SBOMs having no packages

## Verification Commands
- `cargo build -p trustify-fundamental` — should compile without errors
- `cargo test -p trustify-fundamental -- sbom::service::compare` — should pass all comparison tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main

---
Priority: Critical
Fix Versions: RHTPA 1.5.0
Labels: ai-generated-jira

[sdlc-workflow] Description digest: sha256-md:b4e8a2f6c1d9370e5b8f2a4c6d0e3b5a7f9c1d3e5b7a9f2c4e6d8b0a3c5f7e9d
