## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report service logic that aggregates packages by license for a given SBOM and evaluates compliance against a configurable policy. The service queries the existing package-license data, groups packages by their license identifier, walks transitive dependencies, and applies the license policy to flag non-compliant groups.

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — add re-export for the new license report service module

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — implement `LicenseReportService` with a `generate_report` method

## Implementation Notes
- Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) — inject a database connection pool, return `Result<T, AppError>` from public methods.
- The `generate_report` method should:
  1. Accept an SBOM ID and an optional `LicensePolicy` reference
  2. Query the `sbom_package` join table (`entity/src/sbom_package.rs`) to get all packages for the SBOM
  3. For each package, look up its license data via the `package_license` entity (`entity/src/package_license.rs`)
  4. Walk transitive dependencies — follow the dependency links in `sbom_package` to include indirect dependencies
  5. Group packages by license identifier into `LicenseGroup` entries
  6. If a `LicensePolicy` is provided, evaluate each group's license against the policy and set the `compliant` flag
  7. Return a `LicenseReport` containing all groups with computed compliance flags
- Use `common/src/db/query.rs` for any query builder helpers needed for filtering and joining.
- Use `common/src/error.rs::AppError` for error handling with `.context()` wrapping as established in the codebase.
- Performance target: p95 < 500ms for SBOMs with up to 1000 packages. Fetch all packages in a single query rather than N+1 queries. Consider using a single JOIN query across `sbom_package` and `package_license` tables.
- Per constraints doc section 2 (Commit Rules): use Conventional Commits format, reference TC-9004 in the footer, include `--trailer="Assisted-by: Claude Code"`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — demonstrates the service pattern (constructor with DB pool injection, `Result<T, AppError>` returns, query construction)
- `modules/fundamental/src/package/service/mod.rs::PackageService` — demonstrates how to query package entities and could serve as reference for the package-license joins
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination; reuse for building the aggregation query
- `common/src/error.rs::AppError` — error type with `.context()` wrapping used across all services
- `entity/src/package_license.rs` — the package-license mapping entity; this is the data source for license information

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report` returns a `LicenseReport` with packages grouped by license
- [ ] Transitive dependency licenses are included in the report
- [ ] When a `LicensePolicy` is provided, each `LicenseGroup` has the correct `compliant` flag
- [ ] When no `LicensePolicy` is provided, all groups default to `compliant: true`
- [ ] Errors from database queries are wrapped with `AppError` and `.context()`

## Test Requirements
- [ ] Unit test for grouping logic: given a flat list of packages with known licenses, verify correct grouping into `LicenseGroup` entries
- [ ] Unit test for compliance evaluation: given a policy with denied licenses, verify non-compliant groups are flagged
- [ ] Unit test for transitive dependency inclusion: verify that indirect dependencies appear in the report
- [ ] Unit test for no-policy case: verify all groups default to compliant when no policy is provided
- [ ] Unit test for empty SBOM: verify the service returns an empty report without errors

## Dependencies
- Depends on: Task 1 — Add license report model types

[sdlc-workflow] Description digest: sha256:2aad9b5a9f9197217b26d0c1d8e6df4529fb45fd6e7678fe5ba948617880fee3
