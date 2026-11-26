**Summary:** TC-9004: Implement license report model and service with transitive dependency walk

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the service-layer logic that builds a license compliance report for a given SBOM (TC-9004). The service aggregates packages (including transitive dependencies — the full dependency tree) by license from the existing package-license data, evaluates each license group against the `LicensePolicy` from Task 1, and returns a structured `LicenseReport` of the shape `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`.

No new database tables may be introduced — the report is aggregated from the existing `sbom_package`, `package`, and `package_license` entities.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — export the new `license_report` model module
- `modules/fundamental/src/sbom/service/sbom.rs` — add `SbomService::license_report(sbom_id, &LicensePolicy)` method

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseReport` and `LicenseGroup { license: String, packages: Vec<PackageSummary>, compliant: bool }` response types (serde `Serialize`, `utoipa` schema if used by sibling models)

## Implementation Notes
- Add the method on the existing `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs`, following the existing `fetch`/`list` methods for DB access patterns and `Result<T, AppError>` returns with `.context()` wrapping.
- Data sources (SeaORM entities): `entity/src/sbom.rs`, `entity/src/sbom_package.rs` (SBOM → package join), `entity/src/package.rs`, `entity/src/package_license.rs` (package → license mapping). Aggregate via joins; do **not** add migrations or tables (NFR: "No new database tables").
- **Transitive dependencies:** walk the full dependency tree for the SBOM. Inspect how `modules/ingestor/src/graph/sbom/mod.rs` links packages during ingestion to determine where dependency edges are stored, and traverse them (prefer a single recursive CTE query over per-node round-trips to meet the p95 < 500ms target for 1000 packages). Deduplicate packages reached via multiple paths.
- A package with multiple licenses appears in each corresponding group; a package with no license row is grouped under a dedicated unknown-license group (e.g., `"NOASSERTION"`) which the policy evaluates as non-compliant.
- Group `compliant` is computed with `LicensePolicy::is_compliant` from Task 1 (`modules/fundamental/src/sbom/model/license_policy.rs`).
- **Fail-closed behavior (UC-2 CI gate relies on `compliant: false`):** the service MUST return a not-found `AppError` when the SBOM ID does not exist, rather than an empty report (an empty `groups` array would look "compliant" to a pipeline). Guard site: start of `SbomService::license_report` in `modules/fundamental/src/sbom/service/sbom.rs`.
- Sort groups deterministically (e.g., non-compliant first, then by license name) so report output is stable.
- Per CONVENTIONS.md §Module pattern: place the response type in `model/` and the query logic in `service/`.
  Applies: task modifies `modules/fundamental/src/sbom/model/license_report.rs` matching the convention's domain-module (`model/ + service/ + endpoints/`) scope.
- Per CONVENTIONS.md §Query helpers: reuse `common/src/db/query.rs` helpers for any filtering/sorting rather than hand-rolling query builders.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's service-layer query scope.
- Commit rules (docs/constraints.md §2), PR rules (§3: `--base main`), code change rules (§5) apply.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing fetch logic for resolving an SBOM by ID (reuse for the not-found check)
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing package response type including the `license` field; reuse for `LicenseGroup.packages`
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package fetch/list queries; reuse join logic where it overlaps
- `common/src/db/query.rs` — shared query builder helpers (filtering, sorting)
- `entity/src/package_license.rs` — existing package-license mapping entity

## Acceptance Criteria
- [ ] `SbomService::license_report` returns packages grouped by license with a `compliant` flag per group
- [ ] Transitive dependencies (full tree) are included, and each package appears at most once per license group
- [ ] Packages without license data are grouped under an unknown-license group flagged `compliant: false`
- [ ] A non-existent SBOM ID returns a not-found error, not an empty report
- [ ] No new migrations, tables, or entities are introduced
- [ ] Report generation for an SBOM with 1000 packages completes within the p95 < 500ms target

## Test Requirements
- [ ] Test: SBOM with direct-only packages groups them correctly by license
- [ ] Test: SBOM with transitive dependencies includes the transitive packages' licenses
- [ ] Test: package reachable via two dependency paths is not duplicated
- [ ] Test: group containing a denied license is flagged `compliant: false`; allowed-only group is `compliant: true`
- [ ] Test: package with no license row lands in the unknown group with `compliant: false`
- [ ] Test: unknown SBOM ID returns a not-found error (fail closed), not `{ groups: [] }`

## Verification Commands
- `cargo test --workspace license_report` — all service tests pass

## Dependencies
- Depends on: Task 1 — Add configurable license compliance policy (JSON config + loader)
