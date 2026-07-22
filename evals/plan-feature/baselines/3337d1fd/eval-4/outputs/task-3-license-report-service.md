## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license compliance report service that queries package-license data for a given SBOM, walks the transitive dependency tree, groups packages by license, and applies the license policy to determine compliance flags. This is the core business logic for the license report feature.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add re-export for the new license_report service module
- `modules/fundamental/Cargo.toml` — Add any needed dependencies (if not already present)

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` (or extend `SbomService`) with a `generate_report(sbom_id: Uuid, policy: &LicensePolicy, db: &DatabaseConnection) -> Result<LicenseReportResponse, AppError>` method. Implementation steps: (1) query all packages linked to the SBOM via the `sbom_package` join table, (2) for each package, fetch its license(s) from the `package_license` entity, (3) walk transitive dependencies by following package dependency relationships, (4) group packages by license identifier, (5) classify each group using the LicensePolicy, (6) build and return the LicenseReportResponse with summary statistics.

## Implementation Notes
- Use the existing `sbom_package` join table in `entity/src/sbom_package.rs` to find packages for a given SBOM.
- Use the `package_license` entity in `entity/src/package_license.rs` to look up license identifiers for each package.
- For transitive dependency resolution, query the dependency graph recursively. Use a visited-set to avoid cycles.
- Follow the existing query patterns in `common/src/db/query.rs` for database access.
- Use `.context()` wrapping on all fallible operations per the project's error handling convention.
- Ensure the query is performant for SBOMs with up to 1000 packages (p95 < 500ms NFR). Consider batching package-license lookups rather than N+1 queries.
- No new database tables are needed; aggregate from existing `package`, `sbom_package`, and `package_license` entities.

## Acceptance Criteria
- [ ] Service correctly groups all direct dependency packages by license
- [ ] Service correctly includes transitive dependency packages with `is_transitive: true`
- [ ] Each license group has the correct compliance flag based on the loaded policy
- [ ] Summary statistics (total, compliant, non-compliant, restricted counts) are accurate
- [ ] Returns `AppError::NotFound` if the SBOM ID does not exist
- [ ] Handles packages with no license data gracefully (grouped under "Unknown")

## Test Requirements
- [ ] Unit test: given mock package-license data, verify correct grouping by license
- [ ] Unit test: verify transitive dependencies are included and flagged correctly
- [ ] Unit test: verify summary statistics calculation
- [ ] Unit test: verify error handling for non-existent SBOM ID

## Dependencies
- Depends on: Task 1 — License policy model (provides LicensePolicy and classification logic)
- Depends on: Task 2 — License report model (provides response types)
