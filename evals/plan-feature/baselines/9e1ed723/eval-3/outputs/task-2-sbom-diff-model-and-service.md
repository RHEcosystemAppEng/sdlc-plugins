# Task 2 — Add SBOM comparison model and diff service

**Summary:** Add SBOM comparison response model and on-the-fly diff service
**Epic:** TC-9003: SBOM diff API
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003; fixVersion scope = both)

---

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Implement the domain model and service logic that computes a structured diff between two SBOMs. This is the core of feature TC-9003 (SBOM comparison view): given a left and a right SBOM ID, produce added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes.

Per the feature's non-functional requirements, the diff must be computed on-the-fly from existing package and advisory data — **no new database tables or migrations** — and must support SBOMs with up to 2000 packages each within a p95 < 1s budget for the full endpoint (Task 3 exposes this service over HTTP).

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export the new `compare` model module
- `modules/fundamental/src/sbom/service/mod.rs` — declare and re-export the new `compare` service module

## Files to Create
- `modules/fundamental/src/sbom/model/compare.rs` — `SbomComparison` response struct and its row structs (`AddedPackage`/`RemovedPackage` (or a shared `PackageDiffEntry`), `VersionChange`, `VersionDirection`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`)
- `modules/fundamental/src/sbom/service/compare.rs` — diff computation (`SbomService::compare(left_id, right_id, tx)` or a dedicated `SbomCompareService`), with unit tests in a `#[cfg(test)]` module for the pure diffing functions

## Implementation Notes
**Response shape** (must match the contract consumed by the frontend, from the Figma design context):

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

- Use `#[serde(rename_all = "snake_case")]` on structs and serialize `VersionDirection` as lowercase `"upgrade"` / `"downgrade"`. Severity must be serialized with the same representation already used by `AdvisorySummary.severity` in `modules/fundamental/src/advisory/model/summary.rs` (the Figma contract shows lowercase `"critical"`) — reuse that type rather than introducing a new severity enum.
- Follow the existing model layout: sibling structs `SbomSummary` (`modules/fundamental/src/sbom/model/summary.rs`) and `SbomDetails` (`modules/fundamental/src/sbom/model/details.rs`) show the derive set and serialization conventions to replicate.

**Diff algorithm (data sources — read-only):**
- Packages per SBOM: `entity/src/sbom_package.rs` (SBOM–Package join) joined with `entity/src/package.rs`.
- Licenses: `entity/src/package_license.rs` (Package–License mapping); `PackageSummary` in `modules/fundamental/src/package/model/summary.rs` already exposes a `license` field — reuse its mapping logic.
- Advisories per SBOM: `entity/src/sbom_advisory.rs` (SBOM–Advisory join) joined with `entity/src/advisory.rs`. Verify whether `sbom_advisory` records the affected package; if it does not, derive `affected_package` by intersecting the advisory's affected packages with the SBOM's packages. Do not leave `affected_package` empty silently — if it cannot be derived, raise this with the reviewer before merging.
- Identity: match packages across SBOMs by package name. `added` = names only in right; `removed` = names only in left; `version_changes` = names in both with differing versions; `license_changes` = names in both with differing license. Advisories: `new` = advisory IDs affecting right but not left; `resolved` = advisory IDs affecting left but not right.
- `advisory_count` on added/removed rows = number of advisories linked to that package within the respective SBOM.
- `direction`: compare versions semantically (semver-aware where parseable, fall back to lexical comparison) — document the fallback in a code comment.
- Edge case: an SBOM may contain multiple versions of the same package name; treat each `(name, version)` pair deterministically (e.g., report a version change only when the version sets differ) and cover it with a unit test.

**Performance (NFR p95 < 1s for 2000 packages each):** fetch each SBOM's package set, license set, and advisory set with a bounded number of queries (one query per data set per SBOM, no per-package N+1 queries), then diff in memory using `HashMap`/`HashSet`. Reuse the shared query helpers in `common/src/db/query.rs` for query construction.

**Error handling:** per the repo convention, return `Result<T, AppError>` (`common/src/error.rs`) and wrap fallible DB calls with `.context()`. If either SBOM ID does not exist, return a not-found `AppError` variant — never an empty diff (see fail-closed criteria below).

**Fail-closed coverage:** a missing or unknown SBOM ID must not produce a "green" empty diff (`{ added_packages: [], ... }`), because the UI would render "no changes" and mislead a compliance reviewer. The guard belongs at the top of the compare function in `modules/fundamental/src/sbom/service/compare.rs`, which must look up both SBOMs (reuse the fetch logic in `SbomService`, `modules/fundamental/src/sbom/service/sbom.rs`) before computing the diff.

**Shared-artifact note:** the diff is a read-only consumer of `sbom_package`, `sbom_advisory`, and `package_license`. These are populated by `modules/ingestor/src/graph/sbom/mod.rs` (SBOM ingestion: packages and licenses) and `modules/ingestor/src/graph/advisory/mod.rs` (advisory ingestion/correlation: `sbom_advisory`). No producer changes are required; the vulnerability sections reflect the current correlation state at query time.

**Conventions:**
- Per CONVENTIONS.md §Module pattern: place the model in `sbom/model/` and the logic in `sbom/service/`, keeping the `model/ + service/ + endpoints/` structure. Applies: task modifies `modules/fundamental/src/sbom/model/compare.rs` matching the convention's domain module (`modules/*/src/<domain>/`) scope. Example: `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` and use `.context()` on every fallible call. Applies: task modifies `modules/fundamental/src/sbom/service/compare.rs` matching the convention's Rust handler/service (`.rs`) scope. Example: `common/src/error.rs` and existing calls in `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Query helpers: build filtering queries with `common/src/db/query.rs` rather than ad-hoc SQL. Applies: task modifies `modules/fundamental/src/sbom/service/compare.rs` matching the convention's Rust database-access (`.rs`) scope.

**Project constraints (docs/constraints.md):**
- §2 Commit rules: Conventional Commits message, `Implements <task-key>` footer, `Assisted-by:` trailer.
- §3 PR rules: `gh pr create --base TC-9003`; post the PR link on the Jira task.
- §5 Code change rules: limit changes to the listed files; inspect code before modifying; reuse existing helpers (no duplicated package/license/advisory lookups); compare against sibling services for error-handling parity.
- §1.4/§1.5: keep scope to this task; inspect `SbomService` and entities before writing code.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing SBOM fetch logic; reuse it to validate both IDs exist and to load SBOM metadata
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package fetch/list logic; reuse its package + license loading for an SBOM rather than re-querying from scratch
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — already carries `license`; reuse its conversion from entity to model
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — advisory fetch/list/search; reuse to load advisory title and severity
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — includes the `severity` field and type to reuse in vulnerability rows
- `common/src/db/query.rs` — shared query builder helpers (filtering)
- `common/src/error.rs::AppError` — error type for not-found handling

## Acceptance Criteria
- [ ] `SbomComparison` serializes to exactly the six snake_case keys of the agreed contract (`added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`)
- [ ] Packages only in the right SBOM appear in `added_packages`; only in the left appear in `removed_packages`, each with name, version, license, and `advisory_count`
- [ ] Packages present in both with different versions appear in `version_changes` with `left_version`, `right_version`, and `direction` (`upgrade` / `downgrade`)
- [ ] Advisories affecting right but not left appear in `new_vulnerabilities`; advisories affecting left but not right appear in `resolved_vulnerabilities`, each with advisory ID, severity, title, and affected package
- [ ] Packages present in both whose license differs appear in `license_changes`
- [ ] Comparing an SBOM with itself returns six empty arrays
- [ ] Fail-closed: when either SBOM ID does not exist, the service returns a not-found `AppError` instead of an empty diff
- [ ] No new database tables, entities, or migrations are introduced
- [ ] Data is loaded with a bounded number of queries per SBOM (no per-package queries)

## Test Requirements
- [ ] Unit tests for the pure diff functions: added, removed, version change (upgrade and downgrade), license change, new and resolved advisories, identical inputs → empty diff
- [ ] Unit test for the multiple-versions-of-same-package edge case
- [ ] Unit test for `direction` with non-semver version strings (fallback path)
- [ ] Unit test that serialization produces the snake_case contract keys and lowercase `direction`
- [ ] Fail-closed test: calling compare with a non-existent left ID, and separately a non-existent right ID, returns a not-found error and not an empty `SbomComparison`

## Verification Commands
- `cargo build -p trustify-module-fundamental` (or the crate name in `modules/fundamental/Cargo.toml`) — builds without errors
- `cargo test -p trustify-module-fundamental compare` — all new unit tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
