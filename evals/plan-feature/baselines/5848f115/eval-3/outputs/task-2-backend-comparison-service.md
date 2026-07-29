## Repository
trustify-backend

## Target Branch
main

## Description
Add a comparison method to SbomService that computes a structured diff between two SBOMs. The method queries existing package, advisory, and license data from the database to produce the SbomComparisonResult without creating any new database tables — all computation is performed on-the-fly from existing entity data.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add `compare(left_id, right_id) -> Result<SbomComparisonResult, AppError>` method to SbomService

## Implementation Notes
- Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService: fetch, list, ingest).
- The comparison method should:
  1. Fetch packages for both SBOMs using the `sbom_package` join table (`entity/src/sbom_package.rs`)
  2. Compute set differences for added/removed packages by comparing package lists
  3. Detect version changes by matching packages present in both SBOMs by name but with different versions
  4. Determine upgrade vs downgrade direction using semantic version comparison (consider using the `semver` crate if available, or simple string comparison as fallback)
  5. Query advisories linked to each SBOM via the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find new and resolved vulnerabilities
  6. Query license information from the `package_license` mapping (`entity/src/package_license.rs`) to detect license changes
- Return type must be `Result<SbomComparisonResult, AppError>` following the error handling convention where all handlers return `Result<T, AppError>` with `.context()` wrapping.
- Use the shared query builder helpers from `common/src/db/query.rs` for any database queries.
- NFR: response time p95 < 1s for SBOMs with up to 2000 packages each. Consider batch-loading packages rather than N+1 queries.
- No new database tables — the requirement explicitly states compute diff on-the-fly from existing data.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service with fetch/list methods showing the established service pattern and error handling
- `modules/fundamental/src/package/service/mod.rs::PackageService` — PackageService fetch/list methods for querying package data
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — AdvisoryService fetch/list/search for querying advisory data
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying packages per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for querying advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for license data

## Acceptance Criteria
- [ ] `SbomService::compare(left_id, right_id)` method exists and returns `Result<SbomComparisonResult, AppError>`
- [ ] Added packages are correctly identified (present in right SBOM but not left)
- [ ] Removed packages are correctly identified (present in left SBOM but not right)
- [ ] Version changes are correctly detected with upgrade/downgrade direction
- [ ] New vulnerabilities are identified (advisories affecting right SBOM but not left)
- [ ] Resolved vulnerabilities are identified (advisories affecting left SBOM but not right)
- [ ] License changes are detected for packages present in both SBOMs with different licenses
- [ ] Method handles the case where either SBOM ID is invalid (returns appropriate error)
- [ ] No new database tables or migrations are introduced

## Test Requirements
- [ ] Test comparison with two SBOMs that have distinct package sets (verifies added/removed detection)
- [ ] Test comparison with overlapping packages at different versions (verifies version change and direction detection)
- [ ] Test comparison with advisory differences (verifies new/resolved vulnerability detection)
- [ ] Test comparison with license changes (verifies license change detection)
- [ ] Test comparison with identical SBOMs (all diff sections should be empty)
- [ ] Test error handling when an invalid SBOM ID is provided
- [ ] Test performance with large package sets (up to 2000 packages per SBOM) does not regress p95 latency

## Verification Commands
- `cargo build -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental` — all tests pass

## Dependencies
- Depends on: Task 1 — Backend comparison models (SbomComparisonResult and related structs must exist)
