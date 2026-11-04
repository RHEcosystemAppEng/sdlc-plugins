# Implementation Plan — TC-9203: Add package license filter to list endpoint

> Simulated run of `/sdlc-workflow:implement-task TC-9203`. No repository files were modified,
> and no external tools (Jira, git, Serena, gh) were called. Each step says what would happen.

## Step 0 — Project Configuration validation

The mock CLAUDE.md (`claude-md-mock.md`) has all required sections:

- **Repository Registry**: `trustify-backend` | Rust backend service | Serena instance `serena_backend` | path `./`
- **Jira Configuration**: Project key `TC`, Cloud ID `2b9e35e3-...`, Feature issue type ID `10142`,
  Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
- **Code Intelligence**: naming convention `mcp__<serena-instance>__<tool>`. Limitation:
  rust-analyzer can take 30-60s to index on first use.

Result: the check passes, so the run continues.

## Step 1 — Parse task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR | none (default flow) |
| Bookend Type | none (normal implementation) |
| Dependencies | None |
| GitHub Issue (customfield_10747) | would be read from the issue. If it is empty, skip it. |

All required sections are present (Repository, Target Branch, Description, Files to Modify,
Files to Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements).
The task also has a **Reuse Candidates** section, which drives the reuse strategy below.

## Steps 1.5 – 3 — Jira (simulated)

- 1.5: would fetch comments, find the `[sdlc-workflow] Description digest:` comment and compare the digest.
- 2: no dependencies to check.
- 3: would assign TC-9203 to the current user and move it to **In Progress**.

## Step 4 — Understand the code (would use `serena_backend`)

These are the planned inspections. Allow for rust-analyzer's indexing delay on first use.

1. `mcp__serena_backend__get_symbols_overview` on
   - `modules/fundamental/src/package/endpoints/list.rs`
   - `modules/fundamental/src/package/service/mod.rs`
2. `mcp__serena_backend__find_symbol(include_body=true)` on:
   - the advisory list handler and its Query struct in `modules/fundamental/src/advisory/endpoints/list.rs`.
     This is the reference for how `severity` is declared, parsed and passed on.
   - `AdvisoryService::list` in `modules/fundamental/src/advisory/service/advisory.rs`, to see how
     the severity filter reaches the service and is passed to `apply_filter`
   - `apply_filter` in `common/src/db/query.rs`, to get its exact signature: input type, column
     argument, return type and error behaviour on empty or bad values
   - `PackageService::list` and the package list handler
   - the `package_license` entity (`entity/src/package_license.rs`): the `Relation` enum, the
     `Related<package::Entity>` impl and the license column name (e.g. `license` / `spdx_id`)
3. `mcp__serena_backend__find_referencing_symbols` on `PackageService::list`, to find every caller
   (the package list handler, and possibly search or other modules) that must change if the
   signature changes.
4. `mcp__serena_backend__search_for_pattern` for `license` across `common/` and `modules/` to find
   any existing SPDX validation helper or license constants before writing new ones.
5. Siblings for convention analysis: `advisory/endpoints/list.rs`, `sbom/endpoints/list.rs`,
   `advisory/service/advisory.rs`, `sbom/service/sbom.rs`. Test siblings: `tests/api/advisory.rs`
   and `tests/api/sbom.rs`.
6. **CONVENTIONS.md**: would read `./CONVENTIONS.md` at the repo root, pull out its CI check
   commands (e.g. `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo check`) and any codegen
   commands (e.g. OpenAPI spec generation) for Step 9.
7. **Documentation files**: `README.md`, `docs/api.md` (the REST API reference, which describes
   `GET /api/v2/package`) and `docs/architecture.md`.

### Expected conventions (from repo-backend.md; would be confirmed against siblings)

- **Framework**: Axum handlers and SeaORM queries.
- **Error handling**: handlers return `Result<T, AppError>` with `.context()` wrapping. `AppError`
  (`common/src/error.rs`) implements `IntoResponse`, so a `BadRequest`-type variant maps to HTTP 400.
- **Query params**: a `#[derive(Deserialize)]` Query struct with `Option<String>` fields, extracted
  with `Query<...>` alongside the pagination params (as with `severity` in advisory).
- **Responses**: list endpoints return `PaginatedResults<T>` (`common/src/model/paginated.rs`).
- **Module layout**: `model/ + service/ + endpoints/`. Routes are registered in `endpoints/mod.rs`.
- **Tests**: integration tests in `tests/api/` run against a real PostgreSQL database, using
  `assert_eq!(resp.status(), StatusCode::OK)`.

## Step 5 — Branch (simulated)

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 — Changes

Scope is limited to the three files listed in the task. No other files would be planned for change.

### 1. MODIFY `modules/fundamental/src/package/endpoints/list.rs`

- Add an optional `license` field to the package list Query struct. It mirrors the advisory
  `severity` field exactly:
  ```rust
  /// Query parameters accepted by `GET /api/v2/package`.
  #[derive(Debug, Default, Deserialize, IntoParams)]
  pub struct PackageListQuery {
      /// Optional license filter: a single SPDX identifier or a comma-separated list
      /// (e.g. `MIT` or `MIT,Apache-2.0`). Packages matching any listed license are returned.
      #[serde(default)]
      pub license: Option<String>,
      // ...existing fields (search / pagination) unchanged
  }
  ```
  If the handler currently uses only a shared pagination/search query type, add a separate
  `Query<PackageListQuery>` extractor, in the same way the advisory handler adds its severity
  extractor. The shape follows whatever advisory does.
- **Validation (400 Bad Request)**: before calling the service, validate the raw `license` value.
  Reject an empty string, empty items after splitting on commas (e.g. `MIT,,` or `,`), and items
  that are not valid SPDX identifier syntax (allowed characters `[A-Za-z0-9.+-]`, with optional
  `LicenseRef-` prefix). Return the existing `AppError` bad-request variant, so no new error type is
  added. If `apply_filter` already rejects malformed input with an `AppError` that maps to 400,
  rely on that and add only the SPDX character check. Step 4 inspection decides this, and there
  will be no second, duplicate parser.
- Pass the filter on to the service with `.context("...")` wrapping, matching sibling handlers:
  `state.package_service.list(query.license.as_deref(), paginated, &db).await.context("listing packages")?`
- The return type stays `Result<Json<PaginatedResults<PackageSummary>>, AppError>`, so the
  response shape does not change.
- Update the `#[utoipa::path(...)]` `params(...)` attribute (if the advisory endpoint uses one) to
  document the new `license` parameter. This keeps the generated OpenAPI spec accurate.

### 2. MODIFY `modules/fundamental/src/package/service/mod.rs`

- Extend `PackageService::list` with a `license: Option<&str>` parameter, in the same position and
  style as the `severity` argument of `AdvisoryService::list`.
- When `license` is `Some`, join `package` to `package_license` through the SeaORM relation from
  `entity::package_license`, and apply the filter with the shared helper:
  ```rust
  let mut select = package::Entity::find();
  if let Some(license) = license {
      select = select
          .join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())
          // apply_filter parses "MIT,Apache-2.0" into an IN (...) clause, or "MIT" into =
          ;
      select = apply_filter(select, package_license::Column::License, license)?;
      // A package with several matching licenses must not appear twice
      select = select.distinct();
  }
  ```
  The exact relation and column names, and the exact `apply_filter` argument order and return
  type, come from the Step 4 `find_symbol` output. The snippet shows intent only.
- Add `.distinct()` (or a `GROUP BY package.id`) when the join is active. A package mapped to both
  MIT and Apache-2.0 must be returned once for `?license=MIT,Apache-2.0`, and the paginated
  `total` must count distinct packages. This keeps the `PaginatedResults<PackageSummary>` shape
  and counts correct.
- With no filter (`license == None`), the query is unchanged: no join and no extra clause. This
  meets the "no regression" criterion.
- Update every caller found with `find_referencing_symbols`. Callers inside the listed files get
  updated. If a caller lives outside the listed files (e.g. the search module), it is **not**
  edited. Instead it is flagged for user approval in Step 9 scope containment. A fallback is to
  keep the old signature and add a `list_filtered` variant, but extending the signature is
  preferred if every caller is in scope.
- Add or extend a doc comment on `list` that describes the `license` parameter.

### 3. CREATE `tests/api/package_license_filter.rs`

Integration tests follow the `tests/api/advisory.rs` style: a real PostgreSQL test DB,
`assert_eq!(resp.status(), StatusCode::OK)`, and the same fixture/setup helpers. Each test function
gets a `///` doc comment and `// Given / // When / // Then` sections.

Fixture: seed packages `pkg-mit` (MIT), `pkg-apache` (Apache-2.0), `pkg-gpl` (GPL-3.0-only), and
`pkg-dual` (MIT and Apache-2.0, to cover de-duplication) through the `package_license` mapping.

| Test | Asserts |
|---|---|
| `test_list_packages_single_license_filter` | `?license=MIT` gives 200, and the returned package **names** equal exactly `{pkg-dual, pkg-mit}` (value-based, not just a count) |
| `test_list_packages_multi_license_filter` | `?license=MIT,Apache-2.0` gives 200, names equal `{pkg-apache, pkg-dual, pkg-mit}`, `pkg-dual` appears once, `total == 3` |
| `test_list_packages_without_license_filter` | no param gives 200, all four seeded packages are returned, and the response deserializes as `PaginatedResults<PackageSummary>` with the same fields as before (shape unchanged) |
| `test_list_packages_invalid_license_returns_400` | invalid values (`""`, `MIT,,`, `,`, `MIT;DROP`) each give `StatusCode::BAD_REQUEST` |

The single and multi filter tests share the same setup, action and assertion structure, so they
could be one table-driven case. The invalid-input cases are the main candidate for parameterizing,
with `rstest` `#[case]` or a simple loop over inputs. That is used **only if** the sibling tests
(`tests/api/*.rs`) already use `rstest` or table-driven loops. If they do not, the plan follows the
project pattern and writes separate test functions or a plain loop inside one test.

**Test registration**: the new file probably has to be registered (e.g. a `[[test]]` entry in
`tests/Cargo.toml` or a `mod package_license_filter;` line in a tests `main.rs`/`lib.rs`). That file
is not in Files to Create/Modify, so it is flagged in Step 9 scope containment for user approval
rather than planned silently.

### Documentation impact

The task has no Documentation Updates section. `docs/api.md` describes `GET /api/v2/package` and
would become out of date once the new `license` param exists. It is **not** in the task's file
scope, so it is flagged for user approval in Step 9 and not edited unilaterally. The utoipa
annotation in `list.rs` (which is in scope) keeps the generated OpenAPI spec accurate.

## Step 7 — Test run (simulated)

`cargo test -p <crate>` for each affected crate, with crate names taken from `cargo metadata`
(not guessed from the nearest Cargo.toml). The expected crates are the fundamental module crate
and the tests crate.

## Step 8 — Acceptance criteria mapping

| Criterion | How it is met |
|---|---|
| `?license=MIT` returns only MIT packages | Join on `package_license` plus `apply_filter` equality. Covered by the single-filter test |
| `?license=MIT,Apache-2.0` returns either | `apply_filter` builds an IN clause, with `.distinct()`. Covered by the multi-filter test |
| No param returns all packages | Join and filter are skipped when `None`. Covered by the no-filter test |
| Response shape unchanged | Handler return type stays `PaginatedResults<PackageSummary>`. Asserted in the no-filter test |
| Invalid values return 400 | Handler validation returns `AppError` bad request. Covered by the invalid test |

## Step 9 — Self-verification plan

- **Scope containment**: expected diff is `list.rs`, `service/mod.rs` and
  `tests/api/package_license_filter.rs`. These would be flagged for approval if needed:
  `tests/Cargo.toml` (test registration), `docs/api.md` (doc currency), and any
  `PackageService::list` caller outside these files.
- **Symbol deduplication / duplication check**: grep for `license`, `spdx`, `SPDX` and
  comma-splitting helpers (`split(',')`) across `common/` and `modules/`. Do not write a new
  comma-split parser, and do not redeclare the `package_license` relation.
- **Defensive access**: guard `Option<String>` with `as_deref()` and do not unwrap. Treat
  whitespace-trimmed empty items as invalid.
- **Dead parameters**: none expected, because nothing is removed.
- **CI checks**: run every command listed in CONVENTIONS.md, plus any OpenAPI codegen command,
  and commit generated changes. Any non-zero exit is a hard stop.
- **Rust module tests**: `cargo test -p <crate>` for each crate containing modified files.
- **Data-flow trace**: HTTP query string, then `Query<PackageListQuery>` deserialization, then
  validation (400 on failure), then `PackageService::list(license)`, then SeaORM select with
  `package_license` join and `apply_filter` IN/=, then `.distinct()` with pagination, then
  `PaginatedResults<PackageSummary>` JSON. Every stage connects to the next.
- **Query scope**: the filter is pushed into SQL (JOIN + WHERE IN). There is no in-memory
  filtering after loading all packages.
- **Contract and sibling parity**: the handler signature and error handling match the advisory
  list handler. The utoipa params match. The service's use of `apply_filter` matches
  `AdvisoryService::list`. The `package_license` join is read-only, so cross-module write concerns
  do not apply. For the caller site, every `PackageService::list` caller is updated consistently.
- **Sensitive-pattern check** on the staged diff.

## Step 10 — Commit and PR (simulated)

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(package): add license filter to package list endpoint

Add optional `license` query parameter (single or comma-separated SPDX ids)
to GET /api/v2/package. Reuses common::db::query::apply_filter and the
package_license entity join, following the advisory severity filter pattern.

Implements TC-9203"
```

Fork detection would use `git remote get-url upstream`. Then
`gh pr create --base main ...` (or the fork variant with `-R`/`--head`). The PR body includes
`Implements [TC-9203](<webUrl>)` and a `Closes <owner>/<repo>#<n>` line if customfield_10747
is set.

## Step 11 — Jira (simulated)

- Set `customfield_10875` to the PR URL as an ADF `inlineCard`.
- Add a comment with the PR link, a summary of changes and any deviations (e.g. approval of
  out-of-scope test registration or docs), ending with the implement-task comment footnote.
- Move the issue to **In Review**.
