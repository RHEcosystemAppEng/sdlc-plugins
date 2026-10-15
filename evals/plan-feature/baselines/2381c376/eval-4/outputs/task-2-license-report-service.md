## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license compliance report service that aggregates package license data from existing database tables, walks the full transitive dependency tree for an SBOM, and checks each license against the configured policy to produce a compliance report.

The service must meet the non-functional requirement of p95 < 500ms for SBOMs with up to 1000 packages. It must not create new database tables -- all data is aggregated from the existing `package_license`, `sbom_package`, and `package` entities.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` -- `LicenseReportService` with a `generate_report` method that accepts an SBOM ID and returns a `LicenseComplianceReport`

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` -- add `pub mod license_report;` and re-export the service
- `modules/fundamental/Cargo.toml` -- add any necessary dependencies (if not already present)

## Implementation Notes
- Follow the existing service pattern: see `modules/fundamental/src/sbom/service/sbom.rs` for `SbomService` as the structural reference. The service should accept a database connection/pool and the policy configuration.
- Use SeaORM queries against existing entities: `entity/src/sbom_package.rs` (SBOM-Package join), `entity/src/package.rs` (Package entity), and `entity/src/package_license.rs` (Package-License mapping).
- Transitive dependency resolution: walk the `sbom_package` relationships recursively to include all transitive dependencies, not just direct ones. Use an iterative approach with a visited set to avoid cycles.
- License grouping: aggregate packages by their license identifier from `package_license`. Group into `LicenseGroup` entries.
- Policy checking: for each license group, check the license against the loaded `LicensePolicy` to set the `compliant` flag. Allowlist mode: compliant if license is in the allowed list. Denylist mode: compliant if license is NOT in the denied list.
- Error handling: return `Result<LicenseComplianceReport, AppError>` using the `AppError` enum from `common/src/error.rs`. Use `.context()` wrapping for all fallible operations per the project's error handling convention.
- Performance: use batch queries rather than N+1 queries. Load all package-license mappings for the SBOM in a single query, then group in memory.
- Use the query builder helpers from `common/src/db/query.rs` for any filtering operations.
- Per docs/constraints.md S5.4: reuse existing query patterns from `SbomService` and `PackageService` rather than writing new query logic from scratch.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- structural reference for service pattern, database access, and error handling
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- reference for package-related query patterns
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` -- error type with `.context()` pattern
- `entity/src/sbom_package.rs` -- SBOM-Package join table entity for dependency traversal
- `entity/src/package_license.rs` -- Package-License mapping entity for license data

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report(sbom_id)` returns a `LicenseComplianceReport` with packages grouped by license
- [ ] Transitive dependencies are included in the report (not just direct dependencies)
- [ ] Each license group has a correct `compliant` flag based on the configured policy
- [ ] Non-existent SBOM IDs return an appropriate error (not a panic or empty report)
- [ ] No new database tables are created -- all data comes from existing entities
- [ ] All errors are wrapped with `.context()` per the project's error handling pattern

## Test Requirements
- [ ] Unit test: service groups packages by license correctly for a mock dataset
- [ ] Unit test: service flags non-compliant licenses when using a denylist policy
- [ ] Unit test: service flags non-compliant licenses when using an allowlist policy
- [ ] Unit test: service includes transitive dependencies in the report
- [ ] Unit test: service returns an error for a non-existent SBOM ID
- [ ] Unit test: service handles an SBOM with no packages (returns empty groups)

## Dependencies
- Depends on: Task 1 -- Add license compliance report model and policy configuration
