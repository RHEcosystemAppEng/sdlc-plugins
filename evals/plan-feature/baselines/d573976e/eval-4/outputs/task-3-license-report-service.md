# Task 3 — Add license report service

## Repository
trustify-backend

## Target Branch
main

## Description
Add the service layer that generates a license compliance report for a given SBOM. The service aggregates packages from the SBOM by their license using existing package-license data, walks transitive dependencies through the sbom_package relationship, and evaluates each license group against the configured policy to determine compliance.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add license report method to SbomService or add `license_report` module declaration

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — license report generation logic: query packages for SBOM, resolve transitive dependencies, group by license, evaluate compliance via LicensePolicy

## API Changes
- `SbomService::get_license_report(sbom_id, policy) -> Result<LicenseReportSummary, AppError>` — NEW: generates the license compliance report

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` — the existing SbomService handles fetch, list, and ingest operations
- Query strategy (no new tables required per NFRs):
  1. Use the `sbom_package` join table (`entity/src/sbom_package.rs`) to get all packages for the given SBOM ID
  2. Use the `package_license` mapping (`entity/src/package_license.rs`) to get the license for each package
  3. For transitive dependencies: walk the dependency tree through sbom_package relationships. The SBOM ingestion process (`modules/ingestor/src/graph/sbom/mod.rs`) links packages during ingestion, so the dependency graph should be queryable from the existing data
  4. Group packages by license identifier
  5. For each group, call `LicensePolicy::is_compliant()` to set the compliance flag
- Use existing query helpers from `common/src/db/query.rs` for database operations
- Error handling: wrap all database errors with `.context()` and return `Result<T, AppError>` per the pattern in `common/src/error.rs`
- Performance: the NFR requires p95 < 500ms for SBOMs with up to 1000 packages. Consider:
  - Batch-loading package-license mappings in a single query rather than N+1 queries
  - Using a HashMap for grouping to achieve O(n) aggregation

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — extend with license report method or follow its patterns for a new service
- `entity/src/sbom_package.rs` — existing SBOM-Package join entity for querying packages by SBOM
- `entity/src/package_license.rs` — existing Package-License mapping for resolving package licenses
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion logic that establishes the package dependency graph (reference for understanding data relationships)

## Acceptance Criteria
- [ ] Service correctly aggregates packages by license for a given SBOM
- [ ] Transitive dependencies are included in the report (full dependency tree walk)
- [ ] Compliance flags are set correctly based on the provided LicensePolicy
- [ ] Packages with no license information are grouped and flagged appropriately
- [ ] Returns appropriate error when SBOM ID does not exist

## Test Requirements
- [ ] Integration test: generate report for an SBOM with packages having different licenses and verify grouping
- [ ] Integration test: verify transitive dependencies appear in the report
- [ ] Integration test: verify compliance flags match policy (allowed license -> compliant: true, denied license -> compliant: false)
- [ ] Integration test: verify error response for non-existent SBOM ID
- [ ] Unit test: verify grouping logic with mock data produces correct LicenseGroup entries

## Verification Commands
- `cargo test --package fundamental -- license_report` — run license report service tests

## Dependencies
- Depends on: Task 1 — Add license policy configuration model
- Depends on: Task 2 — Add license report response model
