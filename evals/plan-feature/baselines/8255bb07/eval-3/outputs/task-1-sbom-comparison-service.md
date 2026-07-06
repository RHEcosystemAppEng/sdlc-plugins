## Repository
trustify-backend

## Target Branch
main

## Description
Implement the SBOM comparison diff logic that computes structural differences between two SBOMs. This includes model types for the comparison response and a service method that fetches package, advisory, and license data for both SBOMs, then computes six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

This is the core business logic for the SBOM comparison feature (TC-9003). The comparison must operate on existing data — no new database tables are needed. The diff is computed on-the-fly from existing SBOM-package and SBOM-advisory relationships.

## Files to Create
- `modules/fundamental/src/sbom/model/compare.rs` — Comparison response model: SbomComparisonResult struct with fields for each diff category (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes) and supporting item structs (AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
- `modules/fundamental/src/sbom/service/compare.rs` — Comparison service method: SbomService::compare(left_id, right_id) that fetches packages and advisories for both SBOMs, computes set differences, and returns SbomComparisonResult

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod compare;` to expose the comparison model
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to expose the comparison service

## API Changes
- `SbomService::compare(left_id: Uuid, right_id: Uuid) -> Result<SbomComparisonResult, AppError>` — NEW: Core diff computation method

## Implementation Notes
- Follow the existing module pattern: the SBOM domain uses `model/` for data structures and `service/` for business logic, as seen in `modules/fundamental/src/sbom/model/summary.rs` (SbomSummary) and `modules/fundamental/src/sbom/service/sbom.rs` (SbomService).
- Use `PackageSummary` from `modules/fundamental/src/package/model/summary.rs` to access package name, version, and license fields for diff computation.
- Use `AdvisorySummary` from `modules/fundamental/src/advisory/model/summary.rs` to access advisory ID, severity, and title for vulnerability diff.
- Query SBOM-package relationships via `entity/src/sbom_package.rs` join table and SBOM-advisory relationships via `entity/src/sbom_advisory.rs` join table.
- Use `common/src/db/query.rs` query builder helpers for efficient data fetching. Fetch all packages and advisories for both SBOMs in batch queries to avoid N+1 problems.
- All methods must return `Result<T, AppError>` with `.context()` wrapping per the project error handling pattern (see `common/src/error.rs`).
- Performance constraint: p95 < 1s for SBOMs with up to 2000 packages each. Use HashSet-based set difference for O(n) diff computation — key packages by name for set operations.
- The `direction` field for version changes should be computed by comparing semver strings (upgrade when right > left, downgrade when right < left).
- Per CONVENTIONS.md §Module Pattern: follow the `model/ + service/ + endpoints/` structure for the new comparison module files.
  Applies: task creates `modules/fundamental/src/sbom/model/compare.rs` matching the convention's `.rs` module file scope.
- Per CONVENTIONS.md §Error Handling: all service methods return `Result<T, AppError>` with `.context()` wrapping on fallible operations.
  Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's `.rs` service file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list methods; extend with compare method
- `modules/fundamental/src/sbom/model/details.rs::SbomDetails` — existing SBOM detail model showing field structure patterns
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — package model with name, version, license fields needed for diff
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — advisory model with severity field needed for vulnerability diff
- `common/src/error.rs::AppError` — standard error type for all service methods
- `entity/src/sbom_package.rs` — SeaORM entity for SBOM-package join table (query patterns)
- `entity/src/sbom_advisory.rs` — SeaORM entity for SBOM-advisory join table (query patterns)

## Acceptance Criteria
- [ ] SbomComparisonResult model type with six diff categories is defined and serializable (Serialize/Deserialize)
- [ ] SbomService::compare() correctly identifies added packages (in right SBOM but not left)
- [ ] SbomService::compare() correctly identifies removed packages (in left SBOM but not right)
- [ ] SbomService::compare() correctly identifies version changes with upgrade/downgrade direction
- [ ] SbomService::compare() correctly identifies new vulnerabilities (advisories affecting right but not left)
- [ ] SbomService::compare() correctly identifies resolved vulnerabilities (advisories affecting left but not right)
- [ ] SbomService::compare() correctly identifies license changes for packages present in both SBOMs
- [ ] Comparison completes within 1s for SBOMs with 2000 packages each (p95 target)

## Test Requirements
- [ ] Unit test: compare two SBOMs where right has additional packages — verify added_packages contains them
- [ ] Unit test: compare two SBOMs where left has packages not in right — verify removed_packages contains them
- [ ] Unit test: compare two SBOMs with same package at different versions — verify version_changes with correct direction
- [ ] Unit test: compare two SBOMs where right introduces new advisories — verify new_vulnerabilities
- [ ] Unit test: compare two SBOMs where left has advisories not in right — verify resolved_vulnerabilities
- [ ] Unit test: compare two SBOMs where same package has different licenses — verify license_changes
- [ ] Unit test: compare identical SBOMs — verify all diff categories are empty
- [ ] Unit test: verify error handling when an SBOM ID does not exist

## Verification Commands
- `cargo test --package fundamental -- sbom::service::compare` — all comparison service unit tests pass
- `cargo check --package fundamental` — no compilation errors

## Dependencies
- No dependencies — this is the first task
