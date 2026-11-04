# Task 2 — Add license report models and aggregation service

**Feature**: TC-9004 · **Labels**: ai-generated-jira · **Priority**: Major · **Fix Versions**: RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
Add the response models and the service logic that build a license compliance report for one SBOM. The service gathers every package in the SBOM, transitive dependencies included, groups them by license using existing package-license data (no new tables), and marks each group compliant or non-compliant using the `LicensePolicy` from Task 1. The output shape matches the Feature requirement: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`.

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseReport { groups: Vec<LicenseGroup> }` and `LicenseGroup { license: String, packages: Vec<PackageSummary>, compliant: bool }` (serde `Serialize`, and `utoipa::ToSchema` if the sibling models derive it)

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export `license_report`
- `modules/fundamental/src/sbom/service/sbom.rs` — add `SbomService::license_report(&self, id, policy: &LicensePolicy, ...) -> Result<Option<LicenseReport>, AppError>`

## Implementation Notes
- Data sources: `entity/src/sbom_package.rs` (SBOM→package join), `entity/src/package.rs`, and `entity/src/package_license.rs` (package→license mapping). Build **one** joined SeaORM query (sbom_package ⋈ package ⋈ package_license filtered by SBOM id) and group in memory. Do not issue a query per package (N+1), so the NFR of p95 < 500ms for SBOMs with up to 1000 packages holds.
- **Transitive dependencies**: first confirm whether ingestion (`modules/ingestor/src/graph/sbom/mod.rs`) writes every package in the SBOM, transitive ones included, into `sbom_package`. If it does, the join above already covers the full tree. If only direct dependencies are linked and a package-relationship table exists, walk it with a recursive CTE in a single query. Do not add new tables (NFR). If neither holds, stop and raise it on TC-9004 before implementing.
- Packages with several licenses appear in each of their license groups. Packages with **no license data** go into a group with `license: "NOASSERTION"` and `compliant: false`. They must never be dropped or counted as compliant (fail closed for the UC-2 CI gate).
- Return `Ok(None)` when the SBOM id does not exist (reuse the existing fetch in `SbomService`), so the endpoint can map that to 404. An unknown SBOM must never produce an empty `groups` list, which a CI gate would read as compliant.
- Sort groups deterministically (non-compliant first, then by license name) and sort packages by name within each group.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` on DB errors. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust service-code scope. Example: existing fetch/list methods in `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Module pattern: response structs go under `model/`. Applies: task modifies `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's `model/ + service/ + endpoints/` module scope. Example: `modules/fundamental/src/sbom/model/details.rs` (`SbomDetails`).
- Constraints (docs/constraints.md): §2.1–2.3 (commit footer with the Jira ID, Conventional Commits, `Assisted-by: Claude Code` trailer), §3.1–3.3 (branch naming, PR link on Jira, `--base main`), §5.1–5.4 and §5.14 (scope the query to the SBOM's packages at the data-source level), §1.4–1.5.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — reuse as the package element in `LicenseGroup.packages` (already includes `license`). Do not define a new package struct
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package fetch/list query logic. Reuse or extend its query and conversion to `PackageSummary` instead of duplicating it
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing SBOM fetch by id for the existence check
- `common/src/db/query.rs` — shared query builder helpers
- `modules/fundamental/src/sbom/service/license_policy.rs::LicensePolicy::is_compliant` (from Task 1) — the compliance decision

## Acceptance Criteria
- [ ] `LicenseReport` serializes to `{ "groups": [{ "license": "...", "packages": [...], "compliant": bool }] }`
- [ ] Every package linked to the SBOM, transitive dependencies included, appears in the report
- [ ] Each group's `compliant` flag matches `LicensePolicy::is_compliant` for that license
- [ ] Packages without license data appear in a `NOASSERTION` group marked `compliant: false` (fail closed)
- [ ] An unknown SBOM id returns `Ok(None)`, not an empty report
- [ ] Aggregation uses a bounded number of queries, independent of package count (no N+1), and no new tables or migrations

## Test Requirements
- [ ] Test: an SBOM with packages under MIT and GPL-3.0-only yields two groups with the correct `compliant` flags under the default policy
- [ ] Test: transitive dependency packages are included in the groups
- [ ] Test: a package with two licenses appears in both groups
- [ ] Test (fail-closed): a package with no license data lands in `NOASSERTION` with `compliant: false`
- [ ] Test (fail-closed): a nonexistent SBOM id returns `None`, not `Some(empty)`
- [ ] Test: group and package ordering is deterministic

## Verification Commands
- `cargo test -p trustify-module-fundamental license_report` — service and model tests pass (adjust the crate name as needed)

## Dependencies
- Depends on: Task 1 — Add license policy JSON config and loader
