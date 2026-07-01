## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add a comparison method to SbomService that computes a structured diff between two SBOMs. The method fetches the package sets, advisory associations, and license mappings for both SBOMs, then computes the symmetric difference to produce added/removed packages, version changes, new/resolved vulnerabilities, and license changes.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare(left_id, right_id)` method to `SbomService`
- `modules/fundamental/src/sbom/service/mod.rs` — ensure comparison-related imports are available

## Implementation Notes
- The `compare` method should accept two SBOM IDs (UUID or the existing SBOM ID type) and return `Result<SbomComparisonResult, AppError>`.
- Use the existing `SbomService` methods (`fetch`, `list`) as reference for database access patterns and error handling with `.context()` wrapping.
- Compute the diff on-the-fly (no new database tables per the non-functional requirements):
  1. Fetch packages for both SBOMs using `PackageService` or direct entity queries on `sbom_package` join table.
  2. Build hash maps keyed by package name for O(n) comparison.
  3. Added packages: in right but not in left. Removed packages: in left but not in right.
  4. Version changes: packages in both but with different version strings. Determine direction by comparing version strings (lexicographic or semver if available).
  5. For vulnerability diff: query `sbom_advisory` join table for both SBOMs, diff the advisory sets. Use `AdvisoryService` patterns for fetching advisory details (severity, title).
  6. For license changes: compare the license field on packages present in both SBOMs.
- Follow the query pattern in `common/src/db/query.rs` for any database queries.
- Wrap all database errors with `AppError` using `.context()` per `common/src/error.rs`.
- Target p95 < 1s for SBOMs with up to 2000 packages each — use batch queries rather than N+1 patterns.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with database access patterns to follow
- `modules/fundamental/src/package/service/mod.rs::PackageService` — package querying methods for fetching package lists per SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — advisory fetching patterns for building vulnerability diffs
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying packages by SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for querying advisories by SBOM

## Acceptance Criteria
- [ ] `SbomService::compare(left_id, right_id)` method exists and returns `Result<SbomComparisonResult, AppError>`
- [ ] Added and removed packages are correctly computed as set differences
- [ ] Version changes are detected for packages present in both SBOMs with different versions
- [ ] New and resolved vulnerabilities are computed by diffing advisory associations
- [ ] License changes are detected for packages present in both SBOMs with different licenses
- [ ] Errors (e.g., non-existent SBOM ID) are wrapped with `AppError` and return appropriate error responses

## Test Requirements
- [ ] Unit test: compare two SBOMs where the right has an additional package — verify it appears in `added_packages`
- [ ] Unit test: compare two SBOMs where a package was removed — verify it appears in `removed_packages`
- [ ] Unit test: compare two SBOMs where a package version changed — verify `version_changes` includes correct left/right versions and direction
- [ ] Unit test: compare two identical SBOMs — verify all diff categories are empty
- [ ] Unit test: non-existent SBOM ID returns an appropriate error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison response model types

## Description Digest
sha256-md:a187583a5609c65e7068ec88e866e71ddeaa53f0b530d089851223a14d5c8fd8
