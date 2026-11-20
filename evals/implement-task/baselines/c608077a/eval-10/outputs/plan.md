# Implementation Plan — TC-9208: Add package license summary endpoint with tests

## Step 0 — Project Configuration validation

The mock CLAUDE.md (claude-md-mock.md) has everything the skill needs:
- Repository Registry: `trustify-backend` → Serena instance `serena_backend`, path `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence: tool naming convention `mcp__<serena-instance>__<tool>`, instance `serena_backend` (rust-analyzer)

Validation passes, so the skill continues.

## Step 1 — Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR | none (default flow) |
| Bookend Type | none |
| Dependencies | None (Step 2 has nothing to check) |
| GitHub Issue | customfield_10747 would be read. The mock gives no value, so this is skipped. |

Every required section is present, so there is no reason to stop for clarification.

Step 1.5 (digest check), Step 3 (assign and move to In Progress) and Step 5 (`git checkout main && git pull && git checkout -b TC-9208`) would run normally. They are only described here, not run, because this is an eval.

## Step 4 — Code understanding (planned Serena calls)

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/package/endpoints/mod.rs`, `.../endpoints/list.rs` and `.../model/mod.rs`
- `find_symbol include_body=true` on the list handler in `package/endpoints/list.rs`, which is the reference pattern named in Implementation Notes
- `get_symbols_overview` on `entity/src/package_license.rs` and `entity/src/sbom_package.rs` to learn the column and relation names for the JOIN
- `find_symbol` on `AppError` in `common/src/error.rs` to confirm it has a NotFound variant and to see how `.context()` is used
- `get_symbols_overview` on `sbom/endpoints/get.rs` to see how a `{id}` path parameter is extracted and how a missing SBOM becomes a 404
- Read `CONVENTIONS.md` at the repo root and pull out its CI check commands for Step 9
- Siblings for the convention analysis: `package/model/summary.rs`, `sbom/model/summary.rs`, `advisory/model/summary.rs` (models); `package/endpoints/list.rs`, `sbom/endpoints/get.rs`, `advisory/endpoints/get.rs` (handlers); `tests/api/sbom.rs`, `tests/api/advisory.rs` (tests)
- Search for existing license-classification helpers with `search_for_pattern "permissive|copyleft|LicenseCategory|classify_license"` across the workspace, so nothing is duplicated (symbol deduplication)
- Docs to check later: `README.md`, `docs/api.md` (the REST API reference)

## Step 6 — Changes per file

The work stays inside Files to Modify and Files to Create.

### MODIFY `modules/fundamental/src/package/model/mod.rs`
- Add `pub mod license_summary;` next to the existing `pub mod summary;`, in the same order and style.

### CREATE `modules/fundamental/src/package/model/license_summary.rs`
- `/// License identifiers and their distinct count for one license category.`
  `pub struct LicenseCategorySummary { pub count: u64, pub licenses: Vec<String> }`
- `/// Package licenses in an SBOM, grouped into permissive, copyleft and unknown categories.`
  `pub struct LicenseSummary { pub permissive: LicenseCategorySummary, pub copyleft: LicenseCategorySummary, pub unknown: LicenseCategorySummary }`
- Use the same derives as the sibling `PackageSummary`: `Serialize, Deserialize, Debug, Clone, PartialEq, Eq, Default`, plus `utoipa::ToSchema` if the siblings have it. `Default` gives the all-zeros, empty-lists result.
- Add a doc comment on each public item.
- `/// Builds a summary from raw license identifiers. Classifies each one, deduplicates within its category and sorts it for deterministic output.`
  `impl LicenseSummary { pub fn from_licenses<I: IntoIterator<Item = S>, S: AsRef<str>>(iter: I) -> Self }`
  - It collects into a `BTreeSet<String>` per category, which deduplicates and gives a stable order. Then `count = set.len() as u64` and `licenses = set.into_iter().collect()`.
- `/// Maps an SPDX license identifier to its category.` This is a private `fn classify(id: &str) -> Category` with small constant lists of permissive IDs (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, ...) and copyleft IDs (GPL-*, LGPL-*, AGPL-*, MPL-2.0, EPL-*, ...). Anything else, including empty or NOASSERTION, counts as unknown.
  - These lists are only declared if the search in Step 4 finds no existing classification constant.
- Null-safety: license values come from the DB as `Option<String>`. Map `None` and empty strings to unknown with `.unwrap_or_default()` instead of unwrapping.

### CREATE `modules/fundamental/src/package/endpoints/license_summary.rs`
- Follow the pattern in `package/endpoints/list.rs`: the same extractor style (`State`/DB connection, `Path<Id>`), the same `#[utoipa::path(...)]` annotation if siblings use it, and the same import order.
- `/// GET /api/v2/sbom/{id}/license-summary — returns license counts per category for the packages in an SBOM.`
  `pub async fn get_license_summary(...) -> Result<Json<LicenseSummary>, AppError>`
  1. Look up the SBOM with `entity::sbom::Entity::find_by_id(id)`. If it is missing, return the NotFound `AppError` variant, mirroring `sbom/endpoints/get.rs`. This covers the 404 criterion.
  2. Select the license column from `entity::package_license`, joined through `entity::sbom_package` and filtered by `sbom_id = id`. Every DB call gets `.context("...")`.
  3. Return `Json(LicenseSummary::from_licenses(rows))`. An SBOM with no packages gives `Default`, which is all zeros.
- Query scope: the query filters to the one SBOM at the database. It does not load all licenses.
- The query lives in the handler because `package/service/mod.rs` is not in Files to Modify. If the sibling pattern clearly needs a `PackageService` method, that file is flagged under scope containment and the user is asked before it changes.

### MODIFY `modules/fundamental/src/package/endpoints/mod.rs`
- Add `mod license_summary;` and register `.route("/api/v2/sbom/{id}/license-summary", get(license_summary::get_license_summary))` in the existing router builder.
- Copy whatever caching-layer and OpenAPI registration the sibling routes use.

### CREATE `tests/api/package_license.rs`
- See test-plan.md for the details.

## Possible out-of-scope files (flagged, not changed)

These would be raised in Step 9's scope containment check and need user approval:
- The test harness entry point (for example `tests/api/main.rs`, `tests/api/mod.rs` or a `[[test]]` entry in `tests/Cargo.toml`). It may need `mod package_license;` for the new test file to compile.
- `docs/api.md`, if it lists endpoints. Documentation impact suggests adding the new endpoint, but it is not in scope, so it is flagged.
- The OpenAPI spec, if CONVENTIONS.md lists a generation command. The generated changes would be committed as an artifact, as Step 9 allows.
- `package/service/mod.rs`, only if a service-layer method turns out to be required (see above).

## Steps 7–9

- Tests: see test-plan.md. Run `cargo test -p tests` (resolving the package name with `cargo metadata`) and `cargo test -p trustify-module-fundamental` (or whatever name `cargo metadata` resolves for `modules/fundamental`).
- Run every CI command found in CONVENTIONS.md (for example `cargo fmt --check`, `cargo clippy -- -D warnings`). Any failure is a hard stop.
- Acceptance criteria and how each is met:
  - Categorized counts: `LicenseSummary` built by `from_licenses`.
  - 404 for a missing SBOM: the SBOM lookup runs first.
  - Each category has a count and a list: `LicenseCategorySummary { count, licenses }`.
  - Deduplication: `BTreeSet`.
- Data flow: `Path(id)` → SBOM existence check → JOIN query over `sbom_package` and `package_license` → classification and dedup → `Json` response. Every stage connects to the next.
- Contract and sibling parity: same error type, same extractors and same route registration as the sibling handlers. This is a read-only endpoint, so the cross-module write concerns do not apply.

## Steps 10–11 (described only)

- Commit: `feat(package): add SBOM license summary endpoint` with footer `Implements TC-9208` and `--trailer="Assisted-by: Claude Code (Claude Opus 5.5)"`.
- PR: `gh pr create --base main` (adding `-R`/`--head` if a fork is detected). The body links `Implements [TC-9208](<webUrl>)`.
- Jira: set `customfield_10875` to the PR URL as an ADF inlineCard, add a comment with the footnote (PR link, summary, deviations), then move to In Review.
