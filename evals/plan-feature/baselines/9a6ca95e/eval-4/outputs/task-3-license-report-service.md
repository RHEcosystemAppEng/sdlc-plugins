## Repository

trustify-backend

## Target Branch

main

## Description

Implement the license report service logic that aggregates package license data from an SBOM and checks each license against the configured policy. This service queries the existing package-license data (no new database tables) and groups results by license identifier, producing the `LicenseReport` response model.

## Files to Modify

- `modules/fundamental/src/sbom/service/mod.rs` — register the new license report service module
- `modules/fundamental/Cargo.toml` — add dependency on the common crate if not already present (for `LicensePolicyService`)

## Files to Create

- `modules/fundamental/src/sbom/service/license_report.rs` — implements the `generate_license_report` method that takes an SBOM ID, queries packages and their licenses, groups by license, and checks compliance

## Implementation Notes

- Follow the service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for database access conventions
- Use SeaORM queries joining `entity/src/sbom_package.rs` and `entity/src/package_license.rs` to retrieve all packages and their licenses for a given SBOM ID
- The `entity/src/package.rs` entity provides package details; `entity/src/package_license.rs` provides the license mapping
- Group packages by their license identifier, creating one `LicenseReportGroup` per unique license
- For each group, call `LicensePolicyService::check_compliance` to set the `compliant` boolean
- Include transitive dependencies by walking the full package set linked to the SBOM through `sbom_package`
- Use the query builder helpers from `common/src/db/query.rs` for any filtering operations
- Return `Result<LicenseReport, AppError>` following the error handling pattern in `common/src/error.rs`
- Target p95 < 500ms for SBOMs with up to 1000 packages: use a single query with joins rather than N+1 queries

## Acceptance Criteria

- `generate_license_report(sbom_id)` returns a `LicenseReport` with packages grouped by license
- Each group has a correct `compliant` flag based on the loaded license policy
- Transitive dependency licenses are included in the report
- No new database tables or migrations are introduced
- The implementation uses efficient join queries (not N+1)
- `cargo check` passes with no errors

## Test Requirements

- Unit test with mock database context verifying correct grouping of packages by license
- Unit test verifying that non-compliant licenses are correctly flagged
- Unit test verifying behavior when an SBOM has no packages (returns empty groups list)
- Unit test verifying that a single package with multiple licenses appears in multiple groups
