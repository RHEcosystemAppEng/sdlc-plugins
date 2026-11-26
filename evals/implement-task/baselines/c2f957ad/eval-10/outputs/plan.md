# Implementation Plan — TC-9208: Add package license summary endpoint with tests

## Pre-flight (Steps 0–3)

- **Step 0 – Project Configuration**: The mock CLAUDE.md has `Repository Registry` (trustify-backend, Serena instance `serena_backend`, path `./`), `Jira Configuration` (Project key TC, Cloud ID, Feature issue type ID 10142, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`) and `Code Intelligence` (naming convention `mcp__<instance>__<tool>`). Validation passes.
- **Step 1 – Parse task**: Every required section is there: Repository (`trustify-backend`), Target Branch (`main`), Description, Files to Modify, Files to Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies (None). The task has no Target PR and no Bookend Type, so the default flow applies. The GitHub Issue custom field (`customfield_10747`) would be read from the issue. If it is set, `Closes <owner>/<repo>#<n>` goes in the PR body.
- **Step 1.5 – Digest check**: Would fetch comments, find the most recent `[sdlc-workflow] Description digest:` comment and compare it with `scripts/sha256-digest.py`. (Skipped in the eval because external calls are not allowed.)
- **Step 2 – Dependencies**: None.
- **Step 3**: Would assign TC-9208 to the current user and move it to In Progress. (Skipped in the eval.)
- **Step 5 – Branch**: `git checkout main && git pull && git checkout -b TC-9208` (not executed).

## Step 4 – Code understanding (what would be inspected with `serena_backend`)

- `get_symbols_overview` on `modules/fundamental/src/package/endpoints/mod.rs`, `endpoints/list.rs`, `model/mod.rs`, `model/summary.rs`, `service/mod.rs`.
- `find_symbol include_body=true` on the `list` handler in `package/endpoints/list.rs`. This is the reference pattern named in Implementation Notes: handler signature, extractors, `Result<_, AppError>`, `.context()`.
- `find_symbol` on `entity/src/package_license.rs` (columns and relation to `package`), `entity/src/sbom_package.rs` (join from SBOM to package) and `entity/src/sbom.rs`.
- `find_symbol` on `SbomService::fetch` in `modules/fundamental/src/sbom/service/sbom.rs` and on `sbom/endpoints/get.rs`, to see how "SBOM not found → 404" is already done. Reuse that rather than writing new existence-check logic.
- `find_symbol` on `AppError` in `common/src/error.rs` to confirm there is a `NotFound` variant that maps to 404.
- **Symbol deduplication**: `search_for_pattern` across the workspace for any existing license classification such as `permissive`, `copyleft`, `LicenseCategory`, `LICENSE_CATEGORIES`, or SPDX identifier lists. If one exists, import it and do not declare a new one.
- `CONVENTIONS.md` exists at the repo root. Read it, follow it, and pull out its CI-check commands and any code-generation commands (for example OpenAPI generation) for Step 9.
- Documentation files to note: `README.md`, `docs/api.md` (REST API reference) and `docs/architecture.md`.
- Sibling analysis results are in `conventions.md`.

## Step 6 – Changes by file

### Files to Modify

1. **`modules/fundamental/src/package/model/mod.rs`**
   - Add `pub mod license_summary;` next to the existing `pub mod summary;`, using the same declaration and re-export style.

2. **`modules/fundamental/src/package/endpoints/mod.rs`**
   - Add `mod license_summary;`. Register `GET /api/v2/sbom/{id}/license-summary` → `license_summary::get_license_summary` in the module's route builder, following how `list.rs` is registered (same router and caching-layer style as siblings).
   - Note: this route sits under the `/api/v2/sbom` prefix but is registered from the package module, as the task specifies. Use the full path explicitly so it does not clash with the sbom module's `/api/v2/sbom/{id}` route. Confirm with `server/main.rs` how module routers are merged so the path resolves. `main.rs` only needs reading, not editing.

### Files to Create

3. **`modules/fundamental/src/package/model/license_summary.rs`**
   - `/// Aggregated license breakdown for the packages in an SBOM.`
     `pub struct LicenseSummary { pub permissive: LicenseCategorySummary, pub copyleft: LicenseCategorySummary, pub unknown: LicenseCategorySummary }`
   - `/// Count and deduplicated license identifiers for a single license category.`
     `pub struct LicenseCategorySummary { pub count: usize/u64, pub licenses: Vec<String> }`
   - Use the same derives as `PackageSummary` (`Serialize`, `Deserialize`, `Debug`, `Clone`, `PartialEq`, `Default`, and `ToSchema`/utoipa if siblings use it). `Default` gives the all-zeros response for an empty SBOM.
   - `/// Builds a summary from raw license identifiers, classifying and deduplicating them.`
     `impl LicenseSummary { pub fn from_licenses<I: IntoIterator<Item = String>>(iter: I) -> Self }`. It uses a `BTreeSet<String>` per category, which deduplicates and gives a deterministic sorted order. `count = set.len()`, so count means distinct licenses per category (acceptance criterion 4).
   - Classification helper: `/// Classifies an SPDX license identifier as permissive, copyleft, or unknown.` `fn classify(id: &str) -> LicenseCategory`. Only add it if the dedup search found nothing. Use a small documented set (permissive: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, ...; copyleft: GPL-*, LGPL-*, AGPL-*, MPL-2.0, EPL-*, ...). Anything else, or an empty/NULL license, is `unknown`.
   - Defensive handling: NULL or empty license values from the DB are treated as `unknown`. Decide during implementation whether empty strings go into the `licenses` list (planned: put NULL/empty under the identifier `"NOASSERTION"`, or leave it out of the list but count it. Confirm this against the API contract before finalizing). Trim identifiers before classifying.

4. **`modules/fundamental/src/package/endpoints/license_summary.rs`**
   - `/// GET /api/v2/sbom/{id}/license-summary — returns license counts grouped by category for an SBOM's packages.`
     `pub async fn get_license_summary(State(db)/service, Path(id): Path<Uuid or Id>) -> Result<Json<LicenseSummary>, AppError>`
   - Use the same extractors and state type as `list.rs`.
   - Steps:
     1. Check the SBOM exists by reusing the existing SBOM lookup (`SbomService::fetch` or the same entity `find_by_id` used in `sbom/endpoints/get.rs`). `None` → `AppError::NotFound`, which gives 404.
     2. SeaORM query: `package_license::Entity` JOIN `package` JOIN `sbom_package` with filter `sbom_package::Column::SbomId.eq(id)`, selecting only the license identifier column (scoped to that one SBOM, not a full-table load). Wrap errors with `.context("failed to query package licenses for SBOM {id}")`.
     3. `LicenseSummary::from_licenses(rows)` → `Json(...)`.
   - Add a utoipa `#[utoipa::path]` annotation if the sibling handlers have one.
   - Scope note: `package/service/mod.rs` (PackageService) is **not** in Files to Modify. Siblings normally put DB access in the service layer. To stay in scope, the query lives in the handler file (or a private fn inside it). This sibling-parity gap would be raised in the Step 9 scope check, with the alternative of adding `PackageService::license_summary(sbom_id)` if the user approves the extra file.

5. **`tests/api/package_license.rs`** — integration tests. See `test-plan.md`.

### Documentation impact
- The task has no Documentation Updates section. `docs/api.md` (REST API reference) would normally list the new endpoint, but it is outside Files to Modify/Create. Flag it for user approval in Step 9 and do not edit it silently.
- If `CONVENTIONS.md` lists an OpenAPI generation command, run it in Step 9 and commit the regenerated spec. It is a generated artifact, but it is still flagged in the scope check.

## Step 7 – Tests
See `test-plan.md`. Run `cargo test -p <crate>` for the crates that own the changed files (resolved via `cargo metadata`: the fundamental-module crate and the tests crate).

## Step 8 – Acceptance criteria mapping
| Criterion | How it is met | Test |
|---|---|---|
| Returns categorized license counts | Handler + `LicenseSummary::from_licenses` | `test_license_summary_categorizes_known_licenses` |
| 404 for unknown SBOM | SBOM existence check → `AppError::NotFound` | `test_license_summary_nonexistent_sbom_returns_404` |
| Each category has count + list | `LicenseCategorySummary { count, licenses }` | asserted with full-struct `assert_eq!` |
| Licenses deduplicated per category | `BTreeSet` per category | `test_license_summary_deduplicates_licenses` |

## Step 9 – Self-verification items to raise
- **Scope containment**: expected diff = the 2 modified and 3 created files. Possible out-of-scope items to flag for approval:
  - `tests/Cargo.toml` or a `tests/api/main.rs`/`mod.rs`, if test files must be registered to compile.
  - `package/service/mod.rs`, if the query moves to the service layer.
  - `docs/api.md`, and any generated OpenAPI spec.
- **Untracked file check**: run `git status --short` in the touched directories before staging.
- **CI checks**: run every command from the CI section of `CONVENTIONS.md` (for example `cargo fmt --check`, `cargo clippy`, `cargo check`). Any non-zero exit is a hard stop.
- **Rust module tests**: `cargo test -p <fundamental crate>` and `-p <tests crate>`.
- **Data-flow trace**: Path `{id}` → SBOM existence check → scoped JOIN query → classify and dedup → `Json<LicenseSummary>` → HTTP 200. Not found → `AppError::NotFound` → 404. DB error → `.context()` → `AppError` → 500.
- **Query-scope**: the query is filtered by `sbom_id`, with no `::all()`.
- **Contract/sibling parity**: the handler returns `Result<_, AppError>` like `list.rs`. Same caching-middleware registration as sibling routes. Same derives and utoipa schema as `PackageSummary`. Caller-site: SBOM lookup is used the same way as in `sbom/endpoints/get.rs`.
- **Duplication check**: grep for existing license classifiers or SBOM-existence helpers again after implementing.

## Step 10 – Commit / PR (not executed)
```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(package): add SBOM license summary endpoint

Adds GET /api/v2/sbom/{id}/license-summary returning deduplicated license
identifiers grouped into permissive, copyleft and unknown categories.

Implements TC-9208"
```
`gh pr create --base main` (or `-R <upstream> --head <fork>:TC-9208` if an `upstream` remote exists). The PR body includes `Implements [TC-9208](<webUrl>)`, plus `Closes owner/repo#N` if the GitHub Issue field is set.

## Step 11 – Jira (not executed)
Set `customfield_10875` to the PR URL as an ADF inlineCard. Add a comment with the PR link, a summary, and deviations: the assertion style differs from siblings and the query lives in the handler because the service layer was out of scope. End the comment with the footnote from `shared/comment-footnote.md`. Transition the issue to In Review.
