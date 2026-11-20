# Task 2 — Add SBOM comparison model and diff service

**Summary:** Add SBOM comparison response model and on-the-fly diff computation in SbomService
**Epic:** TC-9003: SBOM diff API
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003)

---

## Repository
trustify-backend

## Target Branch
TC-9003

## Description
Add the domain model and service logic that computes a structured diff between two SBOMs. This is the backend core of the SBOM comparison view (TC-9003). Given a `left` and a `right` SBOM ID, the service returns six diff categories:

- added packages
- removed packages
- version changes
- new vulnerabilities
- resolved vulnerabilities
- license changes

The diff is computed on the fly from existing package, advisory, and license data. The feature's non-functional requirements forbid new database tables, so this task adds no migration. The HTTP endpoint that exposes the service is Task 3.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export the new `compare` model module
- `modules/fundamental/src/sbom/service/sbom.rs` — add a `SbomService::compare(left_id, right_id)` method that loads both SBOMs' packages, licenses, and advisories, then delegates to a pure diff function

## Files to Create
- `modules/fundamental/src/sbom/model/compare.rs` — `SbomComparison` response struct plus the entry structs `PackageDiffEntry`, `VersionChangeEntry`, `VulnerabilityDiffEntry`, `LicenseChangeEntry`, and a `VersionDirection` enum (`upgrade` / `downgrade`), all deriving `Serialize` (snake_case field names)

## Implementation Notes
- **Response shape.** It must match the contract the Figma design expects (figma-context.md, "Backend Interactions"):
  ```json
  {
    "added_packages":           [{ "name": "string", "version": "string", "license": "string|null", "advisory_count": 0 }],
    "removed_packages":         [{ "name": "string", "version": "string", "license": "string|null", "advisory_count": 0 }],
    "version_changes":          [{ "name": "string", "left_version": "string", "right_version": "string", "direction": "upgrade|downgrade" }],
    "new_vulnerabilities":      [{ "advisory_id": "string", "severity": "critical|high|medium|low", "title": "string", "affected_package": "string" }],
    "resolved_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "previously_affected_package": "string" }],
    "license_changes":          [{ "name": "string", "left_license": "string|null", "right_license": "string|null" }]
  }
  ```
  Serialize `VersionDirection` with `#[serde(rename_all = "lowercase")]`. Serialize severity with the same string representation that `AdvisorySummary.severity` already uses (`modules/fundamental/src/advisory/model/summary.rs`), so the frontend can reuse its existing severity mapping.
- **Diff semantics.**
  - Match packages by package name (identity without version).
    - Name only in right → `added_packages`.
    - Name only in left → `removed_packages`.
    - Name in both with a different version → `version_changes`.
  - `license_changes` covers packages present in both SBOMs whose license differs. Read licenses through the `entity/src/package_license.rs` mapping.
  - `new_vulnerabilities` lists advisories linked to the right SBOM but not to the left. `resolved_vulnerabilities` is the reverse. Match on advisory ID. Use `entity/src/sbom_advisory.rs` for the SBOM-to-advisory link.
- **Pure function.** Put the set arithmetic in a pure function (e.g., `fn diff(left: SbomSnapshot, right: SbomSnapshot) -> SbomComparison`) that is separate from the DB loading. This lets the diff logic be unit-tested without a database.
- **Version direction.** Compare versions with semantic-version ordering when both versions parse as semver. Otherwise fall back to a lexical comparison and document that fallback in a code comment.
- **Performance (NFR: p95 < 1s for up to 2000 packages per SBOM).**
  - Load each SBOM's packages with a single joined query over `sbom_package` → `package` → `package_license` (one query per side). Load advisories with one query per side over `sbom_advisory` → `advisory`. Avoid N+1 per-package queries.
  - Use `HashMap`/`HashSet` keyed by package name and advisory ID so the diff runs in O(n).
- **Errors.** `compare` returns `Result<SbomComparison, AppError>` and wraps DB errors with `.context(...)`. It returns the existing not-found variant of `AppError` (`common/src/error.rs`) when either SBOM ID does not exist. It must never return an empty diff for a missing SBOM, because that would be a silent "no changes" result.
- **Data producers (shared-artifact analysis).** The diff only reads `sbom_package`, `package_license`, and `sbom_advisory`. These are populated by the SBOM ingestion path (`modules/ingestor/src/graph/sbom/mod.rs`) and the advisory correlation path (`modules/ingestor/src/graph/advisory/mod.rs`). No producer changes are needed. The diff reflects whatever the ingestor has correlated at request time.
- Per CONVENTIONS.md §Module pattern: place the new model in `sbom/model/` and the logic in `sbom/service/`, following the existing `model/ + service/ + endpoints/` structure. See `modules/fundamental/src/sbom/model/summary.rs` and `modules/fundamental/src/sbom/service/sbom.rs` for the established pattern.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's `modules/<domain>/` Rust module scope.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` and wrap fallible calls with `.context()`. See the existing fetch methods in `modules/fundamental/src/sbom/service/sbom.rs`.
  Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust handler/service scope.
- Constraints (docs/constraints.md):
  - §2 Commit rules: Conventional Commits format, a `Implements TC-<task-key>` footer, and an `Assisted-by:` trailer.
  - §3 PR rules: open the PR with `--base TC-9003` and post the PR link on the Jira task.
  - §5 Code change rules: change only the listed files; inspect code before modifying it; reuse existing helpers rather than duplicating them (§5.4); trace the full data flow from input to output (§5.6).
  - §1.4/§1.5 (implement-task scope): no unrelated refactoring; inspect code structure before changing it.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing fetch logic for SBOM by ID; reuse its lookup and not-found handling for both `left` and `right`
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — already exposes package name, version, and `license`; reuse its field mapping when building the snapshot
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package listing queries; reuse its query or filter for "packages in SBOM X" instead of writing raw SQL
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — includes the `severity` field and title; reuse its severity type for `VulnerabilityDiffEntry.severity`
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing advisory fetch/list; check for a "list advisories by SBOM" query to reuse
- `common/src/db/query.rs` — shared query builder helpers (filtering); reuse them for SBOM-scoped package and advisory filtering
- `common/src/error.rs::AppError` — reuse the existing not-found variant

## Acceptance Criteria
- [ ] `SbomComparison` serializes to exactly the six snake_case top-level keys shown above, and each entry has the listed fields
- [ ] Packages only in the right SBOM appear in `added_packages`, with `advisory_count` equal to the number of advisories linked to that package in the right SBOM
- [ ] Packages only in the left SBOM appear in `removed_packages`
- [ ] Packages in both SBOMs with differing versions appear in `version_changes` with the correct `direction` (`upgrade` when right > left, `downgrade` otherwise)
- [ ] Packages in both SBOMs with differing licenses appear in `license_changes`
- [ ] Advisories linked only to the right SBOM appear in `new_vulnerabilities`; advisories linked only to the left appear in `resolved_vulnerabilities`
- [ ] Comparing an SBOM with itself returns six empty arrays
- [ ] A non-existent `left` or `right` ID returns an `AppError` not-found error, not an empty diff
- [ ] No new migration or entity is added

## Test Requirements
- [ ] Unit tests for the pure diff function covering: added only, removed only, version upgrade, version downgrade, license change, new vulnerability, resolved vulnerability, identical SBOMs (all empty), and non-semver version fallback
- [ ] Unit test confirming that a package present in both SBOMs with the same version and license appears in no category
- [ ] Service-level test against the PostgreSQL test database confirming that a missing SBOM ID yields a not-found error rather than an empty `SbomComparison`
- [ ] Performance sanity test: diffing two synthetic snapshots of 2000 packages each completes well under 1s in-process

## Verification Commands
- `cargo test -p trustify-module-fundamental sbom` — all new and existing SBOM tests pass (adjust the crate name to the one in `modules/fundamental/Cargo.toml`)
- `cargo clippy --all-targets -- -D warnings` — no new warnings

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
