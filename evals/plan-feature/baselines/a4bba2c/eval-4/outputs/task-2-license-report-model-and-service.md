# Task 2 — Add license report model and service logic

## Repository
trustify-backend

## Target Branch
main

## Description
Add the license compliance report model structs and service logic within the existing SBOM module. The service aggregates packages from an SBOM (including transitive dependencies) by license type, checks each license against the compliance policy, and produces a structured report. This provides the business logic consumed by the endpoint in Task 3.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — LicenseGroup and LicenseComplianceReport structs with serde Serialize
- `modules/fundamental/src/sbom/service/license_report.rs` — License report generation logic: query packages for an SBOM, walk transitive dependencies, group by license, apply policy

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod license_report;` to expose the new model
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod license_report;` to expose the new service module
- `modules/fundamental/src/sbom/mod.rs` — Ensure model and service sub-modules are re-exported if needed

## Implementation Notes
- Follow the existing module pattern: models in `model/` with serde derives, service logic in `service/` — see `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/service/sbom.rs` for the established patterns.
- **LicenseComplianceReport struct** should contain:
  - `groups: Vec<LicenseGroup>` — packages grouped by license
  - A summary field with counts (total packages, compliant count, non-compliant count)
- **LicenseGroup struct** should contain:
  - `license: String` — the SPDX license identifier
  - `packages: Vec<PackageLicenseInfo>` — packages with this license (name, version, whether transitive)
  - `compliant: bool` — whether this license is compliant per the policy
- Query packages for a given SBOM using the `sbom_package` join table (`entity/src/sbom_package.rs`) and the `package_license` mapping (`entity/src/package_license.rs`).
- Walk the full dependency tree for transitive dependencies. The `sbom_package` join table links SBOMs to their packages; follow package dependency relationships to include transitive deps.
- Use the `LicensePolicy` from Task 1 (accessed via Axum state/extension or passed as a parameter) to determine compliance for each license group.
- Error handling: return `Result<LicenseComplianceReport, AppError>` using the existing `AppError` enum from `common/src/error.rs` with `.context()` wrapping per project conventions.
- Use the shared query helpers from `common/src/db/query.rs` for database operations where applicable.
- Performance: the feature requires p95 < 500ms for SBOMs with up to 1000 packages. Batch database queries rather than N+1 querying, and consider using a single query with JOINs to fetch all package-license data for an SBOM.
- Per docs/constraints.md section 2 (Commit Rules): commits must reference TC-9004, follow Conventional Commits, and include the `Assisted-by: Claude Code` trailer.
- Per docs/constraints.md section 5 (Code Change Rules): inspect existing code before modifying, follow patterns in Implementation Notes, do not duplicate existing functionality.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs` — SbomService for existing SBOM fetch/query patterns
- `modules/fundamental/src/package/service/mod.rs` — PackageService for package query patterns
- `modules/fundamental/src/package/model/summary.rs` — PackageSummary struct (includes `license` field) — reuse or reference for license data access
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `common/src/error.rs` — AppError enum for error handling patterns
- `entity/src/package_license.rs` — Package-License mapping entity to query license data
- `entity/src/sbom_package.rs` — SBOM-Package join table for linking SBOM to its packages

## Acceptance Criteria
- [ ] LicenseComplianceReport and LicenseGroup structs are defined with serde Serialize
- [ ] Service correctly queries all packages (direct and transitive) for a given SBOM ID
- [ ] Packages are grouped by license type
- [ ] Each group's `compliant` field correctly reflects the license policy
- [ ] Non-existent SBOM ID returns an appropriate error (not a panic or empty report)
- [ ] Report generation completes within performance budget for SBOMs with up to 1000 packages

## Test Requirements
- [ ] Unit test: grouping logic correctly groups packages by license
- [ ] Unit test: compliance flag is set correctly for allowed, denied, and review_required licenses
- [ ] Unit test: transitive dependencies are included in the report
- [ ] Unit test: empty SBOM (no packages) returns an empty report with zero counts
- [ ] Unit test: SBOM with packages that have no license data handles gracefully (e.g., groups under "Unknown" or "NOASSERTION")

## Dependencies
- Depends on: Task 1 — Add license compliance policy configuration
