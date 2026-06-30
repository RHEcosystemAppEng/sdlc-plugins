## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the `SbomComparisonService` that computes the structured diff between two SBOMs. The service loads package and advisory data for both SBOMs using existing services, then computes added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The diff is computed on-the-fly with no new database tables, as specified in the non-functional requirements.

## Files to Create
- `modules/fundamental/src/sbom/service/comparison.rs` — `SbomComparisonService` with a `compare(left_id, right_id, db) -> Result<SbomComparison, AppError>` method

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod comparison;` to expose the comparison service

## Implementation Notes
Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs`. The comparison service should:

1. Use `SbomService` to fetch both SBOMs by ID, returning `AppError::NotFound` if either does not exist
2. Use `PackageService` from `modules/fundamental/src/package/service/mod.rs` to load packages for each SBOM
3. Use `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs` to load advisories linked to each SBOM
4. Compute set differences using `HashMap` keyed by package name:
   - Added packages: in right but not left
   - Removed packages: in left but not right
   - Version changes: in both but with different versions; compute direction by comparing version strings
   - License changes: in both but with different license values
5. For vulnerability diff, compare advisory sets linked to each SBOM's packages
6. Return `SbomComparison` populated with all diff categories

Use `common/src/db/query.rs` for any query builder helpers needed. Wrap all database errors with `.context()` per the error handling convention.

Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `modules/fundamental/src/sbom/service/comparison.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Module pattern: place service logic under `service/` within the sbom module directory.
Applies: task creates `modules/fundamental/src/sbom/service/comparison.rs` matching the convention's `service/` directory scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — fetch SBOM by ID, list packages for an SBOM
- `modules/fundamental/src/package/service/mod.rs::PackageService` — load package details including license
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — load advisories and severity data
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` — error enum for consistent error handling

## Acceptance Criteria
- [ ] `SbomComparisonService::compare()` loads packages and advisories for both SBOMs
- [ ] Correctly computes added, removed, version-changed, and license-changed packages
- [ ] Correctly computes new and resolved vulnerabilities
- [ ] Returns `AppError::NotFound` if either SBOM ID does not exist
- [ ] All database errors are wrapped with `.context()`
- [ ] Service compiles: `cargo check -p trustify-module-fundamental`

## Test Requirements
- [ ] Unit test: compare two SBOMs with known package sets, verify all diff categories
- [ ] Unit test: compare identical SBOMs, verify all diff fields are empty vectors
- [ ] Unit test: compare with non-existent SBOM ID returns appropriate error

## Verification Commands
- `cargo check -p trustify-module-fundamental` — compiles without errors
- `cargo test -p trustify-module-fundamental -- comparison` — service tests pass

## Dependencies
- Depends on: Task 1 — create-branch
- Depends on: Task 2 — backend-comparison-model

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Critical"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}

[sdlc-workflow] Description digest: sha256-md:42ecc8712b80fda1e7ecb00679bc53fc574b3f05ff47dcdfb87d0aa8596372f9
