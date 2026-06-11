## Repository
trustify-backend

## Target Branch
main

## Description
Add service-layer logic to generate a license compliance report for a given SBOM. The service aggregates all packages associated with an SBOM (including transitive dependencies), groups them by license type, loads the license policy configuration, and flags non-compliant license groups. This service will be called by the endpoint handler (Task 3).

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — LicenseReportService with a `generate_report(sbom_id, db)` method that queries package-license data, walks transitive dependencies, groups by license, and applies policy checks
- `config/license-policy.json` — default license policy configuration file defining denied and allowed license lists

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod license_report;` to expose the new service module

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) — services accept a database connection and return `Result<T, AppError>`.
- Use the existing `entity/package_license.rs` (Package-License mapping) and `entity/sbom_package.rs` (SBOM-Package join table) entities to query license data for all packages in an SBOM.
- Walk transitive dependencies by joining through `sbom_package` to find all packages (direct and transitive) linked to the SBOM. The SBOM ingestion process in `modules/ingestor/src/graph/sbom/mod.rs` already links packages during ingestion, so the dependency graph is already stored.
- Use `common/src/db/query.rs` query builder helpers for constructing the database queries.
- Error handling: wrap all database errors with `.context()` and return `AppError`, consistent with the pattern in `common/src/error.rs`.
- Load the license policy from the `config/license-policy.json` file at the repository root. The policy should be read and deserialized into the `LicensePolicy` struct created in Task 1.
- Group packages by their `license` field value, creating one `LicenseGroup` per distinct license. Set `compliant: false` for any group whose license appears in the policy's denied list.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Use a single query with joins rather than N+1 queries.
- No new database tables are needed — aggregate from existing `package_license` and `sbom_package` entity data.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — demonstrates the established service pattern (database access, error handling, return types)
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reuse for constructing the license data query
- `common/src/error.rs::AppError` — the standard error type; use for all error returns
- `entity/package_license.rs` — the existing entity mapping packages to licenses; this is the primary data source
- `entity/sbom_package.rs` — the SBOM-Package join table entity; use to find all packages belonging to an SBOM

## Acceptance Criteria
- [ ] `generate_report` method exists and returns a `LicenseReport` for a given SBOM ID
- [ ] All packages linked to the SBOM (including transitive dependencies) are included in the report
- [ ] Packages are correctly grouped by license type
- [ ] Non-compliant licenses are flagged with `compliant: false` based on the policy file
- [ ] A default license policy configuration file exists at `config/license-policy.json`
- [ ] Database errors are properly wrapped with `.context()` and returned as `AppError`

## Test Requirements
- [ ] Unit test verifying packages are correctly grouped by license type
- [ ] Unit test verifying compliance flags are set correctly based on a test policy (denied licenses flagged as non-compliant)
- [ ] Unit test verifying transitive dependencies are included in the report
- [ ] Unit test verifying an SBOM with no packages returns an empty report
- [ ] Unit test verifying performance with a mock dataset of 1000 packages completes within acceptable bounds

## Verification Commands
- `cargo build -p trustify-fundamental` — should compile without errors
- `cargo test -p trustify-fundamental license_report` — should pass all unit tests

## Dependencies
- Depends on: Task 1 — Add license compliance report model structs
