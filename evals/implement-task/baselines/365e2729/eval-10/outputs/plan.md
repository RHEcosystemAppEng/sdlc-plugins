# Implementation Plan — TC-9208: Add package license summary endpoint with tests

Skill: `/sdlc-workflow:implement-task` (followed from SKILL.md directly; simulated — no Jira, git, or Serena calls were made).

## Step 0 – Project Configuration validation

The mock CLAUDE.md (`claude-md-mock.md`) has everything the skill needs:
- Repository Registry: `trustify-backend` | Serena instance `serena_backend` | Path `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence: `mcp__<serena-instance>__<tool>` naming convention, with `serena_backend` (rust-analyzer). Limitation: indexing can take 30–60s on first use.

Result: validation passes, so the run continues.

## Step 1 – Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR | none (default flow) |
| Bookend Type | none |
| Dependencies | None |
| GitHub Issue (customfield_10747) | would be read from the issue; mock has no value, so skipped |
| webUrl | `https://redhat.atlassian.net/browse/TC-9208` (would be taken from the API response) |

All required sections are present, so there is nothing to ask the user before continuing.

## Steps 1.5 / 2 / 3 (simulated)
- 1.5: fetch the comments and look for a `[sdlc-workflow] Description digest:` comment. If one exists, compare it with `scripts/sha256-digest.py`. If none exists, log a warning and continue.
- 2: there are no dependencies, so nothing to check.
- 3: `jira.user_info()`, then assign TC-9208 to the current user, then transition it to In Progress.

## Step 4 – Code understanding (planned Serena calls on `serena_backend`)
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/package/endpoints/mod.rs`, `.../endpoints/list.rs`, `.../model/mod.rs`, `.../model/summary.rs`
- `find_symbol(include_body=true)` on the `list` handler in `package/endpoints/list.rs`, the route-registration function in `package/endpoints/mod.rs`, and `PackageSummary`. PackageSummary already has a license field, so check how licenses are represented there.
- `find_symbol` on the `package_license` entity (`entity/src/package_license.rs`) and on `sbom_package` (`entity/src/sbom_package.rs`). Purpose: confirm the Relation definitions for the JOIN path sbom → sbom_package → package → package_license.
- `find_symbol` on the SBOM `get` handler (`modules/fundamental/src/sbom/endpoints/get.rs`). It shows how a missing SBOM becomes a 404 (`AppError::NotFound` or similar), and the new handler should reuse that exact mechanism.
- `find_referencing_symbols` on the package route-registration function. This confirms how `server/main.rs` mounts it, and that adding a route does not break callers.
- `search_for_pattern` for existing license-classification logic (`permissive`, `copyleft`, `spdx`, `license_category`, `LicenseCategory`). If any classification helper or constant already exists, reuse it instead of declaring a new one (symbol deduplication).
- Read `CONVENTIONS.md` at the repo root. Extract its CI check commands (e.g. `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`) and any OpenAPI/codegen command, for Step 9.
- Documentation files to track: `README.md`, `docs/api.md` (REST API reference), `CONVENTIONS.md`.
- Sibling analysis: see `conventions.md`.

## Step 5 – Branch
```
git checkout main && git pull && git checkout -b TC-9208
```

## Step 6 – File changes

### Modify: `modules/fundamental/src/package/model/mod.rs`
- Add `pub mod license_summary;` next to the existing `pub mod summary;`, in the existing ordering style.

### Create: `modules/fundamental/src/package/model/license_summary.rs`
- `/// License summary for all packages in an SBOM, grouped by license category.`
  `#[derive(Serialize, Deserialize, Debug, Clone, PartialEq, Eq, Default, ToSchema)] pub struct LicenseSummary { pub permissive: LicenseCategorySummary, pub copyleft: LicenseCategorySummary, pub unknown: LicenseCategorySummary }`
- `/// Count and deduplicated, sorted list of license identifiers for one category.`
  `pub struct LicenseCategorySummary { pub count: u64 /* or usize per sibling convention */, pub licenses: Vec<String> }`
- `/// Category a license identifier belongs to.` A `LicenseCategory` enum (Permissive, Copyleft, Unknown) with `fn classify(id: &str) -> LicenseCategory`, which matches against known SPDX identifier sets (MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, …, which are permissive; GPL-*, LGPL-*, AGPL-*, MPL-2.0, EPL-*, …, which are copyleft; everything else, including empty or NOASSERTION, is unknown). This is only declared after Step 4's search confirms that no such classifier already exists.
- A constructor `LicenseSummary::from_licenses(impl IntoIterator<Item = String>)`, documented. It builds a `BTreeSet<String>` per category, so the lists come out deduplicated and deterministically sorted (AC: "Licenses are deduplicated within each category"), and sets `count = licenses.len()`. A count of distinct identifiers is the reading of AC #4 and Test Requirement #4, "duplicate licenses ... counted only once".
- The derives match the sibling model structs (`summary.rs`) for serde/utoipa.

### Create: `modules/fundamental/src/package/endpoints/license_summary.rs`
- Follows the structure of `package/endpoints/list.rs`: the same extractor style (`State`/db handle, `Path<Id>`), the same utoipa `#[utoipa::path(...)]` annotation style, and the same return type.
- `/// GET /api/v2/sbom/{id}/license-summary — returns license counts grouped by category for the SBOM's packages.`
  `pub async fn get_license_summary(...) -> Result<Json<LicenseSummary>, AppError>`
- Logic:
  1. Confirm the SBOM exists with the `sbom` entity find_by_id, with `.context("fetching SBOM")`. If it does not exist, return the same NotFound `AppError` the SBOM `get.rs` handler uses, which gives a 404.
  2. Run a SeaORM JOIN query from `sbom_package` (filtered by sbom id) to `package` to `package_license`, selecting the license identifier column (`.context("querying package licenses")`). The query is scoped to the single SBOM; it does not load all package licenses.
  3. Map NULL or missing license values to the `unknown` category defensively (`Option<String>` becomes `unwrap_or_default()`).
  4. Return `Json(LicenseSummary::from_licenses(..))`.
- Not paginated: the response is a single aggregate object, not a list, so `PaginatedResults<T>` does not apply. This is a deliberate deviation from the "list endpoints" convention, and it is justified because this is not a list endpoint.

### Modify: `modules/fundamental/src/package/endpoints/mod.rs`
- Add `mod license_summary;` and register `.route("/api/v2/sbom/{id}/license-summary", get(license_summary::get_license_summary))` in the same builder and style as the existing `/api/v2/package` routes, including any caching middleware config the siblings apply. Also add the handler to the module's OpenAPI path list if siblings register one.

### Create: `tests/api/package_license.rs`
- See `test-plan.md`.

### Documentation impact
- `docs/api.md` documents the REST API, so the new endpoint belongs there. However, it is **not** in Files to Modify, so it is flagged in Step 9 for user approval rather than edited unilaterally. If CONVENTIONS.md lists an OpenAPI generation command, run it in Step 9 and commit the generated spec changes as part of the deliverable.

## Scope / convention flags raised to the user (Step 4 / Step 9)
1. **Route location:** `/api/v2/sbom/{id}/...` is registered in the *package* module, but the `/api/v2/sbom` prefix is owned by `sbom/endpoints/mod.rs`. The task explicitly places it in package endpoints, and that is what the plan follows. Flag it so the user can confirm there will be no router path conflict or merge issue in `server/main.rs`.
2. **Service layer:** the module pattern is `model/ + service/ + endpoints/`, but `package/service/mod.rs` is not in Files to Modify. Plan: keep the query inside the handler file, to respect scope. Ask the user whether to move it into `PackageService` (an out-of-scope file).
3. **Test registration:** if the `tests` crate requires registering new test files (e.g. `[[test]]` in `tests/Cargo.toml`, or a `mod package_license;` in a test `main.rs`/`lib.rs`), that file is out of scope. Flag it for approval.
4. **`docs/api.md` update:** out of scope, flagged for approval (see above).

## Step 7 – Tests
See `test-plan.md`. Run `cargo test -p <tests crate>` and `cargo test -p <fundamental crate>`, with crate names resolved via `cargo metadata --no-deps --format-version 1`.

## Step 8 – Acceptance Criteria mapping
| AC | Satisfied by |
|---|---|
| Returns categorized license counts | handler + `LicenseSummary::from_licenses`; test 1 |
| 404 for missing SBOM | existence check + NotFound AppError; test 2 |
| Each category has count + list | `LicenseCategorySummary { count, licenses }`; tests 1 and 3 |
| Deduplicated within category | `BTreeSet` per category; test 4 |

## Step 9 – Self-verification (planned)
- Scope containment: `git diff --name-only` should list only the 2 modified files and 3 created files. Any extra file (flags 2–4) needs explicit approval.
- Untracked files, sensitive patterns, and the duplication check (grep for existing license classifiers).
- CI checks from CONVENTIONS.md, which are a hard stop on any non-zero exit, plus any OpenAPI generation command.
- Rust module-level tests for each crate touched.
- Data-flow trace: HTTP GET with path id, then SBOM existence check (404 if missing), then a JOIN query scoped to the SBOM, then classification and dedup, then a JSON response. Every stage connects.
- Query scope: filtered by sbom id at the database level.
- Contract and sibling parity: same extractors, error wrapping, utoipa annotations, and caching config as `list.rs`; the 404 behaviour matches `sbom/endpoints/get.rs`.

## Step 10 – Commit / PR
```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(package): add SBOM license summary endpoint

Adds GET /api/v2/sbom/{id}/license-summary returning deduplicated license
identifiers grouped into permissive, copyleft and unknown categories.

Implements TC-9208"
```
Run fork detection (`git remote get-url upstream`), then `gh pr create --base main`. The body includes `Implements [TC-9208](https://redhat.atlassian.net/browse/TC-9208)`, plus `Closes owner/repo#N` if the GitHub Issue field is set.

## Step 11 – Jira
Set `customfield_10875` to the PR URL as an ADF inlineCard. Add a comment with the PR link, a summary, and any deviations (the scope flags above, and the assertion-style deviation from siblings), ending with the implement-task footnote. Transition the issue to In Review.
