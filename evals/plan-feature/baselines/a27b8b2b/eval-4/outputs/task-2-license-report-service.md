## Repository
trustify-backend

## Target Branch
main

## Description
Add a license report service that aggregates package license data from the existing `package_license` entity, walks transitive SBOM dependencies via the `sbom_package` join table, groups packages by license type, and evaluates compliance against the configurable license policy introduced in Task 1.

The service must handle SBOMs with up to 1000 packages within a p95 latency target of 500ms. No new database tables are created — all data is aggregated from existing `package_license` and `sbom_package` entities.

## Files to Create
- `modules/fundamental/src/sbom/license_report/service.rs` — `LicenseReportService` with a method to generate a `LicenseReport` for a given SBOM ID

## Files to Modify
- `modules/fundamental/src/sbom/license_report/mod.rs` — Add `pub mod service;` to register the service module

## API Changes
- `LicenseReportService::generate_report(sbom_id, db, policy) -> Result<LicenseReport, AppError>` — NEW: generates a license compliance report for the given SBOM

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) for database interaction patterns, error handling with `.context()`, and connection pool usage.
- Query the `sbom_package` entity (`entity/src/sbom_package.rs`) to find all packages belonging to the SBOM, then join with `package_license` (`entity/src/package_license.rs`) to get license data for each package.
- For transitive dependency resolution: the SBOM ingestion process (`modules/ingestor/src/graph/sbom/mod.rs`) links packages to SBOMs via `sbom_package`. Walk all packages linked to the SBOM — the `sbom_package` join table already captures the full dependency tree as flattened rows.
- Group packages by their license identifier, creating one `LicenseGroup` per unique license.
- For each group, evaluate compliance using `LicensePolicy::is_compliant()` from Task 1.
- Use SeaORM query patterns consistent with `common/src/db/query.rs` for filtering and joining.
- Performance: use a single query with JOINs rather than N+1 queries. Consider using `.find_with_related()` or explicit `JoinType::LeftJoin` for the sbom_package -> package -> package_license chain.
- Return `AppError` (from `common/src/error.rs`) for missing SBOM or database errors.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service pattern for SBOM queries. Reuse the same database connection handling and error wrapping patterns.
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Package query patterns. May already have methods for fetching packages with license data.
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting. Reuse for building the license aggregation query.
- `entity/src/package_license.rs` — Package-License mapping entity. This is the primary data source for license information.
- `entity/src/sbom_package.rs` — SBOM-Package join table. Use this to find all packages in an SBOM.

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report()` returns a `LicenseReport` for a valid SBOM ID
- [ ] Report groups packages by license type with one `LicenseGroup` per unique license
- [ ] Each `LicenseGroup` includes the license name, list of packages with that license, and a compliance flag
- [ ] Transitive dependencies are included (all packages linked via `sbom_package`)
- [ ] Non-compliant licenses are flagged based on the loaded `LicensePolicy`
- [ ] Returns appropriate error for non-existent SBOM ID
- [ ] Performance: report generation completes within 500ms for SBOMs with up to 1000 packages (p95)

## Test Requirements
- [ ] Unit/integration test: generate report for an SBOM with packages having different licenses — verify correct grouping
- [ ] Unit/integration test: generate report with a policy marking specific licenses as non-compliant — verify `compliant: false` on affected groups
- [ ] Unit/integration test: generate report for an SBOM with transitive dependencies — verify all packages appear in the report
- [ ] Unit/integration test: generate report for a non-existent SBOM ID — verify error response
- [ ] Unit/integration test: generate report for an SBOM with no packages — verify empty groups array

## Verification Commands
- `cargo test --package trustify-fundamental -- license_report` — run license report tests

## Dependencies
- Depends on: Task 1 — Add license report model and policy types
