## Repository
trustify-backend

## Target Branch
main

## Description
Implement the license report aggregation for TC-9004. Given an SBOM ID, collect every package in the SBOM, including transitive dependencies, together with its license. Group the packages by license and use the license policy from Task 1 to flag each group as compliant or non-compliant. The aggregation reads existing package-license data. No new database tables are introduced.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — response types: `LicenseReport { groups: Vec<LicenseGroup> }`, `LicenseGroup { license: String, packages: Vec<PackageSummary>, compliant: bool }`
- `modules/fundamental/src/sbom/service/license_report.rs` — `generate_license_report(sbom_id, &LicensePolicy, &db) -> Result<LicenseReport, AppError>`

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export the `license_report` module
- `modules/fundamental/src/sbom/service/mod.rs` — declare the `license_report` module
- `modules/fundamental/src/sbom/service/sbom.rs` — expose a `SbomService::license_report` method that delegates to the new service function, keeping one service entry point per SBOM

## Implementation Notes
- Data sources (SeaORM entities): `entity/src/sbom.rs`, `entity/src/sbom_package.rs` (SBOM-to-package join), `entity/src/package.rs`, `entity/src/package_license.rs` (package-to-license mapping). Join `sbom_package` → `package` → `package_license` in a single query filtered by `sbom_id`. Avoid N+1 per-package queries so the query meets the p95 < 500ms target for up to 1000 packages.
- **Transitive dependencies:** the requirement is to walk the full dependency tree. The repository structure shows no explicit package-to-package relationship entity. Before implementing, check `modules/ingestor/src/graph/sbom/mod.rs` (SBOM ingestion: parse, store, link packages) to confirm whether `sbom_package` already stores every package in the SBOM, direct and transitive. If it does, the join above covers transitive dependencies. If only direct dependencies are linked, stop and raise this with the feature owner. Do not add new tables (NFR: "No new database tables").
- Deduplicate packages that appear more than once in the tree. Sort groups deterministically (non-compliant groups first, then by license name) so the output is stable for CI consumers.
- Packages without any `package_license` row go into a group with license `"UNKNOWN"`. That group is evaluated through `LicensePolicy::evaluate(None)`, so it is non-compliant by default.
- **Fail-closed gate (gate site: `generate_license_report` in `modules/fundamental/src/sbom/service/license_report.rs`).** If the SBOM ID does not exist, return `AppError` NotFound. Never return an empty `groups` array, because a CI gate checking for `compliant: false` would read that as a pass. If the SBOM exists but has zero packages, also return an error or an explicit non-compliant marker, never a silent "all compliant" empty report. Decide between these with the feature owner and record the decision in the PR.
- Per CONVENTIONS.md §Error handling: return `Result<LicenseReport, AppError>` with `.context()` wrapping on database calls. Applies: task modifies `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's Rust handler/service (`.rs`) scope. See `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Query helpers: reuse filtering helpers from `common/src/db/query.rs` rather than hand-building query fragments. Applies: task modifies `modules/fundamental/src/sbom/service/license_report.rs` matching the convention's database query (`.rs` service) scope. See `common/src/db/query.rs`.
- Per CONVENTIONS.md §Module pattern: place types under `sbom/model/` and logic under `sbom/service/`. Applies: task modifies `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's domain module (`modules/*/src/<domain>/`) scope. See `modules/fundamental/src/sbom/model/details.rs`.
- The report is a single structured document, not a list endpoint, so do not wrap it in `PaginatedResults<T>`.
- Constraints (docs/constraints.md): §5.1 keep changes to the files listed above; §5.2 inspect existing code before modifying it; §5.4 do not duplicate `PackageService` lookups; §5.14 filter the query to the target SBOM at the database level; §2.1–2.3 commit rules; §3.1–3.3 PR rules.

## Reuse Candidates
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package fetch logic. Reuse or extend it for package-plus-license retrieval rather than writing a parallel query
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — already includes the `license` field. Reuse it as the package element type in `LicenseGroup`
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing SBOM fetch, for the SBOM existence check
- `common/src/db/query.rs` — shared query builder helpers
- `common/src/error.rs::AppError` — error type

## Acceptance Criteria
- [ ] `generate_license_report` returns packages grouped by license, and each group's `compliant` flag comes from `LicensePolicy`
- [ ] Transitive dependency packages are included in the report, each package at most once
- [ ] Packages with no license data appear in an `UNKNOWN` group marked `compliant: false` under the default policy
- [ ] A nonexistent SBOM ID returns a NotFound `AppError`, never an empty report (fail-closed)
- [ ] An SBOM with no package data never produces a report that reads as fully compliant (fail-closed)
- [ ] No new database tables or migrations are added
- [ ] Package and license data are fetched without per-package queries (no N+1)

## Test Requirements
- [ ] Integration test: an SBOM with MIT and GPL packages produces two groups with the correct `compliant` flags
- [ ] Integration test: transitive dependency packages appear in the report
- [ ] Integration test: a package with no license lands in the `UNKNOWN` group with `compliant: false`
- [ ] Integration test: a nonexistent SBOM returns NotFound rather than an empty `groups` list
- [ ] Integration test: an SBOM with zero packages does not produce an all-compliant empty report
- [ ] Performance check: the report for a seeded SBOM with 1000 packages completes within the 500ms budget in the test environment

## Verification Commands
- `cargo test -p fundamental license_report` — all service tests pass

## Dependencies
- Depends on: Task 1 — Add configurable license policy and evaluator
