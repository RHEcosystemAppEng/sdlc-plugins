# Implementation Plan — TC-9208: Add package license summary endpoint with tests

## Step 0 — Project Configuration validation

The project CLAUDE.md (claude-md-mock.md) has all required sections:
- Repository Registry: `trustify-backend` | Rust backend service | `serena_backend` | `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142 (plus Git Pull Request field `customfield_10875`, GitHub Issue field `customfield_10747`)
- Code Intelligence: tool naming convention `mcp__<serena-instance>__<tool>`, instance `serena_backend` (rust-analyzer; may take 30–60s to index on first use)

Validation passes, so execution continues.

## Step 1 — Parsed task sections

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Description | GET endpoint that groups an SBOM's package licenses into permissive / copyleft / unknown, returning a count and a deduplicated list of license identifiers for each category |
| Files to Modify | `modules/fundamental/src/package/endpoints/mod.rs`, `modules/fundamental/src/package/model/mod.rs` |
| Files to Create | `modules/fundamental/src/package/model/license_summary.rs`, `modules/fundamental/src/package/endpoints/license_summary.rs`, `tests/api/package_license.rs` |
| API Changes | `GET /api/v2/sbom/{id}/license-summary` (NEW) |
| Target PR | none, so the default flow applies (new branch `TC-9208`, new PR against `main`) |
| Bookend Type | none |
| Dependencies | None, so Step 2 is a no-op |

All required sections are present, so the task is not blocked.

Simulated steps (not executed, per the eval rules): digest integrity check (Step 1.5), assign plus transition to In Progress (Step 3), `git checkout main && git pull && git checkout -b TC-9208` (Step 5).

## Step 4 — Code understanding (planned Serena calls on `serena_backend`)

- `get_symbols_overview` on `modules/fundamental/src/package/endpoints/mod.rs` to see how routes are registered (router builder fn, caching layer config).
- `find_symbol` with `include_body=true` on the handler in `modules/fundamental/src/package/endpoints/list.rs`, which is the reference pattern named in Implementation Notes.
- `get_symbols_overview` on `modules/fundamental/src/package/model/summary.rs` (`PackageSummary`, which has a `license` field) and `modules/fundamental/src/package/service/mod.rs` (`PackageService`).
- `find_symbol` on the `entity/src/package_license.rs` entity, on `entity/src/sbom_package.rs` (SBOM to Package join), and on `entity/src/sbom.rs` (used for the 404 existence check).
- `find_symbol` on `AppError` in `common/src/error.rs` to find the NotFound variant and how `.context()` is used.
- Siblings for conventions: `sbom/endpoints/get.rs` (single-resource GET with 404), `advisory/endpoints/get.rs`, `sbom/model/summary.rs`, `tests/api/sbom.rs`, `tests/api/advisory.rs`.
- Read `CONVENTIONS.md` at the repo root to get the CI check commands (fmt, clippy, check, test) and any OpenAPI generation command.
- Documentation files: `README.md`, `docs/api.md` (REST API reference). `docs/api.md` is a candidate for documentation impact, but it is outside Files to Modify/Create, so it is flagged rather than edited (see Scope notes).
- Symbol dedup search: grep the package for an existing license classification (e.g. `LicenseCategory`, `PERMISSIVE`, `copyleft`, `spdx`). If one exists, reuse it and do not redeclare it.

## Step 6 — File changes

### 1. `modules/fundamental/src/package/model/license_summary.rs` (CREATE)

```rust
/// Licenses in one category: how many distinct identifiers, and which ones.
#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize, ToSchema)]
pub struct LicenseCategory {
    /// Number of distinct license identifiers in this category.
    pub count: usize,
    /// Distinct license identifiers, sorted alphabetically.
    pub licenses: Vec<String>,
}

/// Response for `GET /api/v2/sbom/{id}/license-summary`: an SBOM's package licenses grouped by type.
#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize, ToSchema)]
pub struct LicenseSummary {
    pub permissive: LicenseCategory,
    pub copyleft: LicenseCategory,
    pub unknown: LicenseCategory,
}
```

- Add a constructor, `LicenseSummary::from_licenses(impl IntoIterator<Item = Option<String>>) -> Self`, documented with `///`. It sorts each license into a category using a `BTreeSet<String>` per category, so duplicates are removed and the output order is fixed. `count` is set to `set.len()`, which satisfies the "deduplicated within each category" criterion.
- Add a private classifier, `fn classify(license: &str) -> Category`, that matches known SPDX identifiers:
  - Permissive: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, …
  - Copyleft: GPL-*, LGPL-*, AGPL-*, MPL-2.0, EPL-*, …
  - Anything else goes to unknown. A `None` or empty license is also treated as unknown, using `"NOASSERTION"` as its identifier (a defensive guard on cross-module entity data).
- Derives and serde attributes should match `package/model/summary.rs`, including the `utoipa::ToSchema` derive if siblings use it.

### 2. `modules/fundamental/src/package/model/mod.rs` (MODIFY)

- Add `pub mod license_summary;` next to the existing `pub mod summary;`, keeping alphabetical order.

### 3. `modules/fundamental/src/package/endpoints/license_summary.rs` (CREATE)

- `/// GET /api/v2/sbom/{id}/license-summary — returns license counts for the SBOM's packages, grouped by category.`
- Signature follows `list.rs`, e.g. `pub async fn get(State(db): State<Database>, Path(id): Path<Uuid>) -> Result<Json<LicenseSummary>, AppError>`. The exact extractor types are copied from `list.rs`.
- Logic:
  1. Look up the SBOM with `entity::sbom::Entity::find_by_id(id)`, adding `.context("looking up SBOM")`. If the result is `None`, return `AppError::NotFound(...)`, which gives the 404 acceptance criterion.
  2. Query `sbom_package` joined with `package_license`, filtered by `sbom_package::Column::SbomId.eq(id)`. Select only the license column, scoped to this SBOM rather than loading the whole table (query-scope verification). Add `.context("fetching package licenses for SBOM")`.
  3. Return `Json(LicenseSummary::from_licenses(rows))`. An SBOM with no packages produces the all-zero default.
- Add a `#[utoipa::path(...)]` annotation if `list.rs` has one. The OpenAPI spec is then regenerated with the CONVENTIONS.md codegen command, if one exists.
- This is not a list endpoint, so it returns a plain object rather than `PaginatedResults<T>` (that matches the API Changes contract).
- Placement note: siblings delegate DB access to `PackageService` (`service/mod.rs`). That file is not in Files to Modify, so the query stays inside the handler file. Moving it into a `PackageService::license_summary` method is flagged as an out-of-scope suggestion that needs user approval (see Scope notes).

### 4. `modules/fundamental/src/package/endpoints/mod.rs` (MODIFY)

- Add `mod license_summary;`.
- Register `.route("/api/v2/sbom/{id}/license-summary", get(license_summary::get))` in the package router builder, using the same route path syntax and caching layer setup as the existing `/api/v2/package` route.
- `server/main.rs` already mounts the package module router, so no change is needed there.

### 5. `tests/api/package_license.rs` (CREATE)

- Four integration tests (details in test-plan.md), using the same setup, client, fixture ingestion, and naming as `tests/api/sbom.rs` and `tests/api/advisory.rs`.
- Assertions compare values (`assert_eq!` on the full `LicenseSummary` or on per-category vectors). They do not use the sibling `.filter().any()` / `.count() > 0` existence pattern (see conventions.md).

## Step 9 — Self-verification plan

- Scope containment: `git diff --name-only` should list only the 5 files above. If the OpenAPI codegen output changes, stage it as a generated artifact and mention it in the PR.
- Possible out-of-scope needs, flagged for user approval and not done unilaterally:
  - Registering the new test file. If `tests/` uses an aggregator (for example `tests/api/main.rs` or a `[[test]]` entry in `tests/Cargo.toml`), it may need `mod package_license;`.
  - `docs/api.md`, to document the new endpoint.
  - `PackageService`, if reviewers prefer the query in the service layer.
- CI: run every command listed in CONVENTIONS.md (fmt, clippy, check). Any non-zero exit is a hard stop.
- Rust module tests: `cargo test -p <crate>` for the `fundamental` crate and the `tests` crate, with crate names resolved through `cargo metadata --no-deps --format-version 1`.
- Data-flow trace: HTTP GET with path `id` → SBOM existence check (404) → `sbom_package` ⋈ `package_license` query → classify and dedup → JSON `LicenseSummary`. All stages connect.
- Contract and sibling parity: the handler returns `Result<_, AppError>` with `.context()`, the same as siblings. The route uses the same caching layer as siblings. The 404 path matches `sbom/endpoints/get.rs`. No trait contracts are implemented.
- Duplication check: confirm no existing license classifier or category enum exists before keeping the new one.

## Step 10 / 11 — Commit, PR, Jira (simulated)

- Commit: `feat(package): add SBOM license summary endpoint`, with body and footer `Implements TC-9208`, and `--trailer="Assisted-by: Claude Code"`.
- `gh pr create --base main` (with fork flags if an `upstream` remote exists). The PR body contains `Implements [TC-9208](<webUrl>)`. A `Closes owner/repo#N` line is added only if `customfield_10747` has a value.
- Jira: set `customfield_10875` to the PR URL (ADF inlineCard). Add a comment containing the PR link, a summary, and the deviations (the test assertion style differs from siblings; any approved out-of-scope files), ending with the implement-task footnote. Transition to In Review.
