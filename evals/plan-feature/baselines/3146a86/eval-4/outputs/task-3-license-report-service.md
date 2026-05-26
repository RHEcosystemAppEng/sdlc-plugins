# Task 3 — Implement license report service with transitive dependency resolution

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the `LicenseReportService` that generates a license compliance report for a given SBOM. The service aggregates package-license data from existing entities (`package_license`, `sbom_package`, `package`), walks the full dependency tree to include transitive dependencies, groups packages by license, and evaluates each group's compliance against the configured license policy.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with a `generate(sbom_id, db, policy) -> Result<LicenseReport, AppError>` method. Queries the database for all packages linked to the SBOM (direct and transitive), joins with `package_license` to get license data, groups by license, and checks compliance using `LicensePolicy::check_license`.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module.

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` — see `SbomService` for how services accept a database connection, use SeaORM queries, and return `Result<T, AppError>`.
- Use SeaORM to query the existing `sbom_package`, `package`, and `package_license` entities from `entity/src/`. Do NOT create new database tables — the feature requirement explicitly states "no new database tables."
- For transitive dependency resolution: query `sbom_package` for the given SBOM ID to get direct packages, then recursively resolve dependencies. The exact mechanism depends on how the dependency graph is stored — inspect the `sbom_package` entity (`entity/src/sbom_package.rs`) and the SBOM ingestion code (`modules/ingestor/src/graph/sbom/mod.rs`) to understand the dependency graph structure.
- Use `.context()` wrapping on all fallible operations, per the error handling pattern in `common/src/error.rs::AppError`.
- Use `common/src/db/query.rs` query helpers if applicable for building the aggregation queries.
- Performance: the p95 target is < 500ms for SBOMs with up to 1000 packages. Consider using a single query with JOINs rather than N+1 queries. If the dependency tree is stored as a flat list per SBOM (rather than a graph), a single JOIN query should suffice.
- Per docs/constraints.md §5.2: inspect existing code before implementing. Review `SbomService` methods for data-fetching patterns.
- Per docs/constraints.md §5.4: do not duplicate existing functionality. Check if `PackageService` in `modules/fundamental/src/package/service/mod.rs` already has methods for fetching packages by SBOM that can be reused.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing service pattern to follow for database queries and error handling.
- `modules/fundamental/src/package/service/mod.rs::PackageService` — may have existing methods for fetching packages associated with an SBOM.
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination.
- `entity/src/sbom_package.rs` — SBOM-Package join table entity defining the relationship between SBOMs and packages.
- `entity/src/package_license.rs` — Package-License mapping entity needed for license data aggregation.
- `common/src/error.rs::AppError` — error handling pattern with `.context()` wrapping.

## Acceptance Criteria
- [ ] `LicenseReportService::generate` returns a `LicenseReport` with packages grouped by license
- [ ] Each `LicenseGroup` has a `compliant` flag set by evaluating the license against the loaded policy
- [ ] Transitive dependencies are included in the report (not just direct dependencies)
- [ ] Packages with no license data are handled gracefully (e.g., grouped under "Unknown" or similar)
- [ ] The service does not create any new database tables — only reads from existing entities
- [ ] Querying a nonexistent SBOM ID returns an appropriate error

## Test Requirements
- [ ] Unit/integration test: generate a report for an SBOM with packages under different licenses and verify correct grouping
- [ ] Unit/integration test: verify that transitive dependencies appear in the report with the `transitive` flag set
- [ ] Unit/integration test: verify compliance flags match the policy (allowed license -> compliant: true, denied license -> compliant: false)
- [ ] Unit/integration test: verify behavior when an SBOM has no packages (empty report)
- [ ] Unit/integration test: verify error handling for nonexistent SBOM ID

## Dependencies
- Depends on: Task 1 — Add license policy configuration model and loader
- Depends on: Task 2 — Add license report response model
