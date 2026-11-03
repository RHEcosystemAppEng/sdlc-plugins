## Repository
trustify-backend

## Target Branch
main

## Description
Implement the service-layer aggregation that builds a license compliance report for a given SBOM (TC-9004). The service collects every package in the SBOM — including transitive dependencies — joins each package to its license(s) from the existing package-license mapping, groups packages by license, and marks each group compliant or non-compliant using the `LicensePolicy` from Task 1. Data is aggregated from existing tables only; no new tables are introduced.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `SbomService::license_report(sbom_id, &LicensePolicy) -> Result<LicenseReport, AppError>`

## Implementation Notes
- Data sources (SeaORM entities):
  - `entity/src/sbom.rs` — SBOM existence check (return not-found `AppError` when the SBOM id does not exist)
  - `entity/src/sbom_package.rs` — SBOM-to-package join table
  - `entity/src/package.rs` — package rows
  - `entity/src/package_license.rs` — package-to-license mapping
- **Transitive dependencies:** the Feature requires walking the full dependency tree. Before implementing, verify how `modules/ingestor/src/graph/sbom/mod.rs` populates `sbom_package` — if ingestion links every package in the SBOM document (direct and transitive) to the SBOM, a single join over `sbom_package` covers the full tree. If only direct dependencies are linked and package-to-package relationships are stored elsewhere, walk those relationships (e.g., recursive CTE) without adding tables. Record which case applies in the PR description.
- Build the report with a single joined query (`sbom_package` ⨝ `package` ⨝ `package_license`) filtered by `sbom_id`, then group in memory with a `BTreeMap<String, Vec<PackageSummary>>` for deterministic ordering. Avoid N+1 per-package queries to meet the p95 < 500ms target for SBOMs with up to 1000 packages.
- A package with multiple licenses appears in each matching license group. A package with no license row MUST be placed in an explicit unknown group (e.g., `license: "NOASSERTION"`) evaluated by `LicensePolicy::is_compliant` (which returns `false` per Task 1) — never silently dropped. Dropping unlicensed packages would make the CI gate (UC-2) pass green on incomplete data.
- An SBOM that exists but has zero packages returns `{ "groups": [] }`; this is the only case where an empty report is valid.
- Map package rows to `PackageSummary` (`modules/fundamental/src/package/model/summary.rs`) using the same conversion already used by `PackageService` in `modules/fundamental/src/package/service/mod.rs`.
- Per CONVENTIONS.md §Framework: implement the query with SeaORM entity relations, not raw SQL strings. Applies: task modifies modules/fundamental/src/sbom/service/sbom.rs matching the convention's Rust (`.rs`) SeaORM data-access scope. Example: existing fetch/list methods in `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Error handling: return `Result<LicenseReport, AppError>` and wrap database errors with `.context()`. Applies: task modifies modules/fundamental/src/sbom/service/sbom.rs matching the convention's Rust handler/service (`.rs`) scope. Example: `SbomService` fetch in `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Query helpers: reuse shared filtering helpers from `common/src/db/query.rs` where they apply to the SBOM-id filter rather than writing new filter builders. Applies: task modifies modules/fundamental/src/sbom/service/sbom.rs matching the convention's service-layer query (`.rs`) scope. Example: `common/src/db/query.rs`.
- Constraints (docs/constraints.md): Conventional Commits with Jira footer and `Assisted-by: Claude Code` trailer (§2.1–2.3); PR `--base main`, link posted to Jira (§3.2–3.3); scope to listed files, inspect before modifying, no duplicated logic (§5.1–5.4); trace the full data flow input → query → grouping → output before committing (§5.6); verify the query is filtered by the target SBOM id at the data-source level (§5.14).

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing SBOM fetch logic; reuse its SBOM lookup / not-found handling
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package fetch/list and entity-to-`PackageSummary` mapping
- `common/src/db/query.rs` — shared filtering helpers
- `entity/src/package_license.rs` — existing package-license mapping (aggregate from here; no new tables)

## Acceptance Criteria
- [ ] `SbomService::license_report` returns packages grouped by license for the requested SBOM only
- [ ] Transitive dependency packages are included in the report
- [ ] Each group's `compliant` flag reflects `LicensePolicy::is_compliant` for that license
- [ ] Packages without license data appear in an explicit unknown/`NOASSERTION` group flagged `compliant: false` (fail-closed), not omitted
- [ ] A non-existent SBOM id returns a not-found `AppError`, not an empty report
- [ ] Group ordering is deterministic
- [ ] No new migrations, tables, or entities are added

## Test Requirements
- [ ] Integration test (test DB): SBOM with MIT and Apache-2.0 packages returns two groups, both compliant under an allow-list containing both
- [ ] Integration test: SBOM containing a denied license returns that group with `compliant: false`
- [ ] Integration test: transitive dependency package appears in its license group
- [ ] Integration test: package with no license row appears in the unknown group with `compliant: false` (fail-closed path)
- [ ] Integration test: package with two licenses appears in both groups
- [ ] Integration test: unknown SBOM id returns not-found error
- [ ] Integration test: packages from a different SBOM are not included

## Verification Commands
- `cargo test -p trustify-module-fundamental license_report` — service tests pass

## Dependencies
- Depends on: Task 1 — License policy configuration and report model
