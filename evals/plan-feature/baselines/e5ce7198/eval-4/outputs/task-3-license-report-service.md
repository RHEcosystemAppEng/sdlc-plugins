## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report service that generates a compliance report for a given SBOM. The service loads the license policy, queries the SBOM's package-license data (including transitive dependencies), groups packages by license, evaluates each group against the policy, and returns a structured LicenseReport. This is the core business logic for the feature.

## Files to Create
- `modules/fundamental/src/license/service/mod.rs` — LicenseReportService implementation

## Files to Modify
- `modules/fundamental/src/license/mod.rs` — register the service submodule

## Implementation Notes
The service should follow the existing service patterns in the codebase. Reference `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) and `modules/fundamental/src/package/service/mod.rs` (PackageService) for the service struct pattern with database connection handling.

Key implementation steps:
1. Accept an SBOM ID and database connection
2. Load the LicensePolicy (from Task 1)
3. Query the `sbom_package` join table (`entity/src/sbom_package.rs`) to get all packages for the SBOM
4. For each package, look up license data via the `package_license` entity (`entity/src/package_license.rs`)
5. Walk transitive dependencies through the SBOM package graph
6. Group packages by their license identifier
7. For each group, evaluate compliance against the LicensePolicy
8. Build and return a LicenseReport (from Task 2)

Use the query helpers from `common/src/db/query.rs` for database access patterns. All database errors should be wrapped with `.context()` and return `Result<LicenseReport, AppError>` using the error type from `common/src/error.rs`.

Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Consider using a single query with JOINs rather than N+1 queries per package.

Per CONVENTIONS.md §Error Handling: all service methods return Result<T, AppError> with .context() wrapping.
Applies: task creates `modules/fundamental/src/license/service/mod.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `common/src/db/query.rs::QueryBuilder` — shared query builder helpers for filtering and pagination
- `entity/src/package_license.rs` — existing Package-License mapping entity for license lookups
- `entity/src/sbom_package.rs` — SBOM-Package join table for retrieving packages in an SBOM
- `common/src/error.rs::AppError` — standard error type with IntoResponse implementation

## Acceptance Criteria
- [ ] Service correctly groups packages by license for a given SBOM ID
- [ ] Each license group has a `compliant` flag based on the loaded LicensePolicy
- [ ] Transitive dependencies are included in the report with `transitive: true`
- [ ] Unknown/missing licenses are reported with compliance based on the policy's default_policy
- [ ] Service returns AppError::NotFound when the SBOM ID does not exist
- [ ] Report generation meets p95 < 500ms target for SBOMs with up to 1000 packages

## Test Requirements
- [ ] Unit test: service groups packages correctly by license
- [ ] Unit test: denied license in policy results in `compliant: false` for that group
- [ ] Unit test: allowed license in policy results in `compliant: true` for that group
- [ ] Unit test: unknown license with PolicyDefault::Deny marks group as non-compliant
- [ ] Unit test: unknown license with PolicyDefault::Allow marks group as compliant
- [ ] Unit test: non-existent SBOM ID returns NotFound error

## Dependencies
- Depends on: Task 1 — License policy model
- Depends on: Task 2 — License report model

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}]}
