# Task 2 — Add license compliance service for SBOM packages

## Repository
trustify-backend

## Target Branch
main

## Description
Add a service method that generates a license compliance report for a given SBOM. The method aggregates all package licenses (including transitive dependencies) from the SBOM's dependency tree, groups them by license type, and checks each group against the configurable license policy to determine compliance.

This implements the core business logic for TC-9004. The method queries existing `package_license` data through the SBOM-Package relationship without requiring new database tables.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — license report generation logic: query packages for an SBOM, walk transitive dependencies via `sbom_package` join, aggregate by license, check compliance against policy

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add `pub mod license_report;` to register the new service module

## API Changes
- `SbomService::generate_license_report(sbom_id, db, policy) -> Result<LicenseReport, AppError>` — NEW: generates a compliance report for the given SBOM

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for method signatures, error handling, and database access conventions.
- All service methods return `Result<T, AppError>` — use `.context()` wrapping for error enrichment as shown in existing service methods (see `common/src/error.rs` for AppError).
- Use SeaORM queries to join `sbom_package` with `package` and `package_license` entities to collect all licenses for an SBOM. The entities are defined in:
  - `entity/src/sbom_package.rs` — SBOM-Package join table
  - `entity/src/package.rs` — Package entity
  - `entity/src/package_license.rs` — Package-License mapping
- For transitive dependency traversal: walk the `sbom_package` relationship from the SBOM to all packages (direct and transitive). The SBOM ingestion process in `modules/ingestor/src/graph/sbom/mod.rs` already links all packages (including transitive) to the SBOM via `sbom_package`, so a single join query should capture the full dependency tree without recursive traversal.
- Group results by license identifier using a `HashMap<String, Vec<PackageLicenseEntry>>`, then check each group against the `LicensePolicy` to set the `compliant` flag.
- Performance requirement: p95 < 500ms for SBOMs with up to 1000 packages. Use a single database query with JOINs rather than N+1 queries. Consider using `common/src/db/query.rs` query builder helpers for efficient query construction.
- Per CONVENTIONS.md: follow the service module pattern where service logic is in a separate file within `service/`. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's service directory scope.
- Per docs/constraints.md section 5.4: do not duplicate existing query patterns — reuse helpers from `common/src/db/query.rs`.
- Per docs/constraints.md section 2: commits must follow Conventional Commits format and reference TC-9004.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — follow the same service method patterns for database access, error handling, and function signatures
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reuse for constructing the license aggregation query
- `common/src/error.rs::AppError` — error type with `.context()` wrapping; use for all error handling
- `entity/src/package_license.rs` — Package-License mapping entity; query this for license data
- `entity/src/sbom_package.rs` — SBOM-Package join table; use for traversing the dependency tree
- `modules/fundamental/src/package/service/mod.rs::PackageService` — reference for package query patterns

## Acceptance Criteria
- [ ] `generate_license_report` method exists on `SbomService` (or in a dedicated service module)
- [ ] Method aggregates all package licenses for a given SBOM including transitive dependencies
- [ ] Packages are grouped by license type (SPDX identifier)
- [ ] Each group has a `compliant` flag based on the license policy configuration
- [ ] Method returns `Result<LicenseReport, AppError>` following the existing error handling pattern
- [ ] A single database query (with JOINs) is used instead of N+1 queries

## Test Requirements
- [ ] Unit/integration test for a normal SBOM with multiple packages and licenses, verifying correct grouping
- [ ] Test for an SBOM with no packages, verifying an empty groups list is returned
- [ ] Test for an SBOM where some packages have non-compliant licenses, verifying the `compliant: false` flag
- [ ] Test for transitive dependency inclusion — verify that indirectly linked packages are included in the report
- [ ] Test verifying p95 performance stays under 500ms for an SBOM with 1000 packages (use a seeded test database)

## Verification Commands
- `cargo test --package trustify-fundamental -- license_report` — run license report service tests

## Dependencies
- Depends on: Task 1 — Add license report model and policy configuration
