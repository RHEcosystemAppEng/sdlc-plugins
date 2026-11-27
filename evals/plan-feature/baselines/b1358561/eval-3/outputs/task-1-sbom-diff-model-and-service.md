# Task 1 — Add SBOM comparison model and diff service

**Summary:** TC-9003: Add SBOM comparison model and diff computation service
**Issue type:** Task
**Parent (Epic):** Epic 1 — TC-9003: SBOM comparison diff API
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003)

---

## Repository
trustify-backend

## Target Branch
main

## Description
Introduce the domain model and service logic that computes a structured diff between two
SBOMs (left = baseline, right = target). This is the backend core of TC-9003 "SBOM comparison
view". The diff is computed on-the-fly from existing package, license and advisory data —
no new database tables or migrations (Non-Functional Requirement of TC-9003).

The diff must contain six categories:
- **added_packages** — packages present in the right SBOM but not the left
- **removed_packages** — packages present in the left SBOM but not the right
- **version_changes** — packages present in both (matched by package name) with different versions, including direction (`upgrade` / `downgrade`)
- **new_vulnerabilities** — advisories affecting the right SBOM that did not affect the left
- **resolved_vulnerabilities** — advisories that affected the left SBOM but not the right
- **license_changes** — packages present in both whose license changed

This task delivers the model and service only; the HTTP endpoint is Task 2.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export the new `comparison` module
- `modules/fundamental/src/sbom/service/mod.rs` — declare and re-export the new `compare` service module
- `modules/fundamental/src/sbom/service/sbom.rs` — expose (or reuse) the SBOM fetch-by-id lookup so the comparison service can verify both SBOMs exist before diffing

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — `SbomComparison` response struct plus item structs: `AddedPackage`/`RemovedPackage` (`name`, `version`, `license`, `advisory_count`), `VersionChange` (`name`, `left_version`, `right_version`, `direction`), `VersionChangeDirection` enum (`upgrade` / `downgrade`, serialized lowercase), `NewVulnerability` (`advisory_id`, `severity`, `title`, `affected_package`), `ResolvedVulnerability` (`advisory_id`, `severity`, `title`, `previously_affected_package`), `LicenseChange` (`name`, `left_license`, `right_license`)
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomService::compare(left_id, right_id)` (or a dedicated `SbomCompareService`) that loads both SBOMs' packages/licenses/advisories and computes the diff

## Implementation Notes
- **Response shape (contract shared with the frontend — Figma "Backend Interactions"):**
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
  Field names are snake_case; derive `serde::Serialize` (plus `utoipa::ToSchema` if the module's existing structs in `model/summary.rs` / `model/details.rs` derive it — follow sibling structs).
- **Data sources (entity layer, SeaORM):**
  - Packages per SBOM: `entity/src/sbom_package.rs` (SBOM↔Package join) + `entity/src/package.rs`
  - Licenses: `entity/src/package_license.rs`; `PackageSummary` in `modules/fundamental/src/package/model/summary.rs` already carries the `license` field — reuse its mapping logic rather than re-implementing license resolution
  - Advisories per SBOM: `entity/src/sbom_advisory.rs` (SBOM↔Advisory join) + `entity/src/advisory.rs`; `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` carries `severity` — reuse it for severity/title values
- **Performance (NFR: p95 < 1s for up to 2000 packages per SBOM):** issue a bounded number of set-based queries — one query per SBOM for packages+licenses and one per SBOM for advisories (joined to the affected package) — then diff in memory using `HashMap<String /*package name*/, …>` / `HashSet<advisory_id>`. Do NOT issue per-package queries (N+1). Total work is O(n) in the number of packages.
- **Diff rules:**
  - Match packages across SBOMs by package name (PURL without version when available). Same name + different version → `version_changes`, not added+removed.
  - `direction`: compare versions semver-aware where parseable; fall back to lexical comparison when not parseable and document that fallback in a code comment.
  - `advisory_count` for added/removed packages = number of advisories linked to that package in the SBOM it belongs to.
  - New/resolved vulnerabilities are keyed by `(advisory_id, package name)` set difference between right and left.
  - `license_changes` only for packages present in both SBOMs whose license string differs.
  - Sort each list deterministically (by package name / advisory id) so responses and tests are stable.
- **Fail-closed on missing SBOMs:** before diffing, look up both SBOMs via the existing fetch in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService`). If either does not exist, return `AppError` not-found — never return an empty diff for a non-existent ID (an empty diff would silently read as "no changes"). Guard site: the start of the `compare` function in `service/compare.rs`.
- Comparing an SBOM with itself is valid and returns six empty lists.
- Per CONVENTIONS.md §Module pattern: place the new struct under `sbom/model/` and the diff logic under `sbom/service/`, mirroring `sbom/model/summary.rs` and `sbom/service/sbom.rs`.
  Applies: task creates `modules/fundamental/src/sbom/model/comparison.rs` matching the convention's domain-module `model/ + service/ + endpoints/` Rust file scope.
- Per CONVENTIONS.md §Error handling: service functions return `Result<SbomComparison, AppError>` and wrap database errors with `.context("…")`; see `common/src/error.rs` (`AppError`) and `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` for the established pattern.
  Applies: task creates `modules/fundamental/src/sbom/service/compare.rs` matching the convention's Rust handler/service `.rs` scope.
- Constraints (docs/constraints.md): §5.1 keep changes scoped to the listed files; §5.2 inspect `SbomService`, `PackageSummary` and `AdvisorySummary` before modifying; §5.4 reuse existing license/severity mapping rather than duplicating; §2.1–2.3 commits reference TC task key, use Conventional Commits, include `Assisted-by:` trailer; §3.3 PR `--base main`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing SBOM fetch/list; reuse fetch-by-id for existence checks and the DB connection handling pattern
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — already maps package + license; reuse for name/version/license projection
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — already exposes `severity` and title; reuse for vulnerability item fields
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package query logic; check for a "packages by SBOM" query before writing a new one
- `common/src/db/query.rs` — shared query builder helpers; reuse for filtering joins
- `common/src/error.rs::AppError` — not-found / database error variants

## Acceptance Criteria
- [ ] `SbomComparison` and its item structs serialize to exactly the JSON shape above (snake_case field names, `direction` serialized as `"upgrade"` / `"downgrade"`)
- [ ] Packages only in the right SBOM appear in `added_packages`; only in the left in `removed_packages`
- [ ] A package present in both with different versions appears only in `version_changes` (not in added/removed) with the correct `direction`
- [ ] Advisories affecting right-but-not-left appear in `new_vulnerabilities`; left-but-not-right in `resolved_vulnerabilities`, each with `severity` and `title` from the advisory data
- [ ] Packages present in both with a different license appear in `license_changes`
- [ ] Comparing an SBOM with itself yields six empty lists
- [ ] If either SBOM ID does not exist, the service returns a not-found `AppError` instead of an empty diff (fail-closed)
- [ ] No new database tables, entities, or migrations are introduced
- [ ] The number of DB queries is constant with respect to package count (no per-package queries)

## Test Requirements
- [ ] Unit tests for the in-memory diff function covering each of the six categories with hand-built package/advisory sets
- [ ] Unit test: same package, different version → only in `version_changes`; verify `upgrade` and `downgrade` direction, including a non-semver version fallback
- [ ] Unit test: identical inputs → all six lists empty
- [ ] Unit test: non-existent left or right SBOM ID → not-found error, not an empty `SbomComparison` (fail-closed path)
- [ ] Serialization test asserting the JSON field names match the contract above

## Dependencies
- None
