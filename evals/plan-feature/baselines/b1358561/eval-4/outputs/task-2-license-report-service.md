## Repository
trustify-backend

## Target Branch
main

## Description
Implement the service-layer aggregation behind the TC-9004 license compliance report. Given an SBOM ID, collect every package in the SBOM, including transitive dependencies (walk the full dependency tree), group the packages by license, and flag each group as compliant or non-compliant using the `LicensePolicy` from Task 1. The report is built from existing package and license data only. No new database tables are added.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseReport { sbom_id, groups: Vec<LicenseGroup> }` and `LicenseGroup { license: String, packages: Vec<PackageSummary>, compliant: bool }` response models (serde `Serialize` plus the OpenAPI derive used by sibling models)
- `modules/fundamental/src/sbom/service/license_report.rs` — `SbomService::license_report(sbom_id, &LicensePolicy, &db)` (or a dedicated `LicenseReportService`) that runs the aggregation

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export `license_report`
- `modules/fundamental/src/sbom/service/mod.rs` — declare the `license_report` service module
- `modules/fundamental/src/sbom/service/sbom.rs` — expose the report method on `SbomService` (or delegate to the new module) so the endpoint in Task 3 can call it like the existing `fetch` and `list` methods

## Implementation Notes
- Data sources (existing SeaORM entities, no migrations):
  - `entity/src/sbom_package.rs` — SBOM-to-package join. This is the starting set of packages for the SBOM.
  - `entity/src/package.rs` — package entity
  - `entity/src/package_license.rs` — package-to-license mapping
- Transitive dependencies: the report must include every package reachable through the SBOM's dependency relationships, not only direct `sbom_package` rows. Inspect how `modules/ingestor/src/graph/sbom/mod.rs` ("parse, store, link packages") persists package relationships, and walk the same relationships. Prefer a single recursive CTE or a batched breadth-first walk over N+1 per-package queries so SBOMs with up to 1000 packages meet the p95 < 500ms NFR. De-duplicate packages that appear through several paths, and guard against cycles.
- Grouping: group by normalized license identifier. A package with multiple licenses appears in each matching group. Packages with no license go into an explicit `"NOASSERTION"` / `"unknown"` group. They must not be dropped.
- Compliance flag: `LicenseGroup.compliant = policy.evaluate(license)`. Fail-closed: the `"unknown"` group and unrecognized licenses take the policy's fail-closed default from Task 1. The service must not set `compliant: true` for a group it could not evaluate.
- Empty result vs. missing SBOM: when the SBOM ID does not exist, return a not-found `AppError`. Do not return an empty `groups: []` report, because a CI gate (UC-2) would read an empty report as "no violations" and pass. This gate site lives in the service method in `modules/fundamental/src/sbom/service/license_report.rs`.
- Use `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` as the pattern for DB access and SBOM lookup (reuse its fetch-by-id logic for the existence check instead of re-querying).
- Per CONVENTIONS.md §Module pattern: report models go in `sbom/model/` and aggregation logic in `sbom/service/`. Applies: task modifies `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's domain module (`modules/*/src/**.rs`) scope. Example: `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Error handling: return `Result<LicenseReport, AppError>` and wrap DB errors with `.context()`. Applies: task modifies `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust source (`.rs`) scope. Example: `common/src/error.rs`.
- Per CONVENTIONS.md §Query helpers: use the shared filtering/query helpers instead of hand-rolled query building. Applies: task modifies `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's database query (`.rs` service) scope. Example: `common/src/db/query.rs`.
- Constraints (docs/constraints.md): §5.1 change only the files listed above; §5.4 reuse existing services and helpers; §5.6 trace the data flow end to end (SBOM → packages → licenses → groups); §5.14 filter queries to the target SBOM at the data source, with no full-table scans filtered in memory; §2.1–2.3 commit format and trailers; §3.3 `--base main`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing fetch-by-id. Reuse it for the SBOM existence check and DB access pattern.
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package fetch/list logic. Reuse its package-to-`PackageSummary` conversion instead of duplicating it.
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — use it as the package item type inside each `LicenseGroup`.
- `common/src/db/query.rs` — shared query builder helpers.
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for how package dependency relationships are stored (source of truth for the transitive walk).

## Acceptance Criteria
- [ ] The service returns a `LicenseReport` whose `groups` contain every package in the SBOM, grouped by license
- [ ] Transitive dependencies are included (packages reachable only through other packages appear in the report)
- [ ] Each package appears once per license group, even when it is reachable through multiple dependency paths. Cycles do not cause infinite loops.
- [ ] Packages without license data appear in an explicit unknown/NOASSERTION group flagged `compliant: false` under the default policy
- [ ] Each group's `compliant` flag matches `LicensePolicy::evaluate` for that license
- [ ] Fail-closed: a non-existent SBOM ID produces a not-found error, not an empty report
- [ ] No new database tables or migrations are introduced
- [ ] The aggregation uses a bounded number of queries (no per-package N+1 queries)

## Test Requirements
- [ ] Integration test: an SBOM with direct-only packages under two licenses produces two correctly flagged groups
- [ ] Integration test: an SBOM with a transitive dependency chain (A → B → C) includes C in the report
- [ ] Integration test: a package reachable via two paths is not duplicated, and a dependency cycle terminates
- [ ] Integration test: a package with no license lands in the unknown group with `compliant: false`
- [ ] Integration test (fail-closed): a non-existent SBOM ID returns a not-found error rather than `groups: []`

## Verification Commands
- `cargo test license_report` — service tests pass

## Dependencies
- Depends on: Task 1 — Add configurable license compliance policy
