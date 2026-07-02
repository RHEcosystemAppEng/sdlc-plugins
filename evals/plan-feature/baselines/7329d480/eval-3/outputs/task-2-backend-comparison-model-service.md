## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the comparison response model and diff computation service for SBOM comparison. This introduces the data structures that represent a structured diff between two SBOMs and the service logic that queries existing package, advisory, and license data to compute that diff on the fly (no new database tables).

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — SbomComparison response struct containing AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, and LicenseChange sub-structs with Serialize derives
- `modules/fundamental/src/sbom/service/compare.rs` — compare method on SbomService that accepts two SBOM IDs, loads their packages and advisories via SeaORM joins on sbom_package/sbom_advisory, and computes set differences

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — add `pub mod comparison;` to re-export comparison types
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod compare;` to re-export compare service

## Implementation Notes
Follow the existing module pattern: model structs in `model/comparison.rs`, service logic in `service/compare.rs`.

The SbomComparison struct mirrors the API response shape:
- `added_packages`: Vec of packages in right SBOM but not left (join sbom_package for each, diff by package ID)
- `removed_packages`: Vec of packages in left SBOM but not right
- `version_changes`: Vec of packages present in both but with different versions
- `new_vulnerabilities`: Vec of advisories linked to right SBOM packages but not left (join sbom_advisory)
- `resolved_vulnerabilities`: Vec of advisories linked to left SBOM packages but not right
- `license_changes`: Vec of packages whose license field differs between left and right (query package_license entity)

Reuse existing entity relationships:
- `entity/src/sbom_package.rs` for SBOM-to-package joins
- `entity/src/sbom_advisory.rs` for SBOM-to-advisory joins
- `entity/src/package_license.rs` for license lookups

The service method signature should be:
```rust
pub async fn compare(&self, db: &DbConn, left_id: Uuid, right_id: Uuid) -> Result<SbomComparison, AppError>
```

Use `common/src/db/query.rs` helpers for constructing database queries.

Per CONVENTIONS.md §Module pattern: follow model/ + service/ + endpoints/ structure. Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` and `modules/fundamental/src/sbom/service/compare.rs` matching the convention's Rust module scope.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping on fallible operations. Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Framework: use SeaORM for database queries against sbom_package, sbom_advisory, and package_license entities. Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — reference for struct patterns and serde attributes
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — extend with compare method following existing fetch/list patterns
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — package fields (name, version, license) to mirror in comparison sub-structs
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — advisory fields (id, severity, title) to mirror in vulnerability sub-structs
- `common/src/error.rs::AppError` — error type for service method return
- `common/src/db/query.rs` — query builder helpers for filtering and joins

## Acceptance Criteria
- [ ] `SbomComparison` struct serializes to the expected JSON shape with all six diff categories
- [ ] Compare service correctly identifies added packages (present in right, absent in left)
- [ ] Compare service correctly identifies removed packages (present in left, absent in right)
- [ ] Compare service correctly identifies version changes (same package, different versions)
- [ ] Compare service correctly identifies new vulnerabilities (advisories affecting right but not left)
- [ ] Compare service correctly identifies resolved vulnerabilities (advisories affecting left but not right)
- [ ] Compare service correctly identifies license changes (same package, different license)
- [ ] Service returns `AppError` with appropriate context when either SBOM ID is not found

## Test Requirements
- [ ] Unit test: compare two SBOMs with known package differences produces correct added/removed/changed sets
- [ ] Unit test: compare two identical SBOMs produces empty diff across all categories
- [ ] Unit test: compare with non-existent SBOM ID returns appropriate error

## Dependencies
- Depends on: Task 1 — Create feature branch (create-branch bookend)
