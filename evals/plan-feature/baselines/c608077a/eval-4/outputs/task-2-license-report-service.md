**Summary:** Add license report models and aggregation service
**Epic:** TC-9004: License compliance report API
**Labels:** ai-generated-jira | **Priority:** Major | **Fix Versions:** RHTPA 1.5.0

## Repository
trustify-backend

## Target Branch
main

## Description
Implement the core of TC-9004: given an SBOM ID, aggregate all of the SBOM's packages — including transitive dependencies — by license, using existing package-license data (no new database tables), and evaluate each license group against the license policy from Task 1. Produces the response model consumed by the endpoint in Task 3: `{ groups: [{ license: "MIT", packages: [...], compliant: true }] }`.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add `SbomService::license_report(sbom_id, &LicensePolicy)` method
- `modules/fundamental/src/sbom/model/mod.rs` — export the license report model module

## Files to Create
- `modules/fundamental/src/sbom/model/license_report.rs` — `LicenseReport { groups: Vec<LicenseGroup> }` and `LicenseGroup { license: String, packages: Vec<PackageSummary>, compliant: bool }` (serde `Serialize`, utoipa schema if the module uses it)

## Implementation Notes
- Data sources: `entity/src/sbom_package.rs` (SBOM→Package join), `entity/src/package.rs`, `entity/src/package_license.rs` (Package→License mapping). Use SeaORM joins: `sbom_package` → `package` → `package_license`, filtered by `sbom_id`.
- **Transitive dependencies:** verify in `modules/ingestor/src/graph/sbom/mod.rs` that ingestion links every package in the SBOM (direct and transitive) via `sbom_package`. If so, aggregating over `sbom_package` covers the full dependency tree. If ingestion only links direct packages, stop and raise this on TC-9004 — walking the tree would require a dependency-edge table, which conflicts with the "no new database tables" NFR.
- **Performance (p95 < 500ms for 1000 packages):** fetch everything in a single joined query (or at most a constant number of queries); group in memory with a `BTreeMap<String, Vec<PackageSummary>>` for deterministic ordering. Do not issue per-package queries (no N+1). Deduplicate packages reached via multiple paths.
- **Fail-closed behavior (protects the UC-2 CI gate):** packages with no `package_license` row MUST be placed in an `UNKNOWN` group with `compliant: false` — never dropped. A package with multiple licenses appears in each of its license groups. The guard belongs in `SbomService::license_report` in `modules/fundamental/src/sbom/service/sbom.rs`.
- Return `AppError` not-found (existing variant in `common/src/error.rs`) when the SBOM ID does not exist, rather than an empty report.
- Reuse the existing SBOM fetch logic in `SbomService` (`modules/fundamental/src/sbom/service/sbom.rs`) to check SBOM existence.
- Per CONVENTIONS.md §Module pattern: keep the report model in `sbom/model/license_report.rs` and the aggregation in `sbom/service/sbom.rs`, mirroring `modules/fundamental/src/sbom/model/details.rs`.
  Applies: task modifies modules/fundamental/src/sbom/service/sbom.rs matching the convention's domain module (`.rs` model/service) scope.
- Per CONVENTIONS.md §Framework: use SeaORM entities/query builders (not raw SQL strings) for the aggregation query; see `entity/src/package_license.rs`.
  Applies: task modifies modules/fundamental/src/sbom/service/sbom.rs matching the convention's Rust/SeaORM (`.rs`) scope.
- Per CONVENTIONS.md §Query helpers: use shared helpers in `common/src/db/query.rs` for filter construction where applicable instead of hand-rolled query code.
  Applies: task modifies modules/fundamental/src/sbom/service/sbom.rs matching the convention's database query (`.rs`) scope.
- Per CONVENTIONS.md §Error handling: return `Result<LicenseReport, AppError>` with `.context()` wrapping on DB errors; see `common/src/error.rs`.
  Applies: task modifies modules/fundamental/src/sbom/service/sbom.rs matching the convention's Rust error-handling (`.rs`) scope.
- Applicable constraints (docs/constraints.md): §2 commit rules; §3 PR rules (`--base main`); §5 code change rules (5.1 scope, 5.4 no duplication, 5.6 data-flow trace, 5.11–5.13 test doc comments and given-when-then); §1.4/1.5.

## Reuse Candidates
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — existing package DTO with `license` field; use it as the package element type in `LicenseGroup.packages`
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package fetch/list queries; reuse its query construction / entity-to-summary conversion instead of duplicating
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing SBOM fetch used for existence check
- `common/src/db/query.rs` — shared filtering helpers
- `entity/src/package_license.rs` — existing package→license mapping (source of truth; no new tables)

## Acceptance Criteria
- [ ] `SbomService::license_report` returns packages grouped by license with a `compliant` flag computed from `LicensePolicy`
- [ ] Transitive dependency packages of the SBOM are included in the report
- [ ] Packages without license data appear in an `UNKNOWN` group with `compliant: false` (fail-closed; never silently omitted)
- [ ] Packages with multiple licenses appear in each corresponding group; packages are not duplicated within a group
- [ ] Non-existent SBOM ID returns a not-found `AppError`, not an empty report
- [ ] No new database tables or migrations are introduced
- [ ] Aggregation uses a constant number of queries independent of package count

## Test Requirements
- [ ] Test: SBOM with packages under MIT, Apache-2.0, and a denied license → three groups with correct `compliant` flags
- [ ] Test: SBOM with a transitive dependency → transitive package appears in its license group
- [ ] Test (fail-closed): package with no license row → appears in `UNKNOWN` group with `compliant: false`
- [ ] Test: package with two licenses → appears in both groups
- [ ] Test: unknown SBOM ID → not-found error
- [ ] Test: SBOM with zero packages → empty `groups` (and endpoint semantics documented)

## Verification Commands
- `cargo test -p trustify-module-fundamental license_report` — all service tests pass

## Dependencies
- Depends on: Task 1 — Add configurable license policy and loader
