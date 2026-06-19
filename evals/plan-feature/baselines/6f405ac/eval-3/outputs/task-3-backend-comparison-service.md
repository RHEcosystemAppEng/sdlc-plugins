## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the comparison service logic that loads two SBOMs by ID, computes the structured diff (added/removed packages, version changes, new/resolved vulnerabilities, license changes), and returns an `SbomComparison` result. This is the core business logic for the SBOM comparison feature, consumed by the endpoint handler in task 4.

## Files to Create
- `modules/fundamental/src/sbom/service/compare.rs` — Comparison logic as a method on SbomService

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` re-export

## Implementation Notes
Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` — the `SbomService` struct provides methods that accept a database connection and return `Result<T, AppError>`.

Add a `compare` method to `SbomService` that:
1. Fetches both SBOMs by ID using existing `SbomService` fetch logic in `modules/fundamental/src/sbom/service/sbom.rs`
2. Fetches packages for each SBOM using `PackageService` from `modules/fundamental/src/package/service/mod.rs`
3. Fetches advisories for each SBOM using `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs`
4. Computes the diff:
   - Added packages: in right but not in left (match by package name)
   - Removed packages: in left but not in right
   - Version changes: in both but with different versions; determine direction (upgrade vs downgrade)
   - New vulnerabilities: advisories linked to right SBOM but not left
   - Resolved vulnerabilities: advisories linked to left SBOM but not right
   - License changes: packages in both with different license values
5. Returns `SbomComparison` (from task 2)

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Module pattern: follow model/ + service/ + endpoints/ structure. Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list methods to load SBOM data
- `modules/fundamental/src/package/service/mod.rs::PackageService` — fetch packages for an SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — fetch advisories linked to an SBOM
- `common/src/error.rs::AppError` — error type for Result returns with `.context()` wrapping
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for querying advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for license comparison

## Dependencies
- Depends on: Task 2 — Backend comparison models (uses `SbomComparison` and related structs)

## Acceptance Criteria
- [ ] `SbomService::compare(left_id, right_id)` method implemented in `compare.rs`
- [ ] Method correctly identifies added packages (in right, not in left)
- [ ] Method correctly identifies removed packages (in left, not in right)
- [ ] Method correctly identifies version changes with upgrade/downgrade direction
- [ ] Method correctly identifies new vulnerabilities (advisories in right, not in left)
- [ ] Method correctly identifies resolved vulnerabilities (advisories in left, not in right)
- [ ] Method correctly identifies license changes
- [ ] Method returns `Result<SbomComparison, AppError>` with proper error context
- [ ] Returns appropriate error when either SBOM ID is not found

## Test Requirements
- [ ] Unit test: two SBOMs with no differences returns empty diff sections
- [ ] Unit test: added packages are correctly detected
- [ ] Unit test: removed packages are correctly detected
- [ ] Unit test: version changes are detected with correct direction (upgrade vs downgrade)
- [ ] Unit test: new vulnerabilities are correctly identified
- [ ] Unit test: resolved vulnerabilities are correctly identified
- [ ] Unit test: license changes are detected
- [ ] Unit test: non-existent SBOM ID returns an error
