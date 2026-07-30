## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report service that generates a license compliance report for a given SBOM. The service aggregates all packages associated with the SBOM (including transitive dependencies), groups them by license type, and checks each group against the license policy configuration (from Task 1) to flag non-compliant licenses. The service must meet the p95 < 500ms performance target for SBOMs with up to 1000 packages.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — Response models: `LicenseReport` struct containing a `groups` field (Vec of `LicenseGroup`); `LicenseGroup` struct with `license: String`, `packages: Vec<PackageLicenseEntry>`, and `compliant: bool` fields; `PackageLicenseEntry` struct with package name, version, and purl fields
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with a `generate_report(sbom_id: Uuid, db: &DatabaseConnection) -> Result<LicenseReport, AppError>` method

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new model module
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module
- `modules/fundamental/src/sbom/mod.rs` — Re-export license report types if needed

## Implementation Notes
- Use the existing `package_license` entity (`entity/src/package_license.rs`) to query package-license mappings — this is the authoritative source for license data
- Walk transitive dependencies by joining through `sbom_package` (`entity/src/sbom_package.rs`) to resolve the full dependency tree for the given SBOM
- Use `PackageSummary` (`modules/fundamental/src/package/model/summary.rs`) which already includes a `license` field — leverage this existing field rather than re-querying
- Load the `LicensePolicy` from Task 1 to evaluate compliance for each license group
- No new database tables are required — aggregate from existing package-license data per the NFR
- Optimize queries for the p95 < 500ms target: use a single query with JOINs rather than N+1 queries; consider using SeaORM's `find_with_related` or raw query builder for the aggregation
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for method signatures and error handling
- Per docs/constraints.md section 5 (Code Change Rules): changes must be scoped to listed files; inspect code before modifying; follow patterns in Implementation Notes
- Per CONVENTIONS.md -- Module pattern: follow the model/ + service/ + endpoints/ structure. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` service file scope.
- Per CONVENTIONS.md -- Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md -- Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs` where applicable. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` service file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — established service pattern for SBOM operations (method signatures, database connection handling, error wrapping)
- `modules/fundamental/src/package/service/mod.rs::PackageService` — package query patterns and license field access
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/src/package_license.rs` — existing Package-License mapping entity for license data queries
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for resolving package relationships

## Acceptance Criteria
- [ ] `generate_report` returns a `LicenseReport` with packages grouped by license type
- [ ] Each `LicenseGroup` has a `compliant` flag evaluated against the license policy
- [ ] Transitive dependencies are included in the report (full dependency tree walk)
- [ ] Report generation completes within 500ms for SBOMs with up to 1000 packages
- [ ] No new database tables are created — only existing entities are queried

## Test Requirements
- [ ] Unit test: report correctly groups packages by license type
- [ ] Unit test: compliance flags match the configured license policy
- [ ] Unit test: transitive dependencies are included in grouping
- [ ] Unit test: empty SBOM (no packages) returns an empty groups array
- [ ] Unit test: SBOM with all compliant licenses returns all groups as compliant
- [ ] Unit test: SBOM with mixed compliance returns correct flags per group

## Dependencies
- Depends on: Task 1 — Add license policy configuration model
