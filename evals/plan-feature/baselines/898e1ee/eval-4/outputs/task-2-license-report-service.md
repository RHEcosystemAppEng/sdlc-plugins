## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report generation logic in the SBOM service layer. This service method queries the existing package-license data for a given SBOM, walks the full dependency tree (including transitive dependencies), groups packages by license type, evaluates each group against the configured license policy, and returns a `LicenseReport`. No new database tables are needed — the method aggregates from existing `sbom_package` and `package_license` entity data.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — Add a `license_report(&self, sbom_id: Id) -> Result<LicenseReport, AppError>` method to `SbomService`

## Files to Create
- `license-policy.json` — Default license policy configuration file at the repository root (or a `config/` directory) with a starter set of allowed/denied licenses based on common OSI-approved licenses

## Implementation Notes
Follow the existing service method patterns in `modules/fundamental/src/sbom/service/sbom.rs` where `SbomService` methods like fetch and list demonstrate the conventions for database queries, error handling with `.context()`, and return types.

The `license_report` method should:
1. Verify the SBOM exists (reuse existing fetch logic in `SbomService`)
2. Query all packages linked to the SBOM via the `sbom_package` join table (`entity/src/sbom_package.rs`)
3. For each package, look up its license(s) via the `package_license` mapping (`entity/src/package_license.rs`)
4. Walk transitive dependencies — the SBOM ingestion graph in `modules/ingestor/src/graph/sbom/mod.rs` shows how package relationships are stored; use the same join paths to traverse the dependency tree
5. Group packages by license string
6. Load the `LicensePolicy` configuration and evaluate each group's compliance
7. Return the assembled `LicenseReport`

For performance (p95 < 500ms for 1000 packages): use a single query with JOINs to fetch all package-license data for the SBOM rather than N+1 queries. The query builder helpers in `common/src/db/query.rs` may be useful for constructing the aggregation query.

All errors should return `Result<T, AppError>` using the patterns in `common/src/error.rs`.

Per CONVENTIONS.md §Error Handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `.rs` scope.

Per CONVENTIONS.md §Module Pattern: follow the `model/ + service/ + endpoints/` structure.
Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's module structure scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Existing service with fetch/list methods to follow as patterns; reuse the SBOM existence check
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting; reuse for constructing the aggregation query
- `entity/src/sbom_package.rs` — SBOM-Package join table entity for querying packages belonging to an SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for looking up licenses per package
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion graph showing how package dependency relationships are stored

## Acceptance Criteria
- [ ] `SbomService::license_report(sbom_id)` returns a `LicenseReport` with packages grouped by license
- [ ] Transitive dependencies are included in the report (full dependency tree walk)
- [ ] Each license group has a `compliant` flag evaluated against the loaded `LicensePolicy`
- [ ] Returns `AppError::NotFound` if the SBOM ID does not exist
- [ ] No new database tables or migrations are created
- [ ] Default `license-policy.json` configuration file is present in the repository

## Test Requirements
- [ ] Unit test: service returns correct grouping for an SBOM with packages under multiple licenses
- [ ] Unit test: transitive dependencies are included in the grouping
- [ ] Unit test: compliance flags correctly reflect the policy (compliant and non-compliant cases)
- [ ] Unit test: service returns NotFound error for non-existent SBOM ID

## Dependencies
- Depends on: Task 1 — Add license compliance report model and policy types

[sdlc-workflow] Description digest: sha256-md:11a8308dda9d5eaf972a480c19956afafd9d5581918ce57f0dfa40989fe85d45
