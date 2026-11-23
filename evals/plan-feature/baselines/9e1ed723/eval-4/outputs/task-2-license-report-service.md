## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license compliance report aggregation for TC-9004. Given an SBOM ID, the service collects every package in the SBOM — including transitive dependencies — joins each package to its license data, groups packages by license, and flags each group as compliant or non-compliant using the `LicensePolicy` from Task 1. The report is aggregated from existing package-license data; no new database tables are added.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseReport { groups: Vec<LicenseGroup> }` and `LicenseGroup { license: String, packages: Vec<PackageSummary>, compliant: bool }` response types
- `modules/fundamental/src/sbom/service/license_report.rs` — `SbomService::license_report(sbom_id, &LicensePolicy)` aggregation logic

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export `license_report`
- `modules/fundamental/src/sbom/service/mod.rs` — declare the `license_report` service module
- `modules/fundamental/src/sbom/service/sbom.rs` — expose the new `license_report` method on `SbomService` alongside fetch/list/ingest

## Implementation Notes
- Query path: `entity/src/sbom.rs` (SBOM) → `entity/src/sbom_package.rs` (SBOM-Package join) → `entity/src/package.rs` (Package) → `entity/src/package_license.rs` (Package-License mapping). Use SeaORM joins in a single (or bounded number of) queries rather than per-package lookups, to meet the p95 < 500ms target for SBOMs with up to 1000 packages.
- Transitive dependencies: the full dependency tree must be walked. Verify at implementation time how SBOM ingestion (`modules/ingestor/src/graph/sbom/mod.rs`) persists package relationships. If `sbom_package` already links every (direct and transitive) package of the SBOM, aggregate from it directly; if dependency edges are stored, walk them (e.g. recursive CTE) with cycle protection. See the impact map's open question on this point — do not add new tables.
- Packages with multiple licenses appear in each corresponding license group; packages with no license are grouped under a dedicated `NOASSERTION` group evaluated by the policy's `unknown_license` rule.
- Group ordering should be deterministic (non-compliant groups first, then alphabetical by license) so CI consumers get stable output.
- **Fail-closed aggregation (gate site: `SbomService::license_report` in `modules/fundamental/src/sbom/service/license_report.rs`)**: UC-2 blocks builds only when a group has `compliant: false`, so an empty `groups` array reads as a pass. The service must (a) return a not-found `AppError` when the SBOM ID does not exist instead of an empty report, (b) never drop packages whose license lookup fails or is missing — they must appear in the `NOASSERTION` group, and (c) never return `compliant: true` for a group when policy evaluation could not be performed.
- Reuse the query helpers in `common/src/db/query.rs` where applicable and `PackageSummary` (`modules/fundamental/src/package/model/summary.rs`) for package entries instead of defining a new package DTO.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust handler/service source scope.
- Per CONVENTIONS.md §Module pattern: report types go in `sbom/model/`, aggregation logic in `sbom/service/`. Applies: task modifies `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's `modules/*/src/*/service/` directory scope.
- Per CONVENTIONS.md §Query helpers: use the shared helpers in `common/src/db/query.rs` rather than hand-rolled query building. Applies: task modifies `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's database query code scope.
- Constraints (docs/constraints.md): commits must reference the Jira task in the footer, follow Conventional Commits, and include an `Assisted-by:` trailer (§2.1–2.3); PR must target `--base main` and its link must be posted on the Jira task (§3.2–3.3); changes must stay within Files to Modify / Files to Create, inspect code before modifying, reuse existing utilities, and trace the full data flow (§5.1–5.6).

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing SBOM fetch logic; reuse its SBOM lookup / not-found handling
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package fetch/list queries joining package data; reuse query shape where possible
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — package DTO already containing the `license` field
- `common/src/db/query.rs` — shared query builder helpers
- `entity/src/package_license.rs` — existing Package-License mapping entity (the data source for the report)

## Acceptance Criteria
- [ ] `SbomService::license_report` returns packages grouped by license, each group with a `compliant` flag computed from `LicensePolicy`
- [ ] Transitive dependency packages are included in the report, not only direct dependencies
- [ ] Packages with no license data appear in a `NOASSERTION` group evaluated by the policy (non-compliant by default) — no package is silently dropped
- [ ] A non-existent SBOM ID returns a not-found error, not an empty report
- [ ] No new database tables or migrations are added
- [ ] Group ordering is deterministic

## Test Requirements
- [ ] Service test: SBOM with MIT, Apache-2.0, and a denied license returns three groups with correct `compliant` flags
- [ ] Service test: a transitive dependency's license appears in the report
- [ ] Service test (fail-closed): a package with no license row is reported in the `NOASSERTION` group with `compliant: false`, and the total package count in the report equals the SBOM's package count
- [ ] Service test (fail-closed): unknown SBOM ID returns a not-found error rather than `groups: []`
- [ ] Performance test: report for an SBOM with 1000 packages completes within the p95 < 500ms budget on the test database

## Verification Commands
- `cargo test -p trustify-module-fundamental license_report` — all service tests pass

## Dependencies
- Depends on: Task 1 — Add configurable license compliance policy
