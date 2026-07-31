## Repository
trustify-backend

## Target Branch
main

## Priority
Major

## Fix Versions
RHTPA 1.5.0

## Description
Implement the license report service that aggregates package license data from an SBOM, walks transitive dependencies to include the full dependency tree, groups packages by license, and checks each group against the configured license policy. This service powers the license compliance report endpoint.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with methods to generate the compliance report: query package-license mappings for an SBOM, walk transitive dependencies via `sbom_package` relations, group by license, and evaluate compliance against the loaded policy
- `modules/fundamental/src/sbom/service/license_policy.rs` — Policy loader that reads the JSON license policy config file and provides compliance checking logic

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` and `pub mod license_policy;` to expose the new service modules

## Implementation Notes
Follow the service pattern established in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`). The service should accept a database connection and SBOM ID, then:

1. Query `entity/src/sbom_package.rs` join table to get all packages in the SBOM
2. For each package, query `entity/src/package_license.rs` to get license mappings
3. Walk transitive dependencies through the `sbom_package` relations to include indirect dependencies
4. Group packages by license identifier
5. Load the license policy from the config file
6. Evaluate each license group against the policy, setting the `compliant` flag

Use `common/src/db/query.rs` query builder helpers for constructing database queries. Return `Result<LicenseReport, AppError>` using the error type from `common/src/error.rs` with `.context()` wrapping for error messages.

The policy loader should look for a `license-policy.json` file in a configurable path (defaulting to the working directory). If no policy file is found, default to all-compliant (no restrictions).

Per CONVENTIONS.md §Module pattern: implement service logic in the service/ subdirectory following the model/ + service/ + endpoints/ structure. Applies: task modifies `modules/fundamental/src/sbom/service/mod.rs` matching the convention's Rust module scope.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping for meaningful error messages. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs::query` — Shared query builder helpers for filtering and pagination; reuse for constructing the package-license aggregation query
- `common/src/error.rs::AppError` — Standard error type; use for all fallible operations in the service
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Reference for service struct pattern and database connection handling

## Acceptance Criteria
- [ ] `LicenseReportService` generates a `LicenseReport` from an SBOM ID
- [ ] Packages are grouped by license with correct package counts
- [ ] Transitive dependencies are included in the report (not just direct dependencies)
- [ ] Compliance flags are correctly set based on the loaded license policy
- [ ] Missing SBOM ID returns an appropriate `AppError` (404)
- [ ] Missing or empty policy file defaults to all-compliant behavior
- [ ] Report generation meets p95 < 500ms target for SBOMs with up to 1000 packages

## Test Requirements
- [ ] Unit test that a single-level SBOM groups packages by license correctly
- [ ] Unit test that transitive dependencies are included in the aggregation
- [ ] Unit test that a deny-list policy flags matching licenses as non-compliant
- [ ] Unit test that an allow-list policy flags unlisted licenses as non-compliant
- [ ] Unit test that an SBOM with no packages returns an empty report
- [ ] Unit test that a missing SBOM ID returns a 404 error

## Dependencies
- Depends on: Task 1 — Add license report model and policy types
