# Task 3 — Implement SBOM comparison service logic

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the service-layer logic that computes a structured diff between two SBOMs. The service fetches package lists and advisory associations for both SBOMs, computes set differences for added/removed packages, detects version changes, identifies new and resolved vulnerabilities, and detects license changes. The diff is computed on-the-fly without new database tables, using existing package, advisory, and SBOM data.

## Files to Create
- `modules/fundamental/src/sbom/service/compare.rs` — SbomComparisonService or comparison method on SbomService: accepts two SBOM IDs, returns SbomComparisonResult

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` or integrate comparison logic into the existing service module

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) — services accept a database connection/pool and return `Result<T, AppError>` using `.context()` wrapping from `common/src/error.rs`.
- Use `PackageService` from `modules/fundamental/src/package/service/mod.rs` to fetch package lists for each SBOM, including license information from the `PackageSummary` struct.
- Use `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs` to fetch advisory associations for each SBOM.
- Compute the diff using set operations on package names:
  - Added packages: packages in right SBOM not in left SBOM (by package identifier)
  - Removed packages: packages in left SBOM not in right SBOM
  - Version changes: packages in both SBOMs with different versions — determine direction by version comparison
  - New vulnerabilities: advisories affecting right SBOM not affecting left SBOM
  - Resolved vulnerabilities: advisories affecting left SBOM not affecting right SBOM
  - License changes: packages in both SBOMs with different license values
- Use `HashMap` for efficient set difference computation on package identifiers.
- The non-functional requirement specifies p95 < 1s for SBOMs with up to 2000 packages each — ensure the algorithm is O(n) with hash-based lookups, not O(n^2) with nested loops.
- Use query helpers from `common/src/db/query.rs` for any database queries that support filtering or pagination.
- Per docs/constraints.md §5.4: Do not duplicate existing functionality — reuse PackageService and AdvisoryService rather than writing new query logic.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Follow the same service pattern for method signatures and error handling
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Reuse to fetch package lists for each SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Reuse to fetch advisory associations
- `common/src/error.rs::AppError` — Use for error propagation with `.context()` wrapping
- `common/src/db/query.rs` — Use shared query helpers for filtering and pagination if fetching large package lists

## Acceptance Criteria
- [ ] Comparison function accepts two SBOM IDs and returns `Result<SbomComparisonResult, AppError>`
- [ ] Correctly identifies added, removed packages by comparing package sets
- [ ] Correctly detects version changes and classifies as upgrade/downgrade
- [ ] Correctly identifies new and resolved vulnerabilities
- [ ] Correctly detects license changes between the two SBOMs
- [ ] Performance: handles SBOMs with 2000 packages each using O(n) hash-based algorithm

## Test Requirements
- [ ] Unit test: comparison of two SBOMs with known package differences produces correct added/removed lists
- [ ] Unit test: version changes correctly classified as upgrade vs downgrade
- [ ] Unit test: vulnerability diff correctly identifies new and resolved advisories
- [ ] Unit test: license changes detected when same package has different licenses
- [ ] Unit test: comparison of identical SBOMs returns empty diff (all lists empty)
- [ ] Unit test: comparison where one SBOM has no packages returns all packages as added or removed

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison diff model types

sha256-md:412933fe01a1bcf58f9da4136a97bad7feb2ac88b63678762229935229500245
