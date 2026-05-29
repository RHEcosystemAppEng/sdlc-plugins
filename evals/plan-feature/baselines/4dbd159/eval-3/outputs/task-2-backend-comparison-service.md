# Task 2 — Add SBOM comparison service logic

## Repository
trustify-backend

## Target Branch
main

## Description
Add a comparison method to the SBOM service that computes an on-the-fly diff between two SBOMs. The method fetches package lists, advisory associations, and license data for both SBOMs from existing database entities and computes six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. No new database tables are required — all data is derived from existing entities.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `compare(left_id, right_id) -> Result<SbomComparisonResult, AppError>` method to `SbomService`

## Implementation Notes
- Follow the existing service method pattern in `modules/fundamental/src/sbom/service/sbom.rs` — methods take a database connection/pool reference and return `Result<T, AppError>` with `.context()` wrapping on errors.
- The comparison must be computed on-the-fly without new database tables per the non-functional requirements.
- **Algorithm outline:**
  1. Fetch packages for left SBOM via `sbom_package` join table and `package` entity
  2. Fetch packages for right SBOM via the same join
  3. Build HashMaps keyed by package name for O(n) lookup
  4. Compute set differences: added = in right but not left, removed = in left but not right
  5. For packages in both: compare versions (detect upgrades/downgrades) and licenses (detect changes)
  6. Fetch advisories for both SBOMs via `sbom_advisory` join table and `advisory` entity
  7. Compute advisory differences: new vulnerabilities = advisories in right but not left, resolved = in left but not right
- **Performance requirement:** p95 < 1s for SBOMs with up to 2000 packages each. Use batch queries (not N+1) when fetching packages and advisories.
- Version direction detection: compare versions using semantic versioning where possible. If versions are not semver-compliant, fall back to string comparison and default to `Upgrade` for differing versions.
- Use the `PackageSummary` license field from `modules/fundamental/src/package/model/summary.rs` for license data.
- Use the `AdvisorySummary` severity field from `modules/fundamental/src/advisory/model/summary.rs` for vulnerability severity.
- Both SBOMs must exist; return `AppError::NotFound` if either ID is invalid.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Extend with the new compare method, following the existing fetch/list method patterns
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Reference for package querying patterns
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Reference for advisory querying patterns
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — Error handling enum with `IntoResponse` implementation
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for querying advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for license data

## Acceptance Criteria
- [ ] `SbomService::compare(left_id, right_id)` method exists and returns `Result<SbomComparisonResult, AppError>`
- [ ] Added packages are correctly identified (in right SBOM but not in left)
- [ ] Removed packages are correctly identified (in left SBOM but not in right)
- [ ] Version changes are detected with correct upgrade/downgrade direction
- [ ] New vulnerabilities are identified (advisories in right but not left)
- [ ] Resolved vulnerabilities are identified (advisories in left but not right)
- [ ] License changes are detected for packages present in both SBOMs
- [ ] Returns `AppError::NotFound` when either SBOM ID does not exist
- [ ] Queries use batch fetching, not N+1 patterns

## Test Requirements
- [ ] Test comparison with two SBOMs that have added, removed, and changed packages
- [ ] Test comparison with new and resolved vulnerabilities
- [ ] Test comparison with license changes
- [ ] Test comparison where one SBOM ID does not exist (expect NotFound error)
- [ ] Test comparison of two identical SBOMs (expect empty diff categories)
- [ ] Test that version direction is correctly classified as upgrade or downgrade

## Verification Commands
- `cargo build -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental compare` — service tests pass

## Dependencies
- Depends on: Task 1 — Add SBOM comparison model structs
