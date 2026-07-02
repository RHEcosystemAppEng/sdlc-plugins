## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license compliance service that generates a license report for a given SBOM. The service traverses the full dependency tree (including transitive dependencies), aggregates packages by license, loads the configured license policy, and evaluates each license group against the policy to produce compliance flags.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with methods to generate the compliance report

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` re-export and wire up the service

## Implementation Notes
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` where `SbomService` provides `fetch` and `list` methods. The `LicenseReportService` should provide a `generate_report(sbom_id, db, policy)` method.
- Use SeaORM to query the `sbom_package` join table (`entity/src/sbom_package.rs`) to get all packages for the SBOM, then join with `package_license` (`entity/src/package_license.rs`) to retrieve license data.
- For transitive dependency traversal: query the `sbom_package` relationship table recursively. If the schema supports a parent-child relationship between packages, walk it. Otherwise, treat all packages linked to the SBOM as the full dependency set (direct + transitive) and mark the `transitive` flag based on depth from the SBOM root.
- Group packages by their SPDX license identifier, then for each group, look up the license in the `LicensePolicy` from Task 1 to determine the `compliant` flag and `policy_category`.
- Licenses not found in the policy should be categorized as `unknown` with `compliant: false` to enforce explicit policy coverage.
- Per CONVENTIONS.md §Error handling: return `Result<LicenseReport, AppError>` from the report generation method with `.context()` wrapping on database query failures. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's .rs scope.
- Per CONVENTIONS.md §Query helpers: use shared query builder helpers from `common/src/db/query.rs` for filtering and pagination if the report supports filtering by license or compliance status. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's .rs scope.
- Per CONVENTIONS.md §Module pattern: place the service in the `service/` subdirectory of the sbom module. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's module organization scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Pattern reference for how services access the database and return domain models
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `entity/src/sbom_package.rs` — SBOM-Package join entity for querying packages belonging to an SBOM
- `entity/src/package_license.rs` — Package-License mapping entity for retrieving license data
- `common/src/model/license_policy.rs::LicensePolicy` — Policy model from Task 1 for compliance evaluation

## Acceptance Criteria
- [ ] Service generates a `LicenseReport` for a given SBOM ID by querying packages and their licenses
- [ ] Transitive dependencies are included in the report with the `transitive` flag set appropriately
- [ ] Each license group is evaluated against the loaded `LicensePolicy` with correct `compliant` and `policy_category` values
- [ ] Unknown licenses (not in policy) are flagged as non-compliant with category `unknown`
- [ ] Report generation meets p95 < 500ms for SBOMs with up to 1000 packages
- [ ] Returns appropriate `AppError` when the SBOM ID is not found

## Test Requirements
- [ ] Unit test: service correctly groups packages by license from mock data
- [ ] Unit test: transitive dependency flag is set correctly
- [ ] Unit test: policy evaluation marks approved licenses as compliant and prohibited licenses as non-compliant
- [ ] Unit test: unknown licenses default to non-compliant

## Dependencies
- Depends on: Task 1 — License policy configuration model and default policy file
- Depends on: Task 2 — License report response model

## additional_fields
```json
{ "labels": ["ai-generated-jira"], "priority": {"name": "Major"}, "fixVersions": [{"name": "RHTPA 1.5.0"}] }
```
