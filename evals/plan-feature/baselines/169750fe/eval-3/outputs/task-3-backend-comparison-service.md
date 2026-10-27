## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the `SbomComparisonService` that computes a structured diff between two SBOMs. The service operates on existing package, advisory, and license data — no new database tables are required. It fetches package lists for both SBOMs, computes set differences for added/removed packages, identifies version changes, correlates advisory data for new/resolved vulnerabilities, and detects license changes.

## Files to Create
- `modules/fundamental/src/sbom/service/comparison.rs` — SbomComparisonService with compare method

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod comparison;` to expose the comparison service module

## Implementation Notes
Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for service struct definition and database interaction patterns.

The `compare` method should:
1. Fetch package lists for both SBOMs using `PackageService` from `modules/fundamental/src/package/service/mod.rs`
2. Compute package set differences (added, removed, version changed) by comparing package names
3. For each package diff, query advisory associations via the `sbom_advisory` and `sbom_package` join tables in `entity/src/`
4. Identify new vulnerabilities (advisories linked to right SBOM packages not linked to left SBOM packages)
5. Identify resolved vulnerabilities (advisories linked to left SBOM packages not linked to right SBOM packages)
6. Detect license changes using `package_license` entity from `entity/src/package_license.rs`

Use query helpers from `common/src/db/query.rs` for database queries. Use `AppError` from `common/src/error.rs` for error handling.

Non-functional requirement: p95 response time < 1s for SBOMs with up to 2000 packages each. Consider batch-loading packages rather than N+1 queries.

Per CONVENTIONS.md §Module Pattern: follow model/ + service/ + endpoints/ structure.
Applies: task creates `modules/fundamental/src/sbom/service/comparison.rs` matching the convention's Rust module file scope.

Per CONVENTIONS.md §Error Handling: all service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/service/comparison.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service pattern for database interactions
- `modules/fundamental/src/package/service/mod.rs::PackageService` — package data access for fetching package lists
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — advisory data access for vulnerability correlation
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/src/sbom_package.rs` — SBOM-Package join table for package list queries
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table for vulnerability correlation

## Acceptance Criteria
- [ ] `SbomComparisonService::compare(left_id, right_id)` returns a populated `SbomComparison` struct
- [ ] Added packages are correctly identified (in right but not left)
- [ ] Removed packages are correctly identified (in left but not right)
- [ ] Version changes are detected with correct direction (upgrade/downgrade)
- [ ] New vulnerabilities are correlated with affected packages
- [ ] Resolved vulnerabilities are identified correctly
- [ ] License changes between package versions are detected
- [ ] Returns appropriate error when either SBOM ID does not exist

## Test Requirements
- [ ] Unit test: compare two SBOMs with known package differences, verify all six diff categories
- [ ] Unit test: compare identical SBOMs, verify all diff categories are empty
- [ ] Unit test: compare with non-existent SBOM ID returns error
- [ ] Performance: verify comparison completes in <1s for 2000 packages per SBOM (if benchmarking infrastructure exists)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Backend comparison model
