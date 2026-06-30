## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the comparison diffing logic to `SbomService` that computes a structured diff between two SBOMs. The service fetches packages, advisories, and licenses for both SBOMs and produces an `SbomComparisonResult` with all six diff categories. The diff is computed on-the-fly from existing data (no new database tables per the non-functional requirements).

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `compare` method to `SbomService` that takes two SBOM IDs and returns `Result<SbomComparisonResult, AppError>`

## Implementation Notes
- The `compare` method should:
  1. Fetch both SBOMs by ID using the existing `fetch` method pattern in `sbom.rs`
  2. Return an error if either SBOM does not exist (`AppError::NotFound`)
  3. Fetch packages for each SBOM using `PackageService` (see `modules/fundamental/src/package/service/mod.rs`)
  4. Compute added packages (in right but not left), removed packages (in left but not right), and version changes (same package name, different version) by comparing the package sets
  5. Fetch advisories for each SBOM using `AdvisoryService` (see `modules/fundamental/src/advisory/service/advisory.rs`)
  6. Compute new vulnerabilities (advisories affecting right but not left) and resolved vulnerabilities (advisories affecting left but not right) by comparing advisory sets
  7. Compute license changes by comparing the license field of packages present in both SBOMs
  8. Determine version change direction: compare semver strings to classify as "upgrade" or "downgrade"
- Follow the error handling pattern from existing service methods: use `Result<T, AppError>` with `.context()` wrapping per `common/src/error.rs`.
- Query helpers in `common/src/db/query.rs` can be used for any database lookups that require filtering or pagination.
- Performance requirement: p95 < 1s for SBOMs with up to 2000 packages each. Consider using `HashMap` for O(1) package lookups during diff computation instead of nested iteration.
- Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service methods demonstrate the fetch-and-transform pattern to follow
- `modules/fundamental/src/package/service/mod.rs::PackageService` — provides package list fetching for each SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — provides advisory list fetching for each SBOM
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error enum for consistent error handling

## Acceptance Criteria
- [ ] `SbomService::compare` method accepts two SBOM IDs and returns `SbomComparisonResult`
- [ ] Returns `AppError::NotFound` when either SBOM ID does not exist
- [ ] Correctly computes added packages (present in right, absent in left)
- [ ] Correctly computes removed packages (present in left, absent in right)
- [ ] Correctly computes version changes with upgrade/downgrade direction
- [ ] Correctly computes new vulnerabilities (advisories in right, not in left)
- [ ] Correctly computes resolved vulnerabilities (advisories in left, not in right)
- [ ] Correctly computes license changes for packages present in both SBOMs
- [ ] Diff computation completes within p95 < 1s for SBOMs with up to 2000 packages each

## Test Requirements
- [ ] Unit test: compare two SBOMs with known package differences — verify added/removed/changed counts
- [ ] Unit test: compare two identical SBOMs — verify all diff sections are empty
- [ ] Unit test: compare with non-existent SBOM ID — verify NotFound error
- [ ] Unit test: compare SBOMs with vulnerability differences — verify new/resolved classification
- [ ] Unit test: compare SBOMs with license changes — verify correct detection

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add comparison model structs

<!-- [sdlc-workflow] Description digest: sha256-md:ec3a694b6575e8730228175aa4e2e3205454c23617715bb11979643ffe53fe5d -->
