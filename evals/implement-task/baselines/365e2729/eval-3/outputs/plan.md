# Implementation Plan — TC-9203: Add package license filter to list endpoint

Skill: `/sdlc-workflow:implement-task` (eval mode: no Jira, git, or Serena calls were made. Each step says what would happen.)

## Step 0 — Project Configuration validation

The mock CLAUDE.md (`claude-md-mock.md`) has all the required sections:

- **Repository Registry**: `trustify-backend`, Serena instance `serena_backend`, path `./`
- **Jira Configuration**: Project key `TC`, Cloud ID `2b9e35e3-...`, Feature issue type ID `10142`, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`
- **Code Intelligence**: naming convention `mcp__<serena-instance>__<tool>`; instance `serena_backend` (rust-analyzer). Known limitation: indexing can take 30-60 seconds on first use.

Result: validation passes, so execution continues.

## Step 1 — Parse task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR | none (default flow) |
| Bookend Type | none |
| Dependencies | None |
| GitHub Issue (customfield_10747) | would be read from the issue. If it is empty, this is skipped silently. |

All required sections are present, so no clarification is needed.

## Step 1.5 / 2 / 3 — Digest check, dependencies, Jira transition (simulated)

- Would fetch the comments, find the `[sdlc-workflow] Description digest:` comment and compare digests with `scripts/sha256-digest.py`.
- No dependencies to verify.
- Would call `jira.user_info()`, assign TC-9203 to the current user and move it to **In Progress**.

## Step 4 — Understand the code (simulated with `serena_backend`)

Planned Serena calls:

- `get_symbols_overview` on `modules/fundamental/src/package/endpoints/list.rs` and `modules/fundamental/src/package/service/mod.rs`
- `find_symbol("apply_filter", include_body=true)` in `common/src/db/query.rs`, to confirm its signature and how it handles comma-separated values
- `find_symbol` on the advisory list handler and its Query struct in `modules/fundamental/src/advisory/endpoints/list.rs`, to see how the `severity` filter is done
- `find_symbol` in `modules/fundamental/src/advisory/service/advisory.rs`, to see how the advisory service passes the severity filter into the query
- `get_symbols_overview` on `entity/src/package_license.rs` (Entity, Column, Relation) and `entity/src/package.rs` (to check that a `Relation`/`Related` impl to `package_license` exists)
- `find_referencing_symbols` on `PackageService::list` and on the package list query struct, to find every caller that a signature change would affect
- Read `CONVENTIONS.md` at the repo root to get the CI check commands (fmt, clippy, check, test) and any OpenAPI generation command

**Siblings used for conventions:** the advisory and sbom `endpoints/list.rs` files, `advisory/service/advisory.rs`, `sbom/service/sbom.rs`, and `tests/api/advisory.rs` and `tests/api/sbom.rs`.

**Conventions found (these bind Steps 6 and 7):**

- **Errors:** handlers return `Result<T, AppError>` and wrap errors with `.context()`. Validation failures become an `AppError` that maps to 400.
- **Naming:** `snake_case` functions and `verb_noun` handler names. Query structs are named `<Entity>ListQuery` (or match the advisory equivalent).
- **Query parameters:** a `#[derive(Deserialize, IntoParams)]` Query struct with `Option<String>` filter fields, extracted with `Query<...>` in the handler.
- **Responses:** list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- **Filtering:** the shared helpers in `common/src/db/query.rs` are used. No raw SQL.
- **Tests:** integration tests in `tests/api/` run against a real PostgreSQL test DB and use `assert_eq!(resp.status(), StatusCode::OK)`.
- **Skill override:** tests must assert on values (package names or licenses in the response), not only on counts. Every test function gets a `///` doc comment and Given/When/Then comments.

**Documentation files found:** `README.md`, `docs/api.md` (REST API reference) and `CONVENTIONS.md`. `docs/api.md` probably documents the package endpoint's query parameters, but it is **not** in Files to Modify, so it is flagged in Step 9 instead of being edited.

## Step 5 — Branch (simulated)

```
git checkout main && git pull && git checkout -b TC-9203
```

## Step 6 — Changes

### Modify: `modules/fundamental/src/package/endpoints/list.rs`

1. Add `license: Option<String>` to the package list Query struct, following the advisory `severity` field exactly: same derives, same `IntoParams`/utoipa attributes, and a `///` doc comment saying it is a comma-separated list of SPDX identifiers. If the endpoint has no dedicated query struct yet, add the field to the struct the handler already extracts. Do not create a parallel struct.
2. In the handler, validate `license` before calling the service:
   - split on `,`, trim each value, and reject empty segments (for example `license=` or `MIT,,Apache-2.0`)
   - reject any value with characters outside the SPDX identifier set (`[A-Za-z0-9.+-]`, plus the `LicenseRef-` form)
   - on failure, return `AppError::BadRequest(...)` (or whichever existing variant maps to 400 in `common/src/error.rs`), with a message naming the bad value
3. Pass the validated license filter to `PackageService::list` alongside the existing pagination and query arguments.
4. Leave the response type alone. It stays `PaginatedResults<PackageSummary>`.
5. Update the `#[utoipa::path]` params if the sibling advisory handler documents its params there. This is what lets the OpenAPI generation command pick up the new parameter.

### Modify: `modules/fundamental/src/package/service/mod.rs`

1. Extend `PackageService::list` to accept the license filter, as `Option<&str>` or the validated `Vec<String>`, matching how the advisory service receives `severity`.
2. When the filter is present:
   - join `package` to `package_license` using the SeaORM relation from `entity/src/package_license.rs`, via `.join(JoinType::InnerJoin, entity::package::Relation::PackageLicense.def())` or `find_also_related`, whichever the existing code uses
   - call `common::db::query::apply_filter` with `entity::package_license::Column::License` (or the actual license column) and the raw parameter. That call handles the comma split and builds the `IN (...)` clause.
   - add `.distinct()` (or group by package id) so a package that matches several requested licenses appears only once and the pagination totals stay correct
3. When the filter is absent, build the same query as today, with no join, so there is no regression and no performance change for unfiltered requests.
4. Update every caller found with `find_referencing_symbols`. Within scope, the expected only caller is `endpoints/list.rs`. Any other caller is flagged in Step 9.

### Create: `tests/api/package_license_filter.rs`

Integration tests that follow the `tests/api/advisory.rs` setup (test DB fixture, app/client builder). Each test has a `///` doc comment and Given/When/Then sections:

| Test | Seed data | Request | Assertions |
|---|---|---|---|
| `test_filter_single_license` | pkg-a (MIT), pkg-b (Apache-2.0), pkg-c (GPL-3.0-only) | `?license=MIT` | status is 200. Returned package names are exactly `["pkg-a"]`. Every item's `license` is `"MIT"`. |
| `test_filter_multiple_licenses` | same | `?license=MIT,Apache-2.0` | status is 200. Sorted names are `["pkg-a","pkg-b"]`. pkg-c is absent. |
| `test_no_license_filter_returns_all` | same | no parameter | status is 200. Names are `["pkg-a","pkg-b","pkg-c"]`. Body deserializes as `PaginatedResults<PackageSummary>`, which proves the shape did not change. |
| `test_invalid_license_returns_400` | same | `?license=MIT,,` and `?license=%3Cscript%3E` | status is `StatusCode::BAD_REQUEST` |

The three success cases share an algorithm (seed, call with a parameter, compare the name set). If the sibling tests use `rstest`, they become one parameterized `#[rstest]` test with cases. If they don't, they stay as separate tests to match the project. The 400 test is separate because its assertions are different.

**Test registration risk:** `tests/` has its own `Cargo.toml`. If test files must be registered (a `[[test]]` entry or a `mod package_license_filter;` in a test root), that file is outside Files to Modify. It would be flagged for approval in Step 9, not edited silently.

## Step 7 — Run tests (simulated)

`cargo test -p <tests crate>` and `cargo test -p <fundamental crate>`. Crate names would be resolved with `cargo metadata --no-deps --format-version 1`.

## Step 8 — Acceptance criteria

| Criterion | Covered by |
|---|---|
| `?license=MIT` returns only MIT packages | service join plus `apply_filter`; `test_filter_single_license` |
| `?license=MIT,Apache-2.0` returns packages matching either | multi-value handling in `apply_filter` plus `distinct`; `test_filter_multiple_licenses` |
| No parameter returns all packages | join and filter only applied when the value is `Some`; `test_no_license_filter_returns_all` |
| Response shape unchanged | return type untouched; deserialized into `PaginatedResults<PackageSummary>` in the test |
| Invalid values return 400 | handler validation returning `AppError` (400); `test_invalid_license_returns_400` |

## Step 9 — Self-verification

- **Scope containment:** the expected diff is the two modified files and the one new test file. Possible out-of-scope items, each flagged for user approval:
  - test registration in `tests/Cargo.toml` or a test root module
  - `docs/api.md`, to document the parameter
  - a generated OpenAPI spec file, if `CONVENTIONS.md` lists a generation command
- **Duplication check:** grep for `split(',')` in the new code. The comma parsing must come from `apply_filter` and must not be reimplemented. The validation helper only checks characters; it does not build the filter.
- **Symbol deduplication:** before adding an SPDX validation regex or constant, search `common/` and `modules/` for an existing license or SPDX validator. Reuse it if one exists.
- **Data-flow trace:** HTTP query `license` → Query struct (`Option<String>`) → handler validation (400 on failure) → `PackageService::list(license)` → SeaORM join on `package_license` plus `apply_filter` IN clause → `PaginatedResults<PackageSummary>` → JSON. Every stage connects.
- **Query scope:** the join and filter happen in the database. Nothing is filtered in memory after fetching.
- **Contract and sibling parity:**
  - Query struct derives match the advisory struct.
  - Error handling uses `AppError` with `.context()`.
  - Callers of `PackageService::list` are updated.
  - The package table is only read; nothing is written to the shared entity.
- **Dead parameters:** none expected. Nothing is removed.
- **CI:** run every CI command from `CONVENTIONS.md` (for example `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo check`) and the OpenAPI generation command. Any failure is a hard stop.
- **Module tests:** `cargo test -p` for the fundamental crate and the tests crate.

## Step 10 — Commit and PR (simulated)

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(package): add license filter to package list endpoint

Adds an optional comma-separated `license` query parameter to
GET /api/v2/package, reusing common::db::query::apply_filter and the
package_license entity join, mirroring the advisory severity filter.

Implements TC-9203"
```

`git remote get-url upstream` decides whether this is a fork. Then `gh pr create --base main` (adding `-R`/`--head` if it is a fork). The PR body includes `Implements [TC-9203](<webUrl>)` and, if the GitHub Issue field is set, `Closes <owner>/<repo>#<n>`.

## Step 11 — Jira (simulated)

- Set `customfield_10875` to the PR URL as an ADF `inlineCard`.
- Add a comment with the PR link, a summary of the changes and any deviations (for example, approved scope additions), ending with the implement-task footnote.
- Move the task to **In Review**.
