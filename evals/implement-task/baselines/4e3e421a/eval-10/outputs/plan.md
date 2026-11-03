# Implementation Plan — TC-9208: Add package license summary endpoint with tests

## Pre-flight (Steps 0–3, simulated)

- **Step 0 — Project Configuration**: The mock CLAUDE.md has Repository Registry (`trustify-backend`, Serena instance `serena_backend`, path `./`), Jira Configuration (Project key TC, Cloud ID, Feature issue type ID 10142) and Code Intelligence (naming convention `mcp__<instance>__<tool>`). Validation passes.
- **Step 1 — Parse task**: Every required section is present: Repository (`trustify-backend`), Target Branch (`main`), Description, Files to Modify, Files to Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies (None). There is no Target PR and no Bookend Type, so the default flow applies. The GitHub Issue field (`customfield_10747`) would be read from the issue. Nothing was fetched (eval mode).
- **Step 1.5 — Digest check**: Would fetch comments and compare the `[sdlc-workflow] Description digest:` value. Skipped in eval mode.
- **Step 2 — Dependencies**: None.
- **Step 3**: Would assign TC-9208 to the current user and move it to In Progress. Skipped in eval mode.
- **Step 5 — Branch**: `git checkout main && git pull && git checkout -b TC-9208`. Not run (eval mode).

## Step 4 — Code understanding (planned Serena calls)

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/package/endpoints/mod.rs`, `.../package/endpoints/list.rs`, `.../package/model/mod.rs`, `.../package/model/summary.rs`.
- `find_symbol(include_body=true)` on the `list` handler in `package/endpoints/list.rs` (the pattern reference) and on the route-builder function in `package/endpoints/mod.rs`.
- `get_symbols_overview` on `entity/src/package_license.rs`, `entity/src/sbom_package.rs`, `entity/src/sbom.rs` to confirm columns and relations for the JOIN (sbom → sbom_package → package → package_license).
- `find_symbol` on `AppError` in `common/src/error.rs` to confirm there is a NotFound variant and how `.context()` is provided.
- Sibling analysis: `sbom/endpoints/get.rs` and `advisory/endpoints/get.rs` (single-resource handlers that return 404), `sbom/model/summary.rs` and `advisory/model/summary.rs` (model struct derives and docs), plus `tests/api/sbom.rs` and `tests/api/advisory.rs` (test structure).
- Reuse search: `search_for_pattern` for `license` across `modules/` and `common/`, looking for any existing license-classification helper (e.g. a permissive/copyleft list or an SPDX categorisation function) before declaring new constants. Covered by symbol deduplication.
- Read `CONVENTIONS.md` at the repo root and extract the CI check commands (fmt, clippy, check, test) plus any OpenAPI generation command for Step 9.
- Documentation identified: `README.md`, `docs/api.md` (REST API reference), `CONVENTIONS.md`.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/mod.rs`
- Add `mod license_summary;` next to the existing `mod list;`.
- In the existing route-registration function, register `GET /api/v2/sbom/{id}/license-summary` → `license_summary::get`. Use the same builder and caching middleware style that `list` uses.
- If the path collides with or nests under the `/api/v2/sbom` scope that `sbom/endpoints/mod.rs` registers, flag it to the user. Do not edit `sbom/endpoints/mod.rs`, because it is out of scope.

### 2. `modules/fundamental/src/package/model/mod.rs`
- Add `pub mod license_summary;`. Optionally add `pub use license_summary::*;` if the siblings re-export (`summary.rs` style).

## Files to Create

### 3. `modules/fundamental/src/package/model/license_summary.rs`
- `/// License summary for all packages in an SBOM, grouped by license category.`
  `pub struct LicenseSummary { pub permissive: LicenseCategory, pub copyleft: LicenseCategory, pub unknown: LicenseCategory }`
- `/// Count and deduplicated, sorted list of license identifiers in one category.`
  `pub struct LicenseCategory { pub count: u64, pub licenses: Vec<String> }`
- Derives match the sibling `PackageSummary`/`SbomSummary`: `Serialize, Deserialize, Debug, Clone, PartialEq, Eq, Default`, plus `utoipa::ToSchema` if the siblings use it for OpenAPI.
- `/// Categorises an SPDX license identifier as permissive, copyleft or unknown.` `fn classify(license: &str) -> Category`, backed by small constant lists (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, ... → permissive; GPL-*, LGPL-*, AGPL-*, MPL-2.0, EPL-* → copyleft; anything else → unknown). Only declare these after the dedup search finds no existing definition.
- `/// Builds a LicenseSummary from raw license strings, deduplicating within each category.` `pub fn from_licenses(iter: impl IntoIterator<Item = String>) -> Self`
  - Uses a `BTreeSet<String>` per category to deduplicate and give deterministic ordering.
  - `count = set.len()`, which is the number of distinct licenses. This satisfies the "duplicates counted only once" requirement.
  - Trims the input and skips empty or NULL licenses defensively (external DB data).

### 4. `modules/fundamental/src/package/endpoints/license_summary.rs`
- `/// GET /api/v2/sbom/{id}/license-summary — returns license counts for the SBOM's packages, grouped by category.`
- Signature mirrors `list.rs`: extracts the DB connection/state and `Path(id)`, and returns `Result<Json<LicenseSummary>, AppError>`.
- Flow:
  1. Look up the SBOM with `entity::sbom::Entity::find_by_id(id)` and `.context("fetching SBOM")`. If it returns `None`, return `AppError::NotFound(...)` (404).
  2. Query `package_license` joined via `sbom_package` and filtered on `sbom_id = id`, selecting only the license column (`.into_tuple::<Option<String>>()`) and wrapping errors with `.context("querying package licenses for SBOM")`. The query is scoped to one SBOM (query-scope check).
  3. `LicenseSummary::from_licenses(rows.into_iter().flatten())` and return `Json(...)`.
- Add a `#[utoipa::path]` annotation if the siblings have one. If the OpenAPI spec is generated, run the generator command from CONVENTIONS.md in Step 9 and commit the result.
- Note: the task gives no service-layer file (`package/service/mod.rs` is not in scope), so the query lives in the handler. If the siblings always put DB access in the service, raise that as a convention conflict or out-of-scope item instead of editing the service.

### 5. `tests/api/package_license.rs`
- Integration tests against the real PostgreSQL test DB, using the setup helpers and naming of `tests/api/sbom.rs`. See test-plan.md for details.
- Note: the repository layout shows no `tests/api/mod.rs` or `tests/api/main.rs`. If the test binary needs a `mod package_license;` line or a `[[test]]` entry in `tests/Cargo.toml`, that file is out of scope and is flagged under Step 9 for user approval, not silently edited.

## Documentation impact
- `docs/api.md` documents the REST API, so a new endpoint is relevant there. The task has no Documentation Updates section and `docs/api.md` is not in Files to Modify, so it is flagged for user approval under scope containment rather than edited.

## Step 8 — Acceptance criteria mapping
| AC | How it is satisfied |
|---|---|
| Returns categorised counts | handler + `LicenseSummary::from_licenses` |
| 404 for missing SBOM | explicit `find_by_id` → `AppError::NotFound` |
| Each category has a count and a list | `LicenseCategory { count, licenses }` |
| Deduplicated within category | `BTreeSet` per category; count = set size |

## Step 9 — Self-verification (planned)
- **Scope containment**: the diff should contain exactly the 2 modified and 3 created files. Possible out-of-scope items to raise with the user: test-harness module registration, `docs/api.md`, service-layer placement, sbom route scope.
- **CI**: run the CONVENTIONS.md commands (e.g. `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo check`) and any codegen. Then run `cargo test -p <fundamental crate name from cargo metadata>` and the `tests` crate. Any failure is a hard stop.
- **Data-flow trace**: HTTP path id → SBOM existence check → join query → classification and dedup → JSON response. Every stage is connected.
- **Contract and sibling parity**: same error wrapping, caching middleware and route builder as `list.rs`. The handler calls the shared `AppError`/DB connection the same way other handlers do.
- **Duplication check**: confirm no existing license classifier exists.
- **Sensitive-pattern check** on the staged diff.

## Steps 10–11 (not run in eval)
- Commit: `feat(package): add SBOM license summary endpoint` with body, footer `Implements TC-9208`, and `--trailer="Assisted-by: Claude Code"`.
- PR: `gh pr create --base main` (with fork flags if an `upstream` remote exists). The body contains `Implements [TC-9208](<webUrl>)` and `Closes <owner>/<repo>#<n>` if the GitHub Issue field is set.
- Jira: set `customfield_10875` to the PR URL as an ADF inlineCard, add a comment (PR link, summary, deviations, including the assertion-style deviation from siblings, with the implement-task footnote), and move the issue to In Review.
