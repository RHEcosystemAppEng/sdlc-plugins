## Repository
trustify-backend

## Target Branch
main

## Description
Implement the SBOM comparison service that computes a structured diff between two SBOMs. The service fetches package lists and advisory associations for both SBOMs, then computes set differences for each diff category: added/removed packages, version changes, new/resolved vulnerabilities, and license changes. This logic is separated from the endpoint layer to enable unit testing and potential reuse.

## Files to Create
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomComparisonService` with a `compare(db, left_id, right_id) -> Result<SbomComparisonResult, AppError>` method

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to export the comparison service module

## Implementation Notes
Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs`. The compare method should:

1. Use `SbomService` from `modules/fundamental/src/sbom/service/sbom.rs` to fetch both SBOMs and validate they exist (return 404 AppError if not found, following the pattern in `common/src/error.rs`).
2. Query packages for each SBOM using `PackageService` from `modules/fundamental/src/package/service/mod.rs` with the SBOM ID filter.
3. Query advisories for each SBOM using `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs`.
4. Compute set differences by package name to populate `added_packages`, `removed_packages`.
5. For packages present in both, compare version strings to populate `version_changes` with direction detection (compare semver where possible, fall back to string comparison).
6. Diff advisory sets by advisory ID to populate `new_vulnerabilities` and `resolved_vulnerabilities`.
7. Diff license fields for packages present in both to populate `license_changes`.

Use `common/src/db/query.rs` query helpers for database access. Wrap database errors with `.context()` per the error handling convention in `common/src/error.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Fetch SBOM details by ID
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Fetch packages for an SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Fetch advisories for an SBOM
- `common/src/db/query.rs` — Shared query builder helpers for filtering
- `common/src/error.rs::AppError` — Error type with context wrapping

## Acceptance Criteria
- [ ] `SbomComparisonService::compare()` returns `Result<SbomComparisonResult, AppError>`
- [ ] Returns 404 AppError when either SBOM ID does not exist
- [ ] Correctly identifies added packages (in right but not left)
- [ ] Correctly identifies removed packages (in left but not right)
- [ ] Correctly identifies version changes with upgrade/downgrade direction
- [ ] Correctly identifies new vulnerabilities (advisories in right but not left)
- [ ] Correctly identifies resolved vulnerabilities (advisories in left but not right)
- [ ] Correctly identifies license changes for packages present in both SBOMs
- [ ] Performance: handles SBOMs with up to 2000 packages each within p95 < 1s

## Test Requirements
- [ ] Unit test: comparison of two identical SBOMs returns empty diff in all categories
- [ ] Unit test: comparison with added/removed packages populates correct categories
- [ ] Unit test: comparison with version changes detects upgrade vs downgrade
- [ ] Unit test: comparison with differing advisories populates vulnerability categories
- [ ] Unit test: comparison with license changes populates license_changes
- [ ] Unit test: non-existent SBOM ID returns 404 error

## Verification Commands
- `cargo check -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental -- compare` — service tests pass

## Dependencies
- Depends on: Task 1 — Backend SBOM comparison model types
