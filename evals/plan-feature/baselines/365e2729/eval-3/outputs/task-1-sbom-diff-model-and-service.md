## Repository
trustify-backend

## Target Branch
main

## Description
Add the domain model and service logic that computes a structured diff between two SBOMs (TC-9003, SBOM comparison view). Given a "left" and a "right" SBOM ID, the service loads each SBOM's packages (with versions and licenses) and associated advisories from existing tables and computes six diff categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. The diff is computed on-the-fly — no new database tables or migrations (Non-Functional Requirement). This task provides the business logic consumed by the HTTP endpoint in Task 2.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export the new `compare` model module
- `modules/fundamental/src/sbom/service/mod.rs` — declare and re-export the new `compare` service module
- `modules/fundamental/src/sbom/service/sbom.rs` — expose (or reuse) a helper on `SbomService` that loads an SBOM by ID and returns a not-found error, so the compare service shares the existing fetch path

## Files to Create
- `modules/fundamental/src/sbom/model/compare.rs` — `SbomComparison` response struct and item structs: `PackageDiffEntry { name, version, license, advisory_count }`, `VersionChangeEntry { name, left_version, right_version, direction }`, `VersionDirection` enum (`upgrade` / `downgrade`), `NewVulnerabilityEntry { advisory_id, severity, title, affected_package }`, `ResolvedVulnerabilityEntry { advisory_id, severity, title, previously_affected_package }`, `LicenseChangeEntry { name, left_license, right_license }`
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomService::compare(left_id, right_id, db)` (or a dedicated `SbomCompareService`) implementing the diff algorithm

## Implementation Notes
- **Response shape contract** (must match exactly, consumed by trustify-ui Task 3 — field names are snake_case on the wire):
  ```json
  {
    "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..." }],
    "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
    "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
  }
  ```
  Derive `serde::Serialize` (and `utoipa::ToSchema` if the sibling models `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` / `details.rs::SbomDetails` derive it) following the existing model structs. Serialize `VersionDirection` as lowercase (`#[serde(rename_all = "lowercase")]`).
- **Data sources (existing entities, no migrations):**
  - Packages per SBOM: `entity/src/sbom_package.rs` (SBOM–Package join) + `entity/src/package.rs`
  - Licenses: `entity/src/package_license.rs` (the `license` field also surfaces on `modules/fundamental/src/package/model/summary.rs::PackageSummary`)
  - Advisories per SBOM: `entity/src/sbom_advisory.rs` (SBOM–Advisory join) + `entity/src/advisory.rs`; severity comes from the same source as `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary.severity`
- **Diff algorithm:** key packages by package name. Load both package sets with one query each (not per-package queries) and build `HashMap<name, (version, license)>`; then:
  - added = names in right only; removed = names in left only
  - version_changes = names in both with different versions; `direction` determined by semantic-version comparison, falling back to lexical comparison when versions are not semver
  - license_changes = names in both with different license values
  - new_vulnerabilities = advisory IDs linked to the right SBOM but not the left; resolved_vulnerabilities = advisory IDs linked to the left but not the right; populate `affected_package` / `previously_affected_package` from the package the advisory is correlated to
  - `advisory_count` on added/removed entries = number of advisories linked to that package in the respective SBOM
- **Performance (NFR p95 < 1s at 2000 packages per SBOM):** issue a bounded number of queries (packages left, packages right, advisories left, advisories right) and diff in memory with `HashMap`/`HashSet` (O(n)). Avoid N+1 queries. Reuse the query helpers in `common/src/db/query.rs` where they apply to filtering by SBOM ID.
- **Error handling:** if either SBOM ID does not exist, return `AppError` not-found (from `common/src/error.rs`) — never an empty diff. Wrap DB errors with `.context(...)`.
- **Per CONVENTIONS.md §Module pattern:** place the new types under `sbom/model/` and the logic under `sbom/service/`, mirroring `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/service/sbom.rs`.
  Applies: task modifies modules/fundamental/src/sbom/service/compare.rs matching the convention's Rust domain-module (`model/ + service/ + endpoints/`) scope.
- **Per CONVENTIONS.md §Error handling:** service functions return `Result<_, AppError>` and wrap fallible calls with `.context()`, as done in `modules/fundamental/src/sbom/service/sbom.rs`.
  Applies: task modifies modules/fundamental/src/sbom/service/compare.rs matching the convention's Rust handler/service `.rs` scope.
- **Constraints (docs/constraints.md):** §2 commits — Conventional Commits, Jira ID footer (`Implements <task-key>`), `Assisted-by:` trailer; §3 PRs — branch named after the task key, `gh pr create --base main`, post PR link on the Jira task; §5 code changes — stay within Files to Modify/Create, inspect before modifying, no duplication of existing fetch/query logic (§5.4), trace the data flow end-to-end (§5.6), compare against sibling services for parity (§5.8); §1.4/1.5 implement-task scope rules.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing SBOM fetch logic; reuse to validate SBOM existence and load SBOM records
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package fetch/list logic; reuse its query construction for loading packages scoped to an SBOM instead of writing new raw queries
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing advisory fetch logic including severity; reuse for loading advisories by SBOM
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — already exposes name/version/license; map from it rather than re-deriving license data
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — already exposes severity and title
- `common/src/db/query.rs` — shared filtering helpers
- `common/src/error.rs::AppError` — not-found / internal error variants

## Acceptance Criteria
- [ ] `SbomComparison` and the six entry structs exist and serialize to exactly the JSON field names listed in Implementation Notes
- [ ] Packages only in the right SBOM appear in `added_packages`; only in the left appear in `removed_packages`
- [ ] Packages in both with different versions appear in `version_changes` with correct `upgrade`/`downgrade` direction
- [ ] Packages in both with different licenses appear in `license_changes`
- [ ] Advisories linked to right but not left appear in `new_vulnerabilities` with severity, title, affected package; advisories linked to left but not right appear in `resolved_vulnerabilities`
- [ ] Comparing an SBOM with itself returns six empty arrays
- [ ] A non-existent left or right SBOM ID yields a not-found `AppError` (fail-closed) rather than an empty diff
- [ ] No new tables or migrations are added
- [ ] Diff uses a bounded number of queries independent of package count (no N+1)

## Test Requirements
- [ ] Unit tests for the in-memory diff function covering: added, removed, version upgrade, version downgrade, non-semver version change, license change, new advisory, resolved advisory, identical SBOMs (empty diff)
- [ ] Test that an unknown SBOM ID returns a not-found error and not an empty `SbomComparison` (fail-closed path)
- [ ] Test that serialization of `SbomComparison` produces the snake_case field names and lowercase `direction` values

## Verification Commands
- `cargo test -p trustify-module-fundamental compare` — new diff tests pass
- `cargo clippy --all-targets -- -D warnings` — no warnings

## Dependencies
- None
