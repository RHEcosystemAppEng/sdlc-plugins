# Implementation Plan — TC-9208: Add package license summary endpoint with tests

Skill: `/sdlc-workflow:implement-task` (followed from SKILL.md; dry run, so no repo, Jira, git, or Serena calls were made)

## Step 0: Project configuration check

The mock CLAUDE.md (`claude-md-mock.md`) has everything the skill needs:
- Repository Registry: `trustify-backend` uses Serena instance `serena_backend`, path `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence: naming convention `mcp__<instance>__<tool>`. Limitation: rust-analyzer can take 30–60s to index on first use.

Result: PASS. Execution continues.

## Step 1: Parse the task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR | not present, so the default flow applies (new branch, new PR) |
| Bookend Type | not present |
| Dependencies | None |
| GitHub Issue (customfield_10747) | read from the issue. If empty, skip silently. |

All required sections are present, so there is no clarification stop.

## Step 1.5 / 2 / 3: Jira steps (would run; not executed here)

- Step 1.5: fetch comments and look for `[sdlc-workflow] Description digest:`. Compute the digest with `scripts/sha256-digest.py` and compare. If there is no digest, warn and continue.
- Step 2: no dependencies, so nothing to check.
- Step 3: `jira.user_info()`, then assign to the current user, then transition to **In Progress**.

## Step 4: Understand the code (planned Serena calls on `serena_backend`)

- `get_symbols_overview` on `modules/fundamental/src/package/endpoints/mod.rs`, `endpoints/list.rs` and `model/mod.rs`, `model/summary.rs`
- `find_symbol` with `include_body=true` on the list handler in `package/endpoints/list.rs`. This is the pattern reference from the Implementation Notes.
- `find_symbol` on the `package_license` entity (`entity/src/package_license.rs`) and on `sbom_package` (`entity/src/sbom_package.rs`) to confirm the relations and column names used in the JOIN
- `find_symbol` on the `sbom/endpoints/get.rs` handler. It is the sibling that already resolves `/api/v2/sbom/{id}` and returns 404 for an unknown ID, so the 404 path can be reused.
- `find_symbol` on `AppError` in `common/src/error.rs` to find the NotFound variant and the `.context()` usage
- `search_for_pattern` for existing license-classification logic (`permissive`, `copyleft`, `LicenseCategory`, `PERMISSIVE_LICENSES`, `Apache-2.0`, `GPL-`). This is the symbol-deduplication check: if a classification list already exists, reuse it.
- `find_referencing_symbols` is not needed for backward compatibility. No existing symbol changes signature; only additive `mod` and route lines are added.
- CONVENTIONS.md lookup: read `./CONVENTIONS.md` at the repo root (it exists per repo-backend.md). Pull out the CI check commands (e.g. `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`) and any OpenAPI or codegen command, for Step 9.
- Documentation files found: `README.md`, `CONVENTIONS.md`, `docs/api.md` (REST API reference), `docs/architecture.md`.
- Sibling convention analysis: see `conventions.md`.

## Step 5: Branch

```
git checkout main
git pull
git checkout -b TC-9208
```

## Step 6: Changes, file by file

### 1. CREATE `modules/fundamental/src/package/model/license_summary.rs`

- `/// License category bucket: number of distinct licenses and their identifiers.`
  `#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize, ToSchema)] pub struct LicenseCategorySummary { pub count: u64, pub licenses: Vec<String> }`
- `/// Response body for GET /api/v2/sbom/{id}/license-summary, grouped by license type.`
  `pub struct LicenseSummary { pub permissive: LicenseCategorySummary, pub copyleft: LicenseCategorySummary, pub unknown: LicenseCategorySummary }`. Derives match the siblings `PackageSummary` and `SbomSummary` (serde plus utoipa `ToSchema`, if siblings use it).
- `/// Classifies an SPDX license identifier as permissive, copyleft, or unknown.`
  `pub enum LicenseCategory { Permissive, Copyleft, Unknown }` with a `fn classify(id: &str) -> LicenseCategory` helper. The helper matches on a case-insensitive SPDX identifier list: MIT, Apache-2.0, BSD-2/3-Clause, ISC, etc. map to permissive; GPL-*, LGPL-*, AGPL-*, MPL-2.0, EPL-*, etc. map to copyleft; anything else maps to unknown. This is only declared if the Step 4 dedup search finds no existing classification symbol. If one exists, import it instead.
- `/// Builds a LicenseSummary from raw license identifiers, deduplicating within each category.`
  `impl LicenseSummary { pub fn from_licenses<I: IntoIterator<Item = String>>(iter: I) -> Self }`. It uses a `BTreeSet<String>` per category, which gives both dedup (an acceptance criterion) and deterministic sorted output so tests can compare exact values. It skips empty or whitespace identifiers (defensive) and sets `count = licenses.len()`.
- Every new struct, enum, and pub fn gets a `///` doc comment, per the skill's code-quality rules.

### 2. MODIFY `modules/fundamental/src/package/model/mod.rs`

- Add `pub mod license_summary;`, alphabetically before `pub mod summary;` to match the existing ordering.

### 3. CREATE `modules/fundamental/src/package/endpoints/license_summary.rs`

- Follows `package/endpoints/list.rs`: same extractor style (`State<AppState>` / db connection, `Path<Id>`), the same `#[utoipa::path(...)]` annotation style if siblings use it, and the same return type `Result<Json<LicenseSummary>, AppError>`.
- `/// GET /api/v2/sbom/{id}/license-summary — returns license counts and identifiers grouped by category.`
  `pub async fn get_license_summary(...) -> Result<Json<LicenseSummary>, AppError>`
  1. Look up the SBOM by ID (`sbom::Entity::find_by_id`). If it is missing, return the `AppError` NotFound variant, which gives a 404. The pattern and variant are taken from `sbom/endpoints/get.rs`.
  2. Query `package_license` joined through `sbom_package` and filtered by `sbom_package.sbom_id = id`, selecting the license identifier column. The query is scoped to the single SBOM, not loaded globally and filtered in memory (query-scope check). Where possible, use `.distinct()` at the DB level.
  3. Treat a nullable license column as optional: `filter_map` out `None` and empty values (defensive access across the entity boundary).
  4. Wrap DB errors with `.context("fetching package licenses for SBOM {id}")`, per the Implementation Notes.
  5. Return `Json(LicenseSummary::from_licenses(rows))`.
- Note on placement: the module convention puts DB access in `service/`, but `package/service/mod.rs` is **not** in Files to Modify. To stay in scope, the query lives in the handler file. Step 9 flags this, offering the user the option to move it into `PackageService::license_summary()` if they approve modifying `service/mod.rs`.

### 4. MODIFY `modules/fundamental/src/package/endpoints/mod.rs`

- Add `mod license_summary;` alongside `mod list;`.
- Register the route in the existing router builder, following the existing chaining and caching-middleware style: `.route("/api/v2/sbom/:id/license-summary", get(license_summary::get_license_summary))`. Use whatever path-parameter syntax the siblings use (`:id` or `{id}`, depending on the Axum version).
- If siblings register handlers in a utoipa `OpenApi` `paths(...)` list, add the new handler and the `LicenseSummary` / `LicenseCategorySummary` schemas there too.
- Flag for review: the URL sits under `/api/v2/sbom/...` but is registered in the **package** module's router, as the task specifies. Make sure it does not collide with the sbom module's `/api/v2/sbom/{id}` routes. Axum merges distinct paths without problems.

### 5. CREATE `tests/api/package_license.rs`

- See `test-plan.md`. Four integration tests against the real PostgreSQL test DB, using the same harness, setup helpers, and naming as `tests/api/sbom.rs` and `advisory.rs`.

### Documentation impact

- There is no "Documentation Updates" section. `docs/api.md` (REST API reference) would normally document a new endpoint, but it is **not** in Files to Modify. Following the scope rule, I would not edit it. Step 9 flags it to the user as a recommended out-of-scope doc update. If an OpenAPI generation command is listed in CONVENTIONS.md, run it and commit the regenerated spec as part of the deliverable.

## Step 7: Tests

See `test-plan.md`. Run `cargo test -p <tests crate>` and `cargo test -p trustify-module-fundamental`. Resolve crate names with `cargo metadata --no-deps --format-version 1`.

## Step 8: Acceptance criteria mapping

| AC | Covered by |
|---|---|
| Returns categorized license counts | handler + `from_licenses`; test `license_summary_categorizes_known_licenses` |
| 404 for non-existent SBOM | SBOM existence check; test `license_summary_unknown_sbom_returns_404` |
| Each category has count + list | `LicenseCategorySummary { count, licenses }`; exact-struct asserts in every test |
| Deduplicated within category | `BTreeSet` + DB `distinct`; test `license_summary_deduplicates_licenses` |

## Step 9: Self-verification

- **Scope containment:** the expected diff is exactly the 2 modified and 3 created files. Items flagged for user approval rather than changed silently:
  1. `docs/api.md`: new endpoint not documented
  2. `package/service/mod.rs`: query placed in the handler instead of the service layer
  3. The test crate may need `tests/api/package_license.rs` registered (e.g. a `mod package_license;` in a tests `main.rs`/`lib.rs`, or a `[[test]]` entry in `tests/Cargo.toml`), depending on how the existing `sbom.rs`/`advisory.rs` files are wired. That registration file is not listed.
- **Untracked file check:** `git status --short`. Make sure all 3 new files are staged and nothing else.
- **Dead parameter detection:** not applicable (no code removed).
- **Sensitive-pattern check:** grep the staged diff.
- **Duplication check:** grep for existing license classification or `from_licenses`-style helpers. Reuse any that exist.
- **CI checks:** run every command from CONVENTIONS.md and stop hard on any non-zero exit. Run the Rust module-level tests for each touched crate (`fundamental` and tests).
- **Data-flow trace:** HTTP GET → `Path<id>` → SBOM existence check (404) → JOIN `sbom_package`⋈`package_license` filtered by SBOM → classify + dedup → `LicenseSummary` → `Json` response. Complete.
- **Query-scope verification:** the query filters by `sbom_id`, with no full-table scan.
- **Contract & sibling parity:** handler signature and `AppError` usage match `list.rs`. Response struct derives match `PackageSummary`. Caching middleware and route builder style match sibling registration. The 404 matches `sbom/endpoints/get.rs`.

## Step 10: Commit and PR

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(package): add SBOM license summary endpoint

Adds GET /api/v2/sbom/{id}/license-summary returning deduplicated license
identifiers grouped into permissive, copyleft and unknown categories.

Implements TC-9208"
```

Check for an `upstream` remote (fork detection), then run `gh pr create --base main` (with `-R`/`--head` if it is a fork). The PR body includes `Implements [TC-9208](<webUrl>)`, plus `Closes <owner>/<repo>#<n>` if the GitHub Issue field is set. It also notes the sibling-assertion deviation and the flagged out-of-scope items.

## Step 11: Jira

Set `customfield_10875` to the PR URL (ADF inlineCard). Add a comment with the PR link, a summary, and deviations (value-based assertions instead of the sibling `.any()`/`count() > 0` style, and the handler-level query). The comment ends with the implement-task footnote. Transition the issue to **In Review**.
