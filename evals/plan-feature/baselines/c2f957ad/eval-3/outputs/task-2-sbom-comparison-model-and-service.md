# Task 2 — Add SBOM comparison model and diff service

**Summary:** Add SBOM comparison model and diff computation in SbomService
**Issue type:** Task | **Parent (Epic):** Epic A — TC-9003: SBOM diff API
**Labels:** ai-generated-jira | **Priority:** Critical | **Fix Versions:** RHTPA 1.5.0

---

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Introduce the domain model and service logic that computes a structured diff between two SBOMs. Given a left and right SBOM id, the service returns: packages added (in right, not in left), packages removed (in left, not in right), version changes (same package name, different version, with upgrade/downgrade direction), new vulnerabilities (advisories affecting right but not left), resolved vulnerabilities (advisories affecting left but not right), and license changes (same package, different license).

Per the feature's non-functional requirements, the diff is computed on the fly from existing package, license and advisory data — **no new database tables or migrations** — and must support a p95 < 1s for SBOMs with up to 2000 packages each. This task delivers the model and service only; the HTTP endpoint is Task 3.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export the new `comparison` module
- `modules/fundamental/src/sbom/service/sbom.rs` — add `SbomService::compare(left_id, right_id, ...)` returning `SbomComparison`

## Files to Create
- `modules/fundamental/src/sbom/model/comparison.rs` — `SbomComparison` response struct and item structs: `AddedPackage`/`RemovedPackage` (`name`, `version`, `license`, `advisory_count`), `VersionChange` (`name`, `left_version`, `right_version`, `direction`), `VersionDirection` enum (`upgrade`, `downgrade`), `NewVulnerability` (`advisory_id`, `severity`, `title`, `affected_package`), `ResolvedVulnerability` (`advisory_id`, `severity`, `title`, `previously_affected_package`), `LicenseChange` (`name`, `left_license`, `right_license`)

## Implementation Notes
- **Response contract** (must match the Figma backend-interaction shape exactly — snake_case field names, consumed verbatim by trustify-ui in Task 4):
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
  Derive `Serialize` (serde, `rename_all = "snake_case"` on `VersionDirection`) following the existing structs in `modules/fundamental/src/sbom/model/summary.rs` and `details.rs`. Every list is always present (empty array, never omitted/null).
- **Data sources (existing entities, no migration):**
  - Packages per SBOM: `entity/src/sbom_package.rs` join → `entity/src/package.rs`
  - License per package: `entity/src/package_license.rs`
  - Advisories per SBOM: `entity/src/sbom_advisory.rs` join → `entity/src/advisory.rs`; severity from the same field exposed on `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`)
- **Algorithm:** load both SBOMs' package sets with one query each (no per-package N+1 queries), build `HashMap<package_name, (version, license)>` per side, then derive added/removed/version/license changes by set difference/intersection. Advisories: build `HashSet<advisory_id>` per side and diff. `advisory_count` = number of advisories linked to that package in its SBOM. Version `direction`: compare versions with a semver-aware comparison (fall back to lexical comparison for non-semver strings) — document the fallback in code.
- **Advisory → package attribution:** `affected_package` / `previously_affected_package` require knowing which package an advisory affects within the SBOM. Verify at implementation time whether `sbom_advisory` (or the advisory correlation done in `modules/ingestor/src/graph/advisory/mod.rs`) records the package; if the link is only SBOM-level, raise it on the task before inventing a new relation (no new tables allowed).
- **Fail closed on missing input:** if either SBOM id does not exist, return an error (`AppError` not-found variant from `common/src/error.rs`) — never an empty diff, which would look like "no changes".
- **Performance:** keep the work to a bounded number of queries (≈2 package queries + 2 advisory queries); compute the diff in memory. Use the existing pagination-free query helpers in `common/src/db/query.rs` where they fit.
- Per CONVENTIONS.md §Module pattern: place the new struct under `sbom/model/` and the logic under `sbom/service/`, keeping the `model/ + service/ + endpoints/` split; follow `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/service/sbom.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust domain-module (`modules/*/src/<domain>/`) scope.
- Per CONVENTIONS.md §Error handling: return `Result<SbomComparison, AppError>` and wrap database errors with `.context()`, as existing `SbomService` fetch methods do.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust (`.rs`) handler/service scope.
- Per CONVENTIONS.md §Query helpers: reuse `common/src/db/query.rs` helpers for any filtering instead of hand-rolled query building.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust (`.rs`) database-query scope.
- Constraints (docs/constraints.md): §1.4/§1.5 keep changes scoped and inspect code before modifying; §2.1–2.3 commits reference TC Jira id in footer, Conventional Commits, `Assisted-by:` trailer; §3.1/§3.3/§3.4 branch naming and `gh pr create --base TC-9003`; §5.1–5.8 scope to listed files, no duplication of existing logic, trace the data flow end to end, sibling parity on error handling/logging.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing fetch logic for an SBOM by id; reuse it to validate that both ids exist and to load package links
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package fetch/list logic (name, version, license) — reuse its query/mapping rather than duplicating package loading
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — already carries the `license` field; reuse its mapping from entity → model
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — advisory fetch/list incl. severity; reuse for advisory lookups
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — source of `severity` and title fields
- `common/src/db/query.rs` — shared query builder helpers
- `common/src/error.rs::AppError` — not-found / bad-request error variants

## Acceptance Criteria
- [ ] `SbomComparison` serializes to exactly the six snake_case top-level arrays and item fields in the contract above
- [ ] Packages only in the right SBOM appear in `added_packages`; only in the left in `removed_packages`
- [ ] Packages in both with different versions appear in `version_changes` with correct `direction` (`upgrade`/`downgrade`)
- [ ] Packages in both with different licenses appear in `license_changes`
- [ ] Advisories affecting only the right SBOM appear in `new_vulnerabilities`; only the left in `resolved_vulnerabilities`, each with severity, title and affected package
- [ ] `advisory_count` reflects advisories linked to the package
- [ ] Comparing an SBOM with itself returns six empty arrays
- [ ] A non-existent left or right id returns a not-found `AppError`, not an empty diff
- [ ] No new tables, entities or migrations are added
- [ ] The number of DB queries is constant with respect to package count (no N+1)

## Test Requirements
- [ ] Unit tests for the diff computation covering: added, removed, version upgrade, version downgrade, license change, new vulnerability, resolved vulnerability, identical SBOMs (all empty)
- [ ] Unit test for version direction with semver and non-semver version strings
- [ ] Test that a missing SBOM id yields a not-found error rather than an empty `SbomComparison`

## Verification Commands
- `cargo build -p trustify-module-fundamental` (or workspace `cargo build`) — compiles without errors
- `cargo test -p trustify-module-fundamental sbom` — new comparison tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
