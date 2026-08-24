## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license compliance report service that aggregates package license data for a given SBOM and checks each license group against the configured policy. The service queries the existing package-license data through SeaORM entities, groups packages by license type, walks transitive dependencies, and flags non-compliant licenses based on the `LicensePolicy` configuration.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` -- add `pub mod license_report;` declaration

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` -- implement `LicenseReportService` with methods to generate the compliance report

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`). The service takes a database connection and any required configuration as constructor parameters.
- Query packages associated with the SBOM using the `sbom_package` join table entity (`entity/src/sbom_package.rs`), then join with `package_license` entity (`entity/src/package_license.rs`) to get license information.
- To include transitive dependency licenses (per requirement), walk the full dependency tree starting from the SBOM's direct packages. Use the `sbom_package` relationship to resolve transitive dependencies.
- Group results by license string, creating one `LicenseGroup` per distinct license. For each group, check the license against `LicensePolicy.denied_licenses` to set the `compliant` flag.
- Performance requirement: p95 < 500ms for SBOMs with up to 1000 packages. Use a single query with JOINs rather than N+1 queries. Consider using `common/src/db/query.rs` query builder helpers for efficient filtering.
- No new database tables are needed -- aggregate from existing `package_license` and `sbom_package` data.
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` and use `.context()` wrapping for all error paths.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ directory structure.
  Applies: task modifies `modules/fundamental/src/sbom/service/mod.rs` matching the convention's `.rs` module file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- reference implementation for service pattern (constructor, database access, error handling)
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- package query patterns; may have methods for fetching packages by SBOM
- `entity/src/sbom_package.rs` -- SBOM-Package join table entity for querying packages belonging to an SBOM
- `entity/src/package_license.rs` -- Package-License mapping entity for resolving license data
- `common/src/db/query.rs` -- shared query builder helpers for filtering and pagination
- `common/src/error.rs::AppError` -- error type for Result return values

## Acceptance Criteria
- [ ] `LicenseReportService` is defined and exported from the sbom service module
- [ ] `generate_report(sbom_id)` method returns a `LicenseReport` with packages grouped by license
- [ ] Each `LicenseGroup` has its `compliant` flag set based on the configured `LicensePolicy`
- [ ] Transitive dependency licenses are included in the report
- [ ] The service uses efficient JOIN queries (no N+1 queries)
- [ ] All error paths use `AppError` with `.context()` wrapping

## Test Requirements
- [ ] Unit test: service correctly groups packages by license type
- [ ] Unit test: service flags denied licenses as non-compliant
- [ ] Unit test: service marks allowed licenses as compliant
- [ ] Unit test: service handles an SBOM with no packages (returns empty groups)
- [ ] Unit test: service includes transitive dependencies in the report

## Verification Commands
- `cargo build -p trustify-fundamental` -- compiles without errors
- `cargo test -p trustify-fundamental -- license_report` -- service unit tests pass

## Dependencies
- Depends on: Task 1 -- Add license report model types and policy configuration
