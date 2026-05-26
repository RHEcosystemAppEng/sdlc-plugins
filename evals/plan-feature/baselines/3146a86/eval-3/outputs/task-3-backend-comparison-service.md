# Task 3 — Add SBOM comparison service logic

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the comparison logic in `SbomService` that computes the structured diff between two SBOMs. The service method loads the package lists and advisory associations for both SBOMs, then computes the six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. The diff is computed on-the-fly from existing data — no new database tables are required.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `compare(left_id, right_id)` method to `SbomService`
- `modules/fundamental/src/sbom/service/mod.rs` — update if needed for new imports

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` — the `SbomService` already has `fetch` and `list` methods. Add a `compare` method that accepts two SBOM IDs and a database connection/transaction.
- Per the backend key conventions (Error handling): all handlers return `Result<T, AppError>` with `.context()` wrapping. The compare method should return `Result<SbomComparisonResult, AppError>`.
- Per the non-functional requirements: comparison must achieve p95 < 1s for SBOMs with up to 2000 packages each. Load package lists for both SBOMs in parallel where possible, and use `HashMap` for O(1) lookups during diff computation rather than nested iteration.
- Per constraint 5.4: reuse existing query patterns from `common/src/db/query.rs` for loading packages. Use the existing `PackageService` and `AdvisoryService` for loading related data.
- Algorithm outline:
  1. Load packages for left SBOM (via `sbom_package` join entity) and right SBOM
  2. Build `HashMap<package_name, PackageInfo>` for both sides
  3. Compute added packages (in right, not in left)
  4. Compute removed packages (in left, not in right)
  5. Compute version changes (in both, different version)
  6. Load advisories for both SBOMs (via `sbom_advisory` join entity)
  7. Compute new vulnerabilities (advisory affects right but not left)
  8. Compute resolved vulnerabilities (advisory affects left but not right)
  9. Compute license changes (same package, different license)
- No new database tables per the non-functional requirements — compute everything on-the-fly from `sbom_package`, `package`, `sbom_advisory`, `advisory`, and `package_license` entities.
- Per constraint 5.2: inspect the existing entity definitions in `entity/src/` before implementing to confirm the exact field names and relationships.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — the existing service struct to extend with `compare` method
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — for loading advisory details by SBOM
- `modules/fundamental/src/package/service/mod.rs::PackageService` — for loading package details
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for loading package lists per SBOM
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity for loading advisories per SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for detecting license changes
- `common/src/db/query.rs` — shared query builder helpers for database queries

## Acceptance Criteria
- [ ] `SbomService::compare(left_id, right_id)` method is implemented and returns `Result<SbomComparisonResult, AppError>`
- [ ] Added packages are correctly computed (packages in right SBOM but not in left)
- [ ] Removed packages are correctly computed (packages in left SBOM but not in right)
- [ ] Version changes are correctly computed with upgrade/downgrade direction
- [ ] New vulnerabilities are correctly computed (advisories affecting right but not left)
- [ ] Resolved vulnerabilities are correctly computed (advisories affecting left but not right)
- [ ] License changes are correctly computed (same package with different license between SBOMs)
- [ ] Error handling returns appropriate errors for non-existent SBOM IDs

## Test Requirements
- [ ] Integration test: compare two SBOMs with known differences and verify all six diff categories produce correct results
- [ ] Integration test: compare two identical SBOMs and verify all diff categories are empty
- [ ] Integration test: compare with non-existent SBOM ID returns an appropriate error
- [ ] Integration test: verify performance is acceptable with SBOMs containing a realistic number of packages (boundary case for the 2000-package requirement)

## Verification Commands
- `cargo test --package trustify-fundamental -- sbom::service::compare` — run comparison service tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 2 — Add SBOM comparison model structs
