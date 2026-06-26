## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the SBOM comparison service that computes a structured diff between two SBOMs. The service loads package and advisory data for both SBOMs from the database and computes added/removed packages, version changes, new/resolved vulnerabilities, and license changes. The diff is computed on-the-fly with no new database tables, per the non-functional requirements.

## Files to Create
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomCompareService` with a `compare(left_id, right_id, db) -> Result<SbomComparison, AppError>` method

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to expose the comparison service module

## Implementation Notes
Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`). The comparison logic should:

1. Use `SbomService` from `modules/fundamental/src/sbom/service/sbom.rs` to fetch both SBOM details by ID. Return `AppError::NotFound` if either SBOM does not exist.
2. Use `PackageService` from `modules/fundamental/src/package/service/mod.rs` to load packages for each SBOM.
3. Use `AdvisoryService` from `modules/fundamental/src/advisory/service/advisory.rs` to load advisories linked to each SBOM.
4. Compute the diff:
   - **Added packages**: packages in right but not in left (match by package name)
   - **Removed packages**: packages in left but not in right
   - **Version changes**: packages in both but with different versions; determine direction by comparing version strings
   - **New vulnerabilities**: advisories linked to right SBOM packages but not linked to left SBOM packages
   - **Resolved vulnerabilities**: advisories linked to left SBOM packages but not linked to right SBOM packages
   - **License changes**: packages in both SBOMs where the license field differs
5. Use `HashMap` for O(n) set-difference operations to meet the p95 < 1s performance requirement for SBOMs with up to 2000 packages each.

Error handling: wrap all database calls with `.context()` per the pattern in `common/src/error.rs` (`AppError`).

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — fetch SBOM details by ID
- `modules/fundamental/src/package/service/mod.rs::PackageService` — load packages for an SBOM
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — load advisories for SBOM packages
- `common/src/error.rs::AppError` — error handling with `.context()` wrapping
- `modules/fundamental/src/sbom/model/comparison.rs::SbomComparison` — return type (from Task 2)

## Acceptance Criteria
- [ ] `compare()` method returns a correctly structured `SbomComparison` for two valid SBOM IDs
- [ ] Returns `AppError::NotFound` when either SBOM ID does not exist
- [ ] Added/removed package detection is correct based on package name matching
- [ ] Version changes correctly identify upgrade vs. downgrade direction
- [ ] New and resolved vulnerabilities are correctly computed from advisory linkage
- [ ] License changes are detected when the same package has different licenses
- [ ] Diff computation uses O(n) algorithms (HashMap-based set operations)

## Test Requirements
- [ ] Unit test: comparing an SBOM with itself produces empty diff (all sections have zero items)
- [ ] Unit test: added and removed packages are correctly identified
- [ ] Unit test: version changes detect upgrade and downgrade correctly
- [ ] Unit test: new and resolved vulnerabilities are correctly categorized
- [ ] Unit test: license changes are detected
- [ ] Unit test: non-existent SBOM ID returns NotFound error

## Verification Commands
- `cargo build -p trustify-fundamental` — compiles without errors
- `cargo test -p trustify-fundamental compare` — service tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch
- Depends on: Task 2 — Backend comparison model structs

[sdlc-workflow] Description digest: sha256-md:ddd5bd3897035a0af573f8b19aae58c4c0855712f60dff82a2c8a78934132d05
