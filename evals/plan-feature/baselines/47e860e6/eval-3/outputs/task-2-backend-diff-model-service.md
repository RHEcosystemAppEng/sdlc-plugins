# Task 2 — Backend: SBOM comparison model and diff service

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the response model and service logic that compute a structured diff between two SBOMs. The comparison is computed on the fly from existing package, license and advisory data, with no new database tables. It produces six categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities and license changes. This is the domain layer behind the new `GET /api/v2/sbom/compare` endpoint (Task 3) that backs the SBOM comparison view of TC-9003.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs`: declare and re-export the new `compare` model module
- `modules/fundamental/src/sbom/service/sbom.rs`: add `SbomService::compare(left_id, right_id, ...)`, which loads both SBOMs' package and advisory sets and computes the diff
- `modules/fundamental/src/sbom/service/mod.rs`: expose any new service helpers if the diff logic is split into a helper module

## Files to Create
- `modules/fundamental/src/sbom/model/compare.rs`: `SbomComparison` response struct and item structs: `AddedPackage` and `RemovedPackage` (or a shared `PackageDiffEntry`), `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`, and a `VersionChangeDirection` enum (`upgrade` / `downgrade`)

## Implementation Notes
- **Response shape:** this is the contract the frontend relies on (from the Figma "Expected response shape"). Serialize with snake_case field names exactly as below:
  - `added_packages` / `removed_packages`: `[{ name, version, license, advisory_count }]`
  - `version_changes`: `[{ name, left_version, right_version, direction }]`, where `direction` serializes as `"upgrade"` / `"downgrade"` (use `#[serde(rename_all = "lowercase")]` on the enum)
  - `new_vulnerabilities`: `[{ advisory_id, severity, title, affected_package }]`
  - `resolved_vulnerabilities`: `[{ advisory_id, severity, title, previously_affected_package }]`
  - `license_changes`: `[{ name, left_license, right_license }]`
- **Diff algorithm:** to meet p95 < 1s at 2000 packages per SBOM:
  1. For each SBOM, load all packages with their licenses in **one bulk query**. Join `entity/src/sbom_package.rs` to `entity/src/package.rs` to `entity/src/package_license.rs`. Do not issue per-package queries (no N+1).
  2. For each SBOM, load all linked advisories in one bulk query via `entity/src/sbom_advisory.rs` to `entity/src/advisory.rs`, including severity and title.
  3. Build `HashMap<package_name, PackageInfo>` for left and right. Then classify: name only in right means added; only in left means removed; in both with a different version means a version change; in both with a different license means a license change. A package can appear in both the version and license categories.
  4. Vulnerabilities: take the advisory ID set difference. In right but not left means new; in left but not right means resolved.
  5. Total cost is about 4 queries plus O(n) in-memory work.
- **Version direction:** compare versions with semver-style ordering when both parse. Otherwise fall back to a lexical comparison. The Figma defines only `upgrade`/`downgrade`.
- **Advisory to package correlation:** `affected_package` and `advisory_count` need advisories mapped to packages. The entity list shows only the SBOM-level `sbom_advisory` join. Before coding, check how `modules/ingestor/src/graph/advisory/mod.rs` ("parse, store, correlate") persists package-level correlation, and use that relation. If no persisted package-level relation exists, stop and raise it on TC-9003. The NFR forbids new tables, so this is a scope decision (see open question 3 in the impact map).
- **Error handling:** if either SBOM ID does not exist, return `AppError` not-found (`common/src/error.rs`). **Never** return an empty diff for a missing SBOM. An empty diff must mean "the two existing SBOMs are identical", never "a lookup silently found nothing".
- **Observability:** log comparison duration and package counts at `debug`/`info` level, using the existing tracing setup. This supports the future timeout monitoring requirement, which is excluded here for lack of a target repo.
- **No migration:** do not add anything under `migration/`.
- Per CONVENTIONS.md §Module pattern: place the new model in `sbom/model/` and the logic in `sbom/service/`, following the `model/ + service/ + endpoints/` structure. See `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/service/sbom.rs` for the established layout.
  Applies: task creates `modules/fundamental/src/sbom/model/compare.rs` matching the convention's domain module (`modules/*/src/<domain>/model|service/*.rs`) scope.
- Per CONVENTIONS.md §Error handling: return `Result<SbomComparison, AppError>` and wrap database errors with `.context()`. See `common/src/error.rs` (`AppError`) and the existing fetch path in `modules/fundamental/src/sbom/service/sbom.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust handler/service (`.rs`) scope.
- Per CONVENTIONS.md §Query helpers: reuse the shared helpers in `common/src/db/query.rs` for query construction where applicable, rather than hand-rolling query builders.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's database query (`.rs` service) scope.
- Constraints (docs/constraints.md): §1.4/§5.1 keep changes to the listed files; §5.2 inspect `SbomService`, the entities and the ingestor correlation code before modifying; §5.4 reuse the existing SBOM fetch, package and advisory model logic and do not duplicate it; §5.6 trace the data flow from DB rows to diff struct to serialized JSON; §5.8 match sibling services for error handling and logging; §2.1–2.3 commits use Conventional Commits, include `Implements TC-<task-key>`, and add the `Assisted-by: Claude Code` trailer; §3.3 open the PR with `--base TC-9003`.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService`: existing SBOM fetch logic. Reuse it to validate that both IDs exist and to load SBOM metadata.
- `modules/fundamental/src/package/model/summary.rs::PackageSummary`: already carries the `license` field. Reuse its mapping from entity to model for package name, version and license.
- `modules/fundamental/src/package/service/mod.rs::PackageService`: existing package fetch and list queries. Check them for a reusable "packages by SBOM" query.
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary`: includes `severity`. Reuse it for advisory severity and title instead of re-deriving them.
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService`: existing advisory fetch, list and search. Check it for an existing "advisories by SBOM" query.
- `common/src/db/query.rs`: shared query builder helpers.
- `common/src/error.rs::AppError`: error type for not-found and invalid-input cases.

## Acceptance Criteria
- [ ] `SbomComparison` serializes to the exact JSON shape above (six top-level arrays, snake_case fields, `direction` as `"upgrade"`/`"downgrade"`)
- [ ] Packages only in the right SBOM appear in `added_packages`; packages only in the left appear in `removed_packages`
- [ ] Packages in both with different versions appear in `version_changes` with the correct `direction`
- [ ] Packages in both with different licenses appear in `license_changes`
- [ ] Advisories affecting only the right SBOM appear in `new_vulnerabilities`; those affecting only the left appear in `resolved_vulnerabilities`, each with severity, title and affected package
- [ ] `advisory_count` on added and removed packages reflects the number of advisories affecting that package
- [ ] A non-existent left or right SBOM ID returns a not-found `AppError`, never an empty `SbomComparison` (fail-closed)
- [ ] Comparing an SBOM with itself returns six empty arrays
- [ ] Diff computation uses bulk queries (no per-package queries), and no migration or new table is added

## Test Requirements
- [ ] Unit tests for the diff computation covering each category: added, removed, upgrade, downgrade, license change, new vulnerability and resolved vulnerability
- [ ] Unit test: identical package and advisory sets produce empty arrays in every category
- [ ] Unit test: a package with both a version change and a license change appears in both categories
- [ ] Unit test: a non-parseable version string falls back to lexical comparison without panicking
- [ ] Test (fail-closed): calling `SbomService::compare` with a non-existent SBOM ID returns a not-found error and not `Ok` with empty arrays

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
