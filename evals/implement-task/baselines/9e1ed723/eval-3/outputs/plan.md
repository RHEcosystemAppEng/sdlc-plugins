# Implementation Plan — TC-9203: Add package license filter to list endpoint

Run in simulated mode: no Jira, git, or Serena calls were made. The repository structure
comes from `repo-backend.md` and the project configuration from `claude-md-mock.md`.

## Step 0 — Project Configuration validation

| Section | Status |
|---|---|
| Repository Registry | Present: `trustify-backend` → Serena instance `serena_backend`, path `./` |
| Jira Configuration | Present: Project key `TC`, Cloud ID, Feature issue type ID `10142` (also Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`) |
| Code Intelligence | Present: naming convention `mcp__<serena-instance>__<tool>`, instance `serena_backend` (rust-analyzer). Known limitation: indexing can take 30–60 seconds on first use |

Result: the configuration is valid, so execution continues.

## Step 1 — Parsed task

- **Repository:** trustify-backend
- **Target Branch:** `main`, so this is the default flow (direct to main)
- **Target PR:** none, so a new branch and PR are needed
- **Bookend Type:** none, so this is a normal implementation task
- **Dependencies:** none, so Step 2 has nothing to check
- **GitHub Issue (customfield_10747):** would be read from the fetched issue. If it is set, add `Closes <owner>/<repo>#<n>` to the PR body.
- **Files to Modify:**
  - `modules/fundamental/src/package/endpoints/list.rs`
  - `modules/fundamental/src/package/service/mod.rs`
- **Files to Create:**
  - `tests/api/package_license_filter.rs`
- **API Changes:** `GET /api/v2/package?license=MIT` and `?license=MIT,Apache-2.0` (MODIFY: add an optional query parameter)
- All required sections are present, so there is nothing to ask the user before starting.

## Step 1.5 — Description integrity (simulated)
The skill would call `jira.get_issue_comments(TC-9203)`, find the most recent
`[sdlc-workflow] Description digest:` comment, and compare it with
`python3 scripts/sha256-digest.py`. If no digest comment exists, it logs a warning and continues.

## Step 3 — Jira (simulated)
The skill would call `jira.user_info()`, then
`jira.edit_issue(TC-9203, assignee=<me>)`, then transition the issue to **In Progress**.

## Step 4 — Understanding the code (planned Serena calls on `serena_backend`)

1. `mcp__serena_backend__get_symbols_overview` on
   `modules/fundamental/src/package/endpoints/list.rs` and `.../package/service/mod.rs`.
   Purpose: find the existing list handler, its Query/params struct, and `PackageService::list`.
2. `mcp__serena_backend__find_symbol` (with `include_body=true`) on:
   - `common/src/db/query.rs` → `apply_filter`, to confirm its signature, its
     comma-splitting behaviour, and how it builds the `IN` clause
   - `modules/fundamental/src/advisory/endpoints/list.rs` → the advisory list Query struct
     and handler. This is the reference pattern for the `severity` filter.
   - `modules/fundamental/src/advisory/service/advisory.rs` → `AdvisoryService::list`, to see
     how the severity value is passed into the service and on to `apply_filter`
   - `entity/src/package_license.rs` → `Entity`, `Column`, and `Relation` (how it links to
     `package::Entity`)
   - `entity/src/package.rs` → the `Relation` / `Related<package_license::Entity>` impl
3. `mcp__serena_backend__find_referencing_symbols` on `PackageService::list`. This finds every
   caller (the endpoint, and possibly the search module or tests) so that changing the
   signature does not break them.
4. `mcp__serena_backend__search_for_pattern` for `license` across `modules/` and `common/`.
   This finds any existing license parsing or SPDX validation helper (see Symbol deduplication).
5. Sibling conventions: `get_symbols_overview` on `sbom/endpoints/list.rs`,
   `advisory/endpoints/list.rs`, and the test files `tests/api/advisory.rs` and `tests/api/sbom.rs`.
6. Read `CONVENTIONS.md` at the repo root. Extract the CI-check commands (fmt, clippy, check,
   test) and any OpenAPI or code generation command.
7. Documentation files to check: `README.md`, `CONVENTIONS.md`, `docs/api.md` (REST API
   reference, listed in the CLAUDE.md docs section).

### Discovered/expected conventions (binding for Steps 6–7)
- **Framework:** Axum handlers and SeaORM queries.
- **Error handling:** handlers return `Result<T, AppError>` and wrap errors with `.context()`.
  Bad input is reported as an `AppError` variant that maps to 400 (`common/src/error.rs`).
- **Query params:** each list endpoint has a `#[derive(Deserialize)]` Query struct with
  `Option<String>` filter fields, extracted with `Query<...>` (the advisory `severity` pattern).
- **Responses:** list endpoints return `PaginatedResults<T>` (`common/src/model/paginated.rs`).
- **Module layout:** `model/ + service/ + endpoints/`. Routes are registered in `endpoints/mod.rs`.
- **Tests:** integration tests live in `tests/api/<name>.rs`, run against a real PostgreSQL
  test database, and assert with `assert_eq!(resp.status(), StatusCode::OK)`.
- **Skill overrides:** tests use value-based assertions (not only length checks), each has a
  `///` doc comment, and non-trivial tests use given/when/then comments.

No conflict between the task description and these conventions is expected.

## Step 5 — Branch (simulated)
```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 — Changes per file

### 1. `modules/fundamental/src/package/endpoints/list.rs` (MODIFY)
- Add the field `pub license: Option<String>` to the existing package list Query struct,
  with a `///` doc comment. The field mirrors the `severity: Option<String>` field in
  `advisory/endpoints/list.rs`. Keep `#[serde(default)]` / `IntoParams` derives consistent
  with the advisory struct so the OpenAPI (utoipa) params pick up the new field.
- Validate in the handler before calling the service:
  - Split the value on `,`, trim each part, and reject the request if any part is empty
    (for example `license=` or `license=MIT,,`) or contains characters outside the SPDX
    identifier grammar (`[A-Za-z0-9.\-+]`, plus the `LicenseRef-` prefix).
  - Return the existing `AppError` bad-request variant, which maps to **400**. Do not invent
    a new error type.
  - Before writing a validator, check whether `apply_filter` or another helper in
    `common/src/db/query.rs` already validates values or returns a parse error. If it does,
    use that and propagate its error to keep a single source of truth. A new private
    `fn validate_license_ids(&str) -> Result<(), AppError>` is written only if no such helper
    exists. It would live in this file, with a doc comment.
- Pass `query.license.as_deref()` through to `PackageService::list`, in the same way the
  advisory handler passes `severity`.
- Leave the response type `PaginatedResults<PackageSummary>` and the route registration
  (`package/endpoints/mod.rs`) unchanged.

### 2. `modules/fundamental/src/package/service/mod.rs` (MODIFY)
- Extend `PackageService::list` with a `license: Option<&str>` parameter, or add it to the
  existing filter/params struct if `list` already takes one. Choose whichever matches
  `AdvisoryService::list`.
- Build the query with SeaORM:
  ```rust
  let mut select = package::Entity::find();
  if let Some(license) = license {
      select = select
          .join(JoinType::InnerJoin, package::Relation::PackageLicense.def())
          .distinct(); // a package with several licenses must not appear twice
      select = apply_filter(select, package_license::Column::License, license);
  }
  ```
  - The join goes through the `package_license` entity and its relation, not raw SQL.
  - `apply_filter` (from `common/src/db/query.rs`) is reused unchanged. It splits
    comma-separated values and emits `= value` for one value or `IN (...)` for several.
  - Use `DISTINCT` (or group by package id) so that a package matching both `MIT` and
    `Apache-2.0` appears once and pagination totals stay correct.
- The existing pagination and sorting helpers from `query.rs` still apply, and the count
  query uses the same filtered `select`.
- Update every caller found by `find_referencing_symbols`. If a caller lives outside the two
  listed files (for example the search module), flag it in Step 9 rather than editing it
  silently. Options: pass `None`, or add a defaulted params struct so call sites do not change.
- Add or update the doc comment on `list` to describe the `license` filter semantics.

### 3. `tests/api/package_license_filter.rs` (CREATE)
Follow the conventions in `tests/api/advisory.rs`: a test DB fixture, `assert_eq!(resp.status(), StatusCode::OK)`,
a `///` doc comment on every test, and given/when/then comments.

Fixture: seed packages `pkg-mit` (MIT), `pkg-apache` (Apache-2.0), and `pkg-gpl` (GPL-3.0-only),
with their licenses stored in `package_license`.

| Test | Asserts |
|---|---|
| `filter_by_single_license_returns_only_matching` | `GET /api/v2/package?license=MIT` → 200. The set of returned package names is exactly `{pkg-mit}`, and every item's `license` field is `"MIT"` |
| `filter_by_multiple_licenses_returns_any_match` | `?license=MIT,Apache-2.0` → 200. The returned names are exactly `{pkg-mit, pkg-apache}` and `pkg-gpl` is absent |
| `no_license_filter_returns_all_packages` | `GET /api/v2/package` → 200. The returned names are `{pkg-mit, pkg-apache, pkg-gpl}` and `total == 3`. This is the regression check |
| `response_shape_unchanged_with_filter` | The body still deserialises as `PaginatedResults<PackageSummary>` (`items`, `total`) |
| `invalid_license_returns_bad_request` | Cases: `?license=` (empty), `?license=MIT,,` (empty element), `?license=M@T!` (illegal characters) → `StatusCode::BAD_REQUEST` |

- The single/multi/no-filter tests share setup, action, and assertion shape but differ in
  data. If the test crate already uses `rstest`, parameterize them as
  `#[rstest] #[case("MIT", &["pkg-mit"]) ...]`. Otherwise keep them as separate functions,
  because sibling patterns win and new frameworks should not be introduced. The invalid-value
  cases are parameterized the same way (or looped over a table) if `rstest` is available.
- Assertions compare sets of package names (value-based), not only `items.len()`.

### API docs / OpenAPI
- If `CONVENTIONS.md` lists an OpenAPI generation command, run it and commit the regenerated
  spec as part of the deliverable.
- `docs/api.md` would ideally document the new `license` parameter, but it is **not** in
  Files to Modify. Flag it in Step 9 for user approval instead of editing it.

## Step 7 — Run tests
`cargo test -p <crate>` for each touched crate. Resolve crate names with
`cargo metadata --no-deps --format-version 1`: expected `trustify-module-fundamental` (or
equivalent) plus the `tests` crate.

## Step 8 — Acceptance criteria mapping
| AC | Satisfied by |
|---|---|
| `?license=MIT` returns only MIT packages | join on `package_license` plus `apply_filter`. Test 1 |
| `?license=MIT,Apache-2.0` returns either | `apply_filter` multi-value `IN` plus `DISTINCT`. Test 2 |
| No param returns all (no regression) | filter applied only when `Some`. Test 3 |
| Response shape unchanged | handler return type untouched. Test 4 |
| Invalid value → 400 | handler validation → `AppError` bad request. Test 5 |

## Step 9 — Self-verification plan
- **Scope containment:** the expected diff is the 3 listed files, plus any regenerated
  OpenAPI spec. Items to flag for user approval if they turn out to be needed:
  - Registering the new test file: if `tests/Cargo.toml` uses explicit `[[test]]` entries or
    a `tests/api/mod.rs` / `main.rs` aggregator exists, it must reference
    `package_license_filter`. That file is out of scope and needs approval.
  - `entity/src/package.rs`: only if the `Relation::PackageLicense` relation does not already
    exist. The task says the entity exists, so this is not expected.
  - `docs/api.md`: documentation for the new parameter.
  - Any other caller of `PackageService::list`.
- **Duplication check:** grep for any new split/`IN` logic. There must be none outside `apply_filter`.
- **Symbol deduplication:** search for an existing SPDX or license validator before declaring one.
- **CI checks:** run every command from `CONVENTIONS.md`. Any failure is a hard stop.
- **Data-flow trace:** `?license=` query string → `Query<PackageListQuery>.license` →
  validation (400 on bad input) → `PackageService::list(license)` → SeaORM join on
  `package_license` plus `apply_filter` → `PaginatedResults<PackageSummary>` JSON. All
  stages connect.
- **Contract and sibling parity:** compared against the advisory severity filter for error
  handling, param naming, and OpenAPI annotation. Caller-site check: every
  `PackageService::list` caller is updated consistently.
- **Sensitive-pattern check** on the staged diff.

## Step 10 — Commit and PR (simulated)
```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(package): add license filter to package list endpoint

Adds optional `license` query parameter (single or comma-separated SPDX ids)
to GET /api/v2/package, reusing common::db::query::apply_filter and the
package_license entity join, following the advisory severity filter pattern.

Implements TC-9203"
```
Fork detection with `git remote get-url upstream`, then
`gh pr create --base main ...`. The PR body contains
`Implements [TC-9203](<webUrl>)`, plus `Closes owner/repo#N` if the GitHub Issue field is set.

## Step 11 — Jira (simulated)
- Set `customfield_10875` to the PR URL as an ADF `inlineCard`.
- Add a comment with the PR link, a summary, and any deviations (for example out-of-scope
  approvals). It ends with the implement-task footnote.
- Transition the issue to **In Review**.
