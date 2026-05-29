# Task 2 — Add license report service with transitive dependency resolution

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the `LicenseReportService` that aggregates license data from existing package-license records, walks the full transitive dependency tree for an SBOM, groups packages by license type, and evaluates each group's compliance against the configured license policy. This service produces the `LicenseReport` model defined in Task 1 and will be consumed by the endpoint in Task 3.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add license report service module declaration or integrate into existing service module
- `modules/fundamental/src/sbom/mod.rs` — ensure service module exports are updated if needed

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with methods to generate the compliance report

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) for service struct organization, dependency injection (database connection/pool), and error handling with `Result<T, AppError>` and `.context()` wrapping.
- The service must query the `package_license` entity (`entity/src/package_license.rs`) joined through `sbom_package` (`entity/src/sbom_package.rs`) to resolve all packages in an SBOM and their licenses.
- **Transitive dependency resolution:** Walk the full dependency tree starting from the SBOM's direct packages. Use the `sbom_package` join table to find all packages associated with the SBOM. If the SBOM ingestion process (see `modules/ingestor/src/graph/sbom/mod.rs`) already flattens transitive dependencies into the `sbom_package` table, a single query suffices. Inspect the ingestion logic to confirm.
- **Grouping:** Group packages by their license identifier string. Each group becomes a `LicenseGroup` with the license name, the list of packages, and a `compliant` boolean.
- **Compliance evaluation:** Load the `LicensePolicy` (from Task 1) and mark each `LicenseGroup` as `compliant: false` if its license appears in the denied list (denylist mode) or does not appear in the allowed list (allowlist mode).
- **Performance:** The p95 target is < 500ms for SBOMs with up to 1000 packages. Use efficient queries — consider a single JOIN query rather than N+1 queries. Use `common/src/db/query.rs` query builder helpers where applicable.
- No new database tables are required — aggregate from existing `package_license` and `sbom_package` data.
- Use `common/src/error.rs::AppError` for error handling, consistent with existing service patterns.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — demonstrates the service pattern (DB access, error handling, method signatures)
- `modules/fundamental/src/package/service/mod.rs::PackageService` — demonstrates package querying patterns
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `entity/src/package_license.rs` — the SeaORM entity for package-license mappings
- `entity/src/sbom_package.rs` — the SeaORM entity for SBOM-package join table
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion logic showing how packages and dependencies are stored

## Acceptance Criteria
- [ ] `LicenseReportService` generates a `LicenseReport` for a given SBOM ID
- [ ] All packages in the SBOM (including transitive dependencies) are included in the report
- [ ] Packages are correctly grouped by license identifier
- [ ] Each license group has a `compliant` flag evaluated against the configured license policy
- [ ] Returns an appropriate error when the SBOM ID does not exist
- [ ] Report generation meets the p95 < 500ms target for SBOMs with up to 1000 packages

## Test Requirements
- [ ] Unit/integration test: generate report for an SBOM with multiple packages under different licenses — verify correct grouping
- [ ] Unit/integration test: verify non-compliant licenses are flagged when they appear in the policy's denied list
- [ ] Unit/integration test: verify compliant licenses are correctly marked when they appear in the policy's allowed list
- [ ] Unit/integration test: verify that transitive dependencies are included in the report
- [ ] Unit/integration test: verify error handling when SBOM ID does not exist

## Verification Commands
- `cargo test -p trustify-fundamental -- license_report` — run license report service tests

## Dependencies
- Depends on: Task 1 — Add license compliance report model and policy configuration
