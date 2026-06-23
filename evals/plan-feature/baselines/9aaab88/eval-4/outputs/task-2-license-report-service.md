## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report service logic that aggregates package license data from an SBOM, walks transitive dependencies, groups packages by license type, and checks each group against the configured license policy to determine compliance status. This is the core business logic for the license compliance report feature.

## Files to Create
- `modules/fundamental/src/sbom/service/license_report.rs` — `LicenseReportService` with methods: `generate_report(sbom_id) -> Result<LicenseReport, AppError>` that loads packages for the SBOM, resolves transitive dependencies, groups by license, and evaluates policy compliance

## Files to Modify
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Reuse the existing SBOM fetch logic to load the SBOM and validate it exists before generating the report
- `modules/fundamental/src/package/service/mod.rs::PackageService` — Reuse package listing/fetching to retrieve packages associated with the SBOM
- `entity/src/sbom_package.rs` — Use the SBOM-Package join entity to query packages belonging to a specific SBOM
- `entity/src/package_license.rs` — Use the Package-License mapping entity to resolve license information for each package
- `common/src/error.rs::AppError` — Use the existing error type with `.context()` wrapping for all fallible operations

## Implementation Notes
- Follow the service pattern in `modules/fundamental/src/sbom/service/sbom.rs` for method signatures, error handling, and database access patterns.
- Use `entity/src/sbom_package.rs` to query all packages linked to the target SBOM ID.
- Use `entity/src/package_license.rs` to resolve each package's license identifier.
- For transitive dependency resolution: query `sbom_package` relations recursively or use a CTE-based query to walk the dependency tree. If the existing schema does not have explicit dependency edges, aggregate all packages linked to the SBOM (direct and transitive are already flattened during ingestion in `modules/ingestor/src/graph/sbom/mod.rs`).
- Load the license policy from `license-policy.json` at service initialization or per-request. A package's license is compliant if it appears in the `allowed` list and not in the `denied` list.
- Group packages into `LicenseGroup` structs keyed by license identifier, setting `compliant: bool` based on policy evaluation.
- Target p95 < 500ms for SBOMs with up to 1000 packages — use a single query with JOINs rather than N+1 queries.
- Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping on database and I/O errors. Applies: task creates `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Module pattern: follow model/ + service/ + endpoints/ structure. Applies: task modifies `modules/fundamental/src/sbom/service/mod.rs` matching the convention's `.rs` module scope.

## Acceptance Criteria
- [ ] `LicenseReportService::generate_report(sbom_id)` returns a `LicenseReport` with packages grouped by license
- [ ] Each `LicenseGroup` has a correct `compliant` flag based on the license policy
- [ ] Transitive dependencies are included in the report (all packages linked to the SBOM)
- [ ] Non-existent SBOM IDs return an appropriate `AppError::NotFound`
- [ ] No N+1 query patterns — license data is fetched in bulk

## Test Requirements
- [ ] Unit test with mock data: SBOM with 5 packages across 3 licenses (2 allowed, 1 denied) produces correct grouping and compliance flags
- [ ] Unit test: empty SBOM (no packages) returns an empty report with no groups
- [ ] Unit test: all packages have allowed licenses results in all groups marked compliant
- [ ] Unit test: policy with a denied license correctly flags the corresponding group as non-compliant

## Dependencies
- Depends on: Task 1 — Add license policy configuration and model types

[sdlc-workflow] Description digest: sha256-md:56ceb67a8612bac63d39c3079f234cd497c9186a9390d2cb42633bc17eab88d1
