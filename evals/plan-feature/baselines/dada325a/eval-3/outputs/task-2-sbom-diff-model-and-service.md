# Task 2 — Add SBOM comparison model and diff service

**Summary:** Add SBOM comparison response model and on-the-fly diff computation in SbomService
**Epic:** TC-9003: SBOM diff API

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the domain model and service logic that computes a structured diff between two SBOMs. The diff covers added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. It is built on the fly from existing package, license, and advisory data, with no new database tables (Feature NFR). This is the backend core of TC-9003. Task 3 exposes it over HTTP.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export the new `compare` model module
- `modules/fundamental/src/sbom/service/mod.rs` — declare and re-export the new `compare` service module
- `modules/fundamental/src/sbom/service/sbom.rs` — add a `SbomService::compare(left_id, right_id)` entry point (or delegate to the new compare module) next to the existing fetch/list methods

## Files to Create
- `modules/fundamental/src/sbom/model/compare.rs` — `SbomComparison` response struct plus row structs: `PackageDiffEntry`, `VersionChangeEntry` (with a `VersionChangeDirection` enum), `NewVulnerabilityEntry`, `ResolvedVulnerabilityEntry`, `LicenseChangeEntry`
- `modules/fundamental/src/sbom/service/compare.rs` — diff algorithm: load the package sets of both SBOMs, key them by package name, and compute the six categories

## Implementation Notes
**Response shape (must match the Figma-documented contract that the frontend Task 4 consumes):**
```json
{
  "added_packages":   [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
  "removed_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
  "version_changes":  [{ "name": "string", "left_version": "string", "right_version": "string", "direction": "upgrade" | "downgrade" }],
  "new_vulnerabilities":      [{ "advisory_id": "string", "severity": "critical|high|medium|low", "title": "string", "affected_package": "string" }],
  "resolved_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "previously_affected_package": "string" }],
  "license_changes":  [{ "name": "string", "left_license": "string", "right_license": "string" }]
}
```
Derive `Serialize` (snake_case field names, as shown) and `utoipa::ToSchema` if the existing `SbomSummary` / `SbomDetails` structs do. Mirror their derives in `modules/fundamental/src/sbom/model/summary.rs` and `details.rs`. Serialize `VersionChangeDirection` as lowercase `upgrade` / `downgrade`.

**Diff semantics:**
- *Added*: package name present in right, absent in left. *Removed*: present in left, absent in right.
- *Version change*: name present in both with a different version. Set `direction` by comparing versions semver-aware, falling back to lexical comparison for non-semver versions. Document the fallback in a code comment.
- *License change*: name present in both with a different license, taken from `PackageSummary`'s license field and the `entity/src/package_license.rs` mapping.
- *New vulnerabilities*: advisories linked to the right SBOM (`entity/src/sbom_advisory.rs`) that are not linked to the left. *Resolved vulnerabilities*: the reverse. Take `severity` and `title` from `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`, which has a severity field).
- `advisory_count` on added/removed rows is the number of advisories affecting that package within its SBOM.

**Data source / open item:** the entity layer has `sbom_package.rs`, `package.rs`, `package_license.rs`, and `sbom_advisory.rs`. No package-to-advisory join entity is visible. Before deciding how to compute `affected_package` / `previously_affected_package` and `advisory_count`, check how `modules/ingestor/src/graph/advisory/mod.rs` correlates advisories to packages. If the correlation only exists at SBOM level, raise it on TC-9003 before you implement anything. Do not emit empty strings for those fields.

**Performance (NFR: p95 < 1s at 2000 packages per SBOM):**
- Load each SBOM's packages, with licenses, in a single query per SBOM, joining `sbom_package` → `package` → `package_license`. Load advisories for both SBOMs in one query. Do not run per-package queries (N+1).
- Compute the diff in memory with `HashMap<name, …>` / `HashSet` lookups (O(n)).
- Sort every output list deterministically (by package name, or by advisory ID) so responses are stable and testable.

**Fail-closed behavior:** if either SBOM ID does not exist, return `AppError` not-found (it maps to 404 via `IntoResponse` in `common/src/error.rs`). Never return an empty `SbomComparison`. An empty diff must mean "no differences", never "SBOM not found". Put this guard at the top of the new `compare` service function, before any diffing.

**Conventions:**
- Per CONVENTIONS.md §Module pattern: put the new types under `sbom/model/` and the logic under `sbom/service/`, following the existing `model/ + service/ + endpoints/` split. See `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/service/sbom.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust domain-module (`modules/*/src/<domain>/`) scope.
- Per CONVENTIONS.md §Error handling: return `Result<SbomComparison, AppError>` and wrap database errors with `.context("…")`, as in the existing fetch methods of `SbomService`.
  Applies: task modifies `modules/fundamental/src/sbom/service/compare.rs` matching the convention's Rust handler/service (`.rs`) scope.
- Per CONVENTIONS.md §Framework: use SeaORM entity queries (`entity::sbom_package`, `entity::package`, `entity::package_license`, `entity::sbom_advisory`) rather than raw SQL.
  Applies: task modifies `modules/fundamental/src/sbom/service/compare.rs` matching the convention's Rust/SeaORM (`.rs`) scope.

**Project constraints (docs/constraints.md):**
- §2: Conventional Commits; the footer references the Jira task (`Implements TC-XXXX`); include the `Assisted-by:` trailer.
- §3: Open the PR with `gh pr create --base TC-9003` and post the PR link on the Jira task.
- §5: Change only the files listed here. Inspect code before modifying it. Reuse the existing service and query helpers rather than duplicating them. Trace the full data flow (SBOM IDs → queries → diff → struct).

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing fetch logic for an SBOM by ID. Reuse it for the existence check / not-found handling.
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package fetch/list. Reuse its query or `PackageSummary` mapping to load an SBOM's packages with licenses.
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — already carries the `license` field. Reuse it as the source of name/version/license.
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` and `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — advisory lookup with severity and title.
- `common/src/db/query.rs` — shared query/filter helpers. Reuse them for SBOM-scoped package filtering instead of hand-rolled conditions.
- `common/src/error.rs::AppError` — error type for the not-found path.

## Acceptance Criteria
- [ ] `SbomComparison` and its row structs serialize to exactly the JSON shape above, with snake_case keys and lowercase `direction`
- [ ] Added and removed packages are computed correctly by package name
- [ ] Version changes report `left_version`, `right_version`, and the correct `upgrade` / `downgrade` direction
- [ ] New and resolved vulnerabilities carry the advisory ID, severity, title, and affected package
- [ ] License changes are reported for packages present in both SBOMs whose license differs
- [ ] Requesting a non-existent left or right SBOM ID returns a not-found `AppError`, not an empty diff (fail-closed)
- [ ] Comparing an SBOM with itself returns six empty lists
- [ ] No new migrations or database tables are added
- [ ] Package and advisory data are loaded with a fixed number of queries, independent of package count (no N+1)

## Test Requirements
- [ ] Unit tests for the in-memory diff function: added, removed, version upgrade, version downgrade, license change, and no change
- [ ] Unit test: identical inputs produce six empty lists
- [ ] Unit test: version-direction fallback for non-semver strings
- [ ] Unit test: a non-existent SBOM ID returns a not-found error and does not produce an empty `SbomComparison` (fail-closed path)
- [ ] Unit test: output lists are deterministically sorted

## Verification Commands
- `cargo build -p trustify-module-fundamental` (or the crate's actual package name from `modules/fundamental/Cargo.toml`) — compiles without errors
- `cargo test -p trustify-module-fundamental compare` — all new unit tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
