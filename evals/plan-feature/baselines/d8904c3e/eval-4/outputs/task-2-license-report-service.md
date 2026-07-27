## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license compliance report service that aggregates package license
data from an SBOM's full dependency tree, groups packages by license type, and
checks each group against the configurable license policy to produce a compliance
report.

The service must walk the complete dependency tree (including transitive
dependencies) using the SBOM-Package relationships, collect the license for each
package, group packages by their license identifier, and evaluate each group
against the loaded `LicensePolicy` to set the `compliant` flag.

Performance target: p95 < 500ms for SBOMs with up to 1000 packages. No new
database tables are needed -- the service aggregates from existing
`package_license`, `sbom_package`, and `package` entity data.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` -- `LicenseReportService` with methods: `generate_report(sbom_id, policy) -> Result<LicenseReport, AppError>` and helper methods for dependency tree walking and license aggregation

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` -- Add `pub mod license_report;` to expose the new service module

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs`
  (`SbomService`) -- services take a database connection/pool parameter and return
  `Result<T, AppError>`.
- Per CONVENTIONS.md Section "Error handling": all service methods must return
  `Result<T, AppError>` with `.context()` wrapping on database and I/O errors.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs`
  matching the convention's `.rs` service file scope.
- Per CONVENTIONS.md Section "Module pattern": place the service under
  `modules/fundamental/src/sbom/service/` following the `model/ + service/ + endpoints/`
  structure.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs`
  matching the convention's module structure scope.
- Per CONVENTIONS.md Section "Query helpers": use the shared query builder helpers
  from `common/src/db/query.rs` for database queries involving filtering and
  pagination of package data.
  Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs`
  matching the convention's `.rs` service file scope.
- Use `entity/src/sbom_package.rs` to find all packages linked to the SBOM.
- Use `entity/src/package_license.rs` to resolve the license for each package.
- For transitive dependency walking, query `sbom_package` relationships recursively
  or use a CTE (Common Table Expression) if the schema supports parent-child
  package relationships.
- Group packages by normalized license identifier (case-insensitive SPDX matching).
- For each group, check the `LicensePolicy`: if the license is in `denied_licenses`,
  set `compliant = false`; if in `allowed_licenses`, set `compliant = true`;
  otherwise follow `default_mode`.
- Consider using a single database query with joins rather than N+1 queries to meet
  the p95 < 500ms performance target.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` -- demonstrates the
  service pattern with database access; reuse its connection handling approach
- `modules/fundamental/src/package/service/mod.rs::PackageService` -- existing
  package query logic; may contain reusable methods for fetching package data
- `common/src/db/query.rs` -- shared query builder helpers for filtering and
  pagination; use these instead of writing custom query logic
- `entity/src/package_license.rs` -- the SeaORM entity for package-license
  relationships; use this for license lookups
- `entity/src/sbom_package.rs` -- the SeaORM entity for SBOM-package join table;
  use this for dependency tree traversal

## Acceptance Criteria
- [ ] `LicenseReportService` generates a `LicenseReport` for a given SBOM ID
- [ ] Packages are grouped by license identifier (case-insensitive)
- [ ] Transitive dependencies are included in the report (full dependency tree walk)
- [ ] Each group's `compliant` flag reflects the license policy evaluation
- [ ] Service returns appropriate error when SBOM ID does not exist
- [ ] No new database tables or migrations are introduced

## Test Requirements
- [ ] Unit test: service groups packages correctly by license (3+ packages with 2 different licenses)
- [ ] Unit test: service correctly flags non-compliant licenses when in the denied list
- [ ] Unit test: service correctly marks compliant licenses when in the allowed list
- [ ] Unit test: service applies default-deny mode correctly (unlisted licenses are non-compliant)
- [ ] Unit test: service applies default-allow mode correctly (unlisted licenses are compliant)
- [ ] Unit test: service returns error for non-existent SBOM ID

## Verification Commands
- `cargo check -p trustify-module-fundamental` -- compiles without errors
- `cargo test -p trustify-module-fundamental -- license_report` -- all unit tests pass

## Dependencies
- Depends on: Task 1 -- Add license report model types and policy configuration
