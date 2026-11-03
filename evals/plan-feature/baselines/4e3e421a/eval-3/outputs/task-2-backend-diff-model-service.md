# Task 2 — Add SBOM comparison diff model and service

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the response model types and service logic that compute a structured diff between two SBOMs, as part of TC-9003 (SBOM comparison view). The diff is computed on the fly from existing package, license, and advisory data; the NFRs forbid new database tables. It produces six categories: added packages, removed packages, version changes, new vulnerabilities, resolved vulnerabilities, and license changes. This task provides the domain logic. Task 3 exposes it over HTTP.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export the new `compare` model module
- `modules/fundamental/src/sbom/service/sbom.rs` — add `SbomService::compare(left_id, right_id)`, which loads both SBOMs' packages, licenses, and advisories and computes the diff

## Files to Create
- `modules/fundamental/src/sbom/model/compare.rs` — `SbomComparison`, `PackageDiffEntry`, `VersionChange`, `VersionDirection`, `VulnerabilityDiffEntry` (new) / `ResolvedVulnerabilityEntry`, `LicenseChange` structs (Serde `Serialize` + `utoipa::ToSchema` if the module already derives it)

## Implementation Notes
- **Response shape** (must match the frontend/Figma contract exactly; field names are snake_case):
  - `added_packages` / `removed_packages`: `{ name, version, license: Option<String>, advisory_count: u32 }`
  - `version_changes`: `{ name, left_version, right_version, direction: "upgrade" | "downgrade" }`. Serialize `VersionDirection` with `#[serde(rename_all = "lowercase")]`.
  - `new_vulnerabilities`: `{ advisory_id, severity, title, affected_package }`
  - `resolved_vulnerabilities`: `{ advisory_id, severity, title, previously_affected_package }`
  - `license_changes`: `{ name, left_license: Option<String>, right_license: Option<String> }`
  - `severity` must serialize as the same lowercase string `AdvisorySummary` already uses (e.g. `"critical"`). Reuse its severity type; do not add a parallel enum.
- **Data sources** (existing SeaORM entities):
  - `entity/src/sbom_package.rs` — packages in each SBOM
  - `entity/src/package.rs` — name and version
  - `entity/src/package_license.rs` — license per package
  - `entity/src/sbom_advisory.rs` and `entity/src/advisory.rs` — advisories per SBOM, with severity and title
  - Check how advisory-to-package correlation is stored. The ingestor correlates them in `modules/ingestor/src/graph/advisory/mod.rs`. Use that to fill `affected_package` and `advisory_count`.
- **Algorithm**:
  - Key packages by name (version-independent identity).
  - Load each side once into a `HashMap<name, (version, license)>`. Then:
    - added = keys only in right; removed = keys only in left
    - version_changes = keys in both with differing versions
    - license_changes = keys in both with differing licenses
  - Advisories:
    - new = advisory IDs linked to right but not left
    - resolved = linked to left but not right
- **Version direction**: compare with semver parsing where possible (the `semver` crate, if it is already in `Cargo.lock`). Otherwise fall back to a lexicographic segment comparison. Document the fallback in a code comment.
- **Performance (NFR p95 < 1s at 2000 packages per side)**:
  - Use a fixed number of bulk queries per SBOM: packages with licenses in one join, advisories in one join. Never query per package (no N+1).
  - Build queries with the shared helpers in `common/src/db/query.rs`, following the patterns in `SbomService` fetch/list.
  - Respect the connection limiter in `common/src/db/limiter.rs`.
- **Fail-closed behavior**: if either SBOM ID does not exist, `compare` must return an `AppError` not-found variant from `common/src/error.rs`. It must never return an empty `SbomComparison`, because an empty diff for a missing SBOM would look like "no changes".
- **Error handling**: follow the existing `Result<T, AppError>` + `.context()` pattern used in `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Module pattern: put the new types under `sbom/model/` and the logic under `sbom/service/`, keeping the `model/ + service/ + endpoints/` layout. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's domain module (`model/`, `service/`, `endpoints/`) scope. Example: `modules/fundamental/src/advisory/model/summary.rs` + `modules/fundamental/src/advisory/service/advisory.rs`.
- Per CONVENTIONS.md §Error handling: return `Result<SbomComparison, AppError>` and wrap DB errors with `.context()`. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust handler/service code scope. Example: existing fetch in `modules/fundamental/src/sbom/service/sbom.rs`.
- **Branch setup (cross-repo feature branch)**: if `TC-9003` does not exist in `trustify-backend`, create it from `main` and push it before you open this task's PR.
- Constraints (docs/constraints.md):
  - §2: Conventional Commits, a Jira footer (`Implements TC-xxxx`), and `--trailer="Assisted-by: Claude Code"`
  - §3: `gh pr create --base TC-9003`, and post the PR link to the Jira task
  - §5: change only the listed files, inspect code before modifying it, reuse existing helpers, and trace the full data flow

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing fetch logic to load an SBOM by ID and its related packages. Extend it rather than adding a new service.
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — already has name, version, and license. Reuse its field mapping or conversion when building `PackageDiffEntry`.
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — has `severity`. Reuse its severity type and serialization.
- `modules/fundamental/src/package/service/mod.rs::PackageService` — package fetch/list queries that join licenses.
- `common/src/db/query.rs` — shared query builder helpers.
- `common/src/error.rs::AppError` — not-found and bad-request variants.

## Acceptance Criteria
- [ ] `SbomService::compare(left, right)` returns an `SbomComparison` with all six categories filled correctly
- [ ] Packages only in the right SBOM appear in `added_packages`, and packages only in the left appear in `removed_packages`, each with license and advisory count
- [ ] Packages in both with different versions appear in `version_changes` with the correct `direction`
- [ ] Packages in both with different licenses appear in `license_changes`
- [ ] Advisories affecting only the right SBOM appear in `new_vulnerabilities`, and those affecting only the left appear in `resolved_vulnerabilities`, each with severity, title, and package
- [ ] A missing left or right SBOM returns a not-found `AppError`, never an empty diff
- [ ] Comparing an SBOM with itself returns six empty arrays
- [ ] Computation uses a constant number of DB queries regardless of package count (no per-package queries)
- [ ] No new tables or migrations are added

## Test Requirements
- [ ] Unit tests for the pure diff function covering added, removed, version upgrade, version downgrade, license change, and no-change inputs
- [ ] Unit test for version direction with semver versions and non-semver fallback versions
- [ ] Test that a nonexistent SBOM ID returns a not-found error and not an empty `SbomComparison` (fail-closed)
- [ ] Test that comparing an SBOM with itself yields an empty diff

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
