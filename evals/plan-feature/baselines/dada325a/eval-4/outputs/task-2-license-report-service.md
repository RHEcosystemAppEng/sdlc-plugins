## Repository
trustify-backend

## Target Branch
main

## Description
Add the service logic that builds the license compliance report for one SBOM. It aggregates the existing package-license data for every package in the SBOM, including transitive dependencies. It groups packages by license and flags each group as compliant or non-compliant using the `LicensePolicy` from Task 1. No new database tables are introduced. The report is computed from the existing `sbom_package` and `package_license` data. This is the core of TC-9004: compliance teams and CI/CD pipelines use the report to find license violations.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseReport { groups: Vec<LicenseGroup> }` and `LicenseGroup { license: String, packages: Vec<PackageSummary>, compliant: bool }` response structs (serde `Serialize`)
- `modules/fundamental/src/sbom/service/license_report.rs` — `SbomService::license_report(sbom_id, &LicensePolicy, &db)` (or a dedicated `LicenseReportService`) that runs the aggregation query and builds the groups

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export `license_report`
- `modules/fundamental/src/sbom/service/mod.rs` — declare the `license_report` service module
- `modules/fundamental/src/sbom/service/sbom.rs` — add or expose the SBOM lookup used to return "not found" for unknown SBOM IDs (reuse the existing fetch logic)

## Implementation Notes
- Data sources (SeaORM entities): `entity/src/sbom.rs` (SBOM), `entity/src/sbom_package.rs` (SBOM-Package join), `entity/src/package.rs` (Package), `entity/src/package_license.rs` (Package-License mapping). Join `sbom_package` → `package` → `package_license`, filtered by `sbom_id`. Aggregate in one query, or a small fixed number of queries. Do not run one query per package (N+1), so the p95 < 500ms target for 1000-package SBOMs is achievable.
- Transitive dependencies: the requirement is to "walk the full dependency tree". First check whether SBOM ingestion (`modules/ingestor/src/graph/sbom/mod.rs`, "parse, store, link packages") already links every package in the SBOM, including transitive ones, through `sbom_package`. If it does, the join above covers transitive packages. If ingestion stores only direct relationships, walk the stored relationships (for example, a recursive CTE) without adding tables. Record which approach was used in the PR description.
- Packages with several licenses (one row per license in `package_license`) appear in each matching group.
- Packages with no `package_license` row must not be silently dropped. Put them in a dedicated group (e.g., `license: "NOASSERTION"`) and evaluate that group with the policy's `unknown_license` rule, which defaults to non-compliant.
- Fail closed (UC-2 automated compliance gate): a CI pipeline passes when no group has `compliant: false`. These degraded cases must not produce a report that looks compliant:
  - Unknown SBOM ID: return a not-found `AppError`. Do not return an empty `groups` array.
  - SBOM with packages but no license data: report them under the `NOASSERTION` group as non-compliant (by default). Do not return an empty or all-compliant report.
  - Policy failed to load: propagate the error. Do not evaluate against an empty policy.
  The guard belongs in the report-building function in `modules/fundamental/src/sbom/service/license_report.rs`.
- Sort groups deterministically (e.g., non-compliant first, then by license name) and sort packages within each group by name, so CI output is stable.
- Per CONVENTIONS.md §Module pattern: put response structs in `model/` and query/aggregation logic in `service/`. Follow `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`) as the existing example.
  Applies: task modifies `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's domain module (`modules/*/src/<domain>/service/*.rs`) scope.
- Per CONVENTIONS.md §Error handling: service functions return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust source (`.rs`) scope.
- Constraints (docs/constraints.md): Conventional Commits with the Jira ID in the footer and an `Assisted-by:` trailer (§2.1–2.3). PR uses `--base main` (§3.3). Stay within the listed files and reuse existing query helpers (§5.1, §5.4). Trace the data flow from the SBOM ID through the query to the grouped output (§5.6). Make sure the query is scoped to the single SBOM (§5.14).

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing SBOM fetch logic. Reuse it for the existence check and not-found handling.
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package fetch/list logic. Reuse its package-to-`PackageSummary` mapping.
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing package DTO that already includes `license`. Use it as the package element in `LicenseGroup.packages`.
- `common/src/db/query.rs` — shared query builder helpers (filtering/sorting). Reuse them instead of hand-building filters.
- `entity/src/package_license.rs` — existing package-license mapping entity. This is the source of license data, so no new table is needed.

## Acceptance Criteria
- [ ] The service returns a `LicenseReport` whose `groups` cover every package linked to the SBOM, including transitive dependencies
- [ ] Each group's `compliant` flag comes from `LicensePolicy::is_compliant` for that license
- [ ] A package with multiple licenses appears in each corresponding group
- [ ] Packages with no license data appear in a `NOASSERTION` group that is non-compliant under the default policy. They are never silently omitted (fail closed).
- [ ] An unknown SBOM ID returns a not-found error, not an empty report (fail closed)
- [ ] No new database tables or migrations are added
- [ ] Groups and packages are ordered deterministically

## Test Requirements
- [ ] Test: an SBOM with MIT and Apache-2.0 packages produces two compliant groups with the correct package membership
- [ ] Test: an SBOM containing a denied license produces a group with `compliant: false`
- [ ] Test: an SBOM with transitive (indirect) dependencies includes their licenses in the report
- [ ] Test: a package with no license rows is reported in the `NOASSERTION` group as non-compliant. The report is not empty and not all-compliant.
- [ ] Test: an unknown SBOM ID returns a not-found error rather than `{ groups: [] }`
- [ ] Test: a multi-licensed package appears in every matching group
- [ ] Performance test or benchmark: report generation for an SBOM with 1000 packages completes within the p95 < 500ms target

## Verification Commands
- `cargo test -p fundamental license_report` — service tests pass

## Dependencies
- Depends on: Task 1 — Add configurable license policy and compliance evaluator
