# Implementation Plan — TC-9208: Add package license summary endpoint with tests

## Step 0 — Project Configuration validation
The mock CLAUDE.md contains all required sections:
- Repository Registry: `trustify-backend` | Rust backend service | `serena_backend` | `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142 (plus Git Pull Request field `customfield_10875`, GitHub Issue field `customfield_10747`)
- Code Intelligence: tool naming convention `mcp__<serena-instance>__<tool>`, instance `serena_backend` (rust-analyzer; may take 30-60s to index on first use)

Validation passes, so execution continues.

## Step 1 — Parsed task
| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR | none, so default flow (new branch + new PR) |
| Bookend Type | none |
| Dependencies | None, so Step 2 has nothing to check |
| GitHub Issue (customfield_10747) | would be read from the issue; skipped if empty |

All required sections are present, so there is no need to stop for clarification.

## Step 1.5 / 2 / 3 — Jira steps (simulated, not executed)
- Would fetch comments, find the `[sdlc-workflow] Description digest:` comment, and compare digests.
- No dependencies to check.
- Would assign the issue to the current user and move it to In Progress.

## Step 4 — Code understanding (would use `mcp__serena_backend__*`)
- `get_symbols_overview` on `modules/fundamental/src/package/endpoints/mod.rs`, `endpoints/list.rs`, `model/mod.rs`, `model/summary.rs`.
- `find_symbol include_body=true` on the list handler in `package/endpoints/list.rs`, the route-registration function in `package/endpoints/mod.rs`, and `PackageSummary` (it already has a `license` field).
- `find_symbol` on the `package_license` entity (`entity/src/package_license.rs`), and on `sbom_package` / `package` entities, to see how the join columns relate.
- Siblings: `sbom/endpoints/get.rs` (the closest analog: a single-resource GET by `{id}` that returns 404) and `advisory/endpoints/get.rs`. For tests: `tests/api/sbom.rs` and `tests/api/advisory.rs`.
- Reuse search: `search_for_pattern` for an existing license categorization helper (e.g. `permissive`, `copyleft`, `spdx`, `LicenseCategory`) and for an existing "fetch SBOM by id or 404" helper in `SbomService` / `common/src/db/query.rs`. Reuse anything that exists instead of re-implementing it.
- Read `CONVENTIONS.md` at the repo root. Extract the CI check commands (e.g. `cargo fmt --check`, `cargo clippy`, `cargo check`) and any code-generation command (e.g. OpenAPI spec generation) for Step 9.
- Documentation files identified: `README.md`, `docs/api.md` (REST API reference), `CONVENTIONS.md`.

## Step 5 — Branch (simulated)
`git checkout main && git pull && git checkout -b TC-9208`

## Step 6 — File changes

### Files to Modify

1. `modules/fundamental/src/package/model/mod.rs`
   - Add `pub mod license_summary;`. Add `pub use license_summary::*;` too if the existing modules are re-exported that way (match how `summary` is exposed).

2. `modules/fundamental/src/package/endpoints/mod.rs`
   - Add `mod license_summary;`.
   - In the existing route-registration function, register `GET /api/v2/sbom/{id}/license-summary` and point it at `license_summary::get`. Follow the same builder / `.route(...)` style and the caching-middleware config used for the `list` route.
   - Flag for review: the path sits under `/api/v2/sbom`, but it is registered in the package module as the task requires. I would check that this doesn't collide with routes registered in `sbom/endpoints/mod.rs`, which mount `/api/v2/sbom`.

### Files to Create

3. `modules/fundamental/src/package/model/license_summary.rs`
   - `/// Summary of license identifiers in an SBOM, grouped by license category.`
     `#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize, ToSchema)] pub struct LicenseSummary { pub permissive: LicenseCategorySummary, pub copyleft: LicenseCategorySummary, pub unknown: LicenseCategorySummary }`
   - `/// Count and sorted, deduplicated license identifiers for one license category.`
     `pub struct LicenseCategorySummary { pub count: u64, pub licenses: Vec<String> }` (same derives). `count == licenses.len()` after deduplication.
   - `/// License category used to bucket package licenses.` `enum LicenseCategory { Permissive, Copyleft, Unknown }`, with a documented `fn categorize(license: &str) -> LicenseCategory`. It uses a static list of SPDX identifiers (e.g. MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, and so on map to permissive; GPL-*, LGPL-*, AGPL-*, MPL-2.0, EPL-*, and so on map to copyleft; anything else, including empty, maps to unknown). Before declaring it, I would search the workspace for an existing license list or constant and reuse it if found (Symbol deduplication rule).
   - `/// Builds a LicenseSummary from raw license identifiers, deduplicating within each category.`
     `pub fn from_licenses<I: IntoIterator<Item = S>, S: AsRef<str>>(iter: I) -> Self`. It trims values, drops nulls and empties into unknown handling, collects into a `BTreeSet` per category so output is deduplicated and deterministically sorted, then fills `count` from the set size.
   - Derives and attributes (`serde`, `utoipa::ToSchema`) match `PackageSummary` in `model/summary.rs`.

4. `modules/fundamental/src/package/endpoints/license_summary.rs`
   - `/// GET /api/v2/sbom/{id}/license-summary — returns package license counts for an SBOM, grouped by category.`
   - Signature follows `list.rs`: `pub async fn get(State(db) / service extractor, Path(id): Path<Uuid or Id>) -> Result<Json<LicenseSummary>, AppError>`. Includes the `#[utoipa::path(...)]` annotation if `list.rs` has one (responses 200 and 404).
   - Logic:
     1. Check the SBOM exists with `entity::sbom::Entity::find_by_id(id)`, or reuse the existing SBOM fetch helper. If it is missing, return `AppError::NotFound` (or the project's 404 variant), as `sbom/endpoints/get.rs` does.
     2. Run the JOIN query `sbom_package` to `package` to `package_license`, filtered by `sbom_package.sbom_id = id`, selecting the license identifier column. Scope is a single SBOM, so the query is filtered at the DB level (query-scope check). Use `common/src/db/query.rs` helpers where applicable.
     3. Call `LicenseSummary::from_licenses(rows)` and return `Json(...)`.
   - Errors: every fallible DB call is wrapped with `.context("...")` and converted to `AppError`, per Implementation Notes and sibling convention.
   - Defensive access: the license column can be NULL. It maps through `Option<String>` and becomes `unknown` instead of being unwrapped.
   - Note: there is no service-layer file in scope. `package/service/mod.rs` (PackageService) is not in Files to Modify, so the query stays in the handler (or a private helper in the same file). If the sibling convention strongly requires service-layer queries, I would flag adding a `PackageService::license_summary` method as an out-of-scope change for user approval instead of making it silently.

5. `tests/api/package_license.rs`
   - Integration tests against the real PostgreSQL test DB, using the same setup, fixtures, and client helpers as `tests/api/sbom.rs` (see test-plan.md).

### Code quality checks
- Every new struct, enum, and public fn gets a `///` doc comment.
- NULL licenses are handled with `Option` / `unwrap_or_default`.
- Symbol deduplication is checked before declaring license-category constants.

### Documentation impact
- The task has no Documentation Updates section. `docs/api.md` (the REST API reference) would normally describe the new endpoint, but it is not in Files to Modify/Create. I would flag it in Step 9 scope containment for user approval rather than edit it. An OpenAPI spec regenerated by a CONVENTIONS.md code-gen command would be staged as part of the deliverable.

## Step 7 — Tests
See `test-plan.md`. Run `cargo test -p <tests crate>` and `cargo test -p <fundamental crate>`, with crate names resolved via `cargo metadata --no-deps --format-version 1`.

## Step 8 — Acceptance Criteria mapping
| AC | Satisfied by |
|---|---|
| Returns categorized license counts | handler + `LicenseSummary::from_licenses`; test `license_summary_returns_categorized_licenses` |
| 404 for missing SBOM | existence check in handler; test `license_summary_unknown_sbom_returns_404` |
| Each category has count + list | `LicenseCategorySummary { count, licenses }`; asserted via full struct equality |
| Deduplicated within category | `BTreeSet` per category; test `license_summary_deduplicates_licenses_within_category` |

## Step 9 — Self-verification
- Scope containment: expected diff is exactly the 2 modified and 3 created files. Possible out-of-scope items to flag rather than change: `tests/Cargo.toml` or a test entry-point (`tests/api/main.rs` / `mod` declaration) if one is needed to compile the new test file; `docs/api.md`; `package/service/mod.rs`.
- Untracked file check, sensitive-pattern grep, and dead-parameter check (none expected; nothing is removed).
- Run every CI command from CONVENTIONS.md, with a hard stop on non-zero exit. Run the code-gen command(s) and stage their output.
- Module-level Rust tests: `cargo test -p` for the fundamental crate and the tests crate.
- Data-flow trace: HTTP GET `{id}` -> Path extractor -> SBOM existence check (404) -> JOIN query sbom_package/package/package_license -> categorize + dedupe -> `Json<LicenseSummary>` -> route registered in endpoints/mod.rs -> mounted by server/main.rs through the existing package module mount. Complete.
- Contract & sibling parity: handler signature and `Result<_, AppError>` match `list.rs` / `get.rs`; caching middleware config matches sibling routes; read-only query, so no cross-module write concerns; caller-site check is consistent with how other handlers call the DB connection or service.

## Step 10 — Commit / PR (simulated)
```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(package): add SBOM license summary endpoint

Add GET /api/v2/sbom/{id}/license-summary returning deduplicated package
licenses grouped into permissive, copyleft and unknown categories.

Implements TC-9208"
```
`gh pr create --base main` (with `-R`/`--head` if an upstream remote exists). The body contains `Implements [TC-9208](<webUrl>)`, plus `Closes <owner>/<repo>#<n>` if the GitHub Issue field is set. The PR description also notes the deviation from sibling `.any()`/`count() > 0` test assertions.

## Step 11 — Jira (simulated)
Set `customfield_10875` to the PR URL in ADF inlineCard form. Add a comment covering the PR link, summary, and deviations (value-based assertions instead of sibling existence checks; out-of-scope docs/api.md flagged), ending with the implement-task comment footnote. Transition to In Review.
