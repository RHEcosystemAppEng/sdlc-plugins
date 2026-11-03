# Implementation Plan — TC-9203: Add package license filter to list endpoint

> Eval mode: no repository files modified, no Jira/git/Serena calls made. This plan
> describes what `/sdlc-workflow:implement-task` would do.

## Step 0 — Project Configuration validation

From `claude-md-mock.md`, the required sections are all present:

- Repository Registry: `trustify-backend` | Rust backend service | `serena_backend` | `./`
- Jira Configuration: Project key `TC`, Cloud ID `2b9e35e3-...`, Feature issue type ID `10142`,
  Git Pull Request field `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence: naming convention `mcp__<serena-instance>__<tool>`; instance `serena_backend`
  (rust-analyzer, may take 30-60 s to index on first use)

Result: validation passes, so the skill continues.

## Step 1 — Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR | none (default flow) |
| Bookend Type | none |
| Dependencies | none, so the Step 2 dependency check passes trivially |
| GitHub Issue | would be read from `customfield_10747`; if empty, skip silently |

All required sections are present (Repository, Target Branch, Description, Files to Modify,
Files to Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements).
The task also has an optional **Reuse Candidates** section, which this plan uses (see
`reuse-analysis.md`).

Step 1.5 (digest check), Step 2 and Step 3 (assign the task, move it to In Progress) are Jira
operations, so they are skipped in this eval. Normally they would run through
`mcp__atlassian__*`.

## Step 4 — Understand the code (planned Serena calls on `serena_backend`)

1. `get_symbols_overview` on:
   - `modules/fundamental/src/package/endpoints/list.rs`: find the handler fn and the
     existing query/params struct (if any) it extracts with `Query<...>`
   - `modules/fundamental/src/package/service/mod.rs`: find `PackageService::list` and its
     signature
2. `find_symbol(include_body=true)` on:
   - `common/src/db/query.rs::apply_filter`: confirm its signature, how it splits
     comma-separated input, how it builds the SQL `IN` / `Condition`, and what error type it
     returns
   - the advisory list handler and its Query struct in
     `modules/fundamental/src/advisory/endpoints/list.rs`: the reference pattern for the
     `severity` filter
   - the severity-filter branch of `AdvisoryService::list` in
     `modules/fundamental/src/advisory/service/advisory.rs`: how the service passes the filter
     to `apply_filter`
   - `entity/src/package_license.rs`: the `Model`, `Column`s (e.g. `PackageId`, `License`) and
     the `Relation` to `package::Entity`
3. `find_referencing_symbols` on `PackageService::list` to find every caller (the endpoint
   handler, and possibly the search module or tests) so a signature change does not break them.
4. `search_for_pattern` for `license` in `common/` and `modules/` to look for an existing
   SPDX validator or a license constant (symbol deduplication).
5. Convention analysis on siblings: `sbom/endpoints/list.rs`, `advisory/endpoints/list.rs`,
   and the tests `tests/api/advisory.rs` and `tests/api/sbom.rs`.
6. Read `CONVENTIONS.md` at the repo root and extract the CI check commands (expected:
   `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`) and any OpenAPI
   generation command.
7. Documentation files to track: `README.md`, `docs/api.md` (REST API reference, which
   documents `GET /api/v2/package` query parameters).

### Conventions to follow (from repo-backend.md, to be confirmed against siblings)

- **Framework**: Axum handlers, SeaORM queries
- **Error handling**: handlers return `Result<T, AppError>`; wrap errors with `.context()`;
  `AppError` implements `IntoResponse`, and a `BadRequest`-style variant maps to 400
- **Query params**: an optional field on a `#[derive(Deserialize)]` Query struct, mirroring
  the advisory `severity` field
- **Response**: `PaginatedResults<PackageSummary>`, which must not change
- **Tests**: integration tests in `tests/api/` against a real PostgreSQL test DB;
  `assert_eq!(resp.status(), StatusCode::OK)`
- **Skill overrides**: value-based assertions (assert on the returned package names and
  licenses, not only on counts), a `///` doc comment on every test, given/when/then
  comments in non-trivial tests

## Step 5 — Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 — Changes

### 1. MODIFY `modules/fundamental/src/package/endpoints/list.rs`

- Add an optional field to the package list Query struct, matching the advisory `severity`
  field:
  ```rust
  /// Query parameters for `GET /api/v2/package`.
  #[derive(Debug, Deserialize, IntoParams)]
  pub struct PackageListQuery {
      // ...existing pagination/sort fields (unchanged)...
      /// Optional license filter: one SPDX identifier or a comma-separated list
      /// (e.g. `MIT` or `MIT,Apache-2.0`). Exact match.
      #[serde(default)]
      pub license: Option<String>,
  }
  ```
  If the endpoint currently uses only a shared pagination struct, add the field the same
  way the advisory endpoint does. Copy whichever structure advisory uses (a dedicated
  struct or a `#[serde(flatten)]` of shared params).
- Validation, so that invalid values return 400: before calling the service, split the
  value on `,`, trim each token, and reject the request with `AppError::BadRequest` (the
  variant the advisory severity path uses) if:
  - a token is empty (e.g. `license=` or `license=MIT,,Apache-2.0`)
  - a token contains characters outside the SPDX license-id charset `[A-Za-z0-9.\-+]`
    (SPDX ids such as `GPL-2.0+` and `LicenseRef-...` are allowed)

  If `apply_filter` already validates its input or returns an error for bad tokens, use
  that and map its error to 400 instead of adding a separate check. If the advisory
  endpoint has a validation helper for severity, follow the same shape.
- Pass `query.license.as_deref()` to `PackageService::list`.
- Update the `#[utoipa::path(...)]` params (if the endpoint uses utoipa) so the OpenAPI spec
  documents `license`. Add a `400` response entry.
- Leave the return type `Result<Json<PaginatedResults<PackageSummary>>, AppError>`
  unchanged.

### 2. MODIFY `modules/fundamental/src/package/service/mod.rs`

- Add a `license: Option<&str>` parameter to `PackageService::list`, or a field on a filter
  struct if the advisory service passes filters that way. Follow `AdvisoryService::list`.
- When `license` is `Some`:
  - join `package::Entity` to `package_license::Entity` through the SeaORM relation
    (`.join(JoinType::InnerJoin, package::Relation::PackageLicense.def())`, or
    `.inner_join(package_license::Entity)`), with no raw SQL
  - call `common::db::query::apply_filter(select, package_license::Column::License, license)`
    so that splitting the comma-separated values and building the `IN (...)` clause is
    handled by the shared helper
  - add `.distinct()` (or group by `package::Column::Id`) so a package with several matching
    licenses (e.g. dual-licensed `MIT OR Apache-2.0` stored as two rows) appears only once,
    which keeps pagination totals correct
- When `license` is `None`, leave the query unchanged (no join), which avoids a regression
  and a performance cost.
- Keep the existing pagination/sort path and the `PaginatedResults<PackageSummary>`
  construction exactly as they are.
- Update every caller found in Step 4 by `find_referencing_symbols` (expected: only the list
  handler). If another caller exists outside the listed files, flag it in the scope check
  rather than editing it silently.
- Add a doc comment describing the new parameter.

### 3. CREATE `tests/api/package_license_filter.rs`

Write the integration tests in the style of `tests/api/advisory.rs`, using the same test
context/DB fixture setup. Seed packages, for example:
`pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (GPL-3.0-only), `pkg-d` (MIT + Apache-2.0).

| Test | Request | Assertions |
|---|---|---|
| `test_filter_single_license` | `?license=MIT` | 200; returned names == {pkg-a, pkg-d}; each item's license includes MIT |
| `test_filter_multiple_licenses` | `?license=MIT,Apache-2.0` | 200; names == {pkg-a, pkg-b, pkg-d}; pkg-d appears exactly once; pkg-c absent |
| `test_no_license_filter_returns_all` | no param | 200; names == {pkg-a, pkg-b, pkg-c, pkg-d}; `total` == 4; response deserializes as `PaginatedResults<PackageSummary>` (shape unchanged) |
| `test_invalid_license_returns_400` | parameterized over `license=`, `license=MIT,,Apache-2.0`, `license=MIT;DROP` | `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` |

- The invalid-value cases share one algorithm with different data. Parameterize them with
  `rstest` `#[case]` only if sibling tests already use `rstest`. Otherwise use a single test
  with a data array, or separate tests, following the project's existing pattern.
- Every test gets a `///` doc comment. Non-trivial tests get `// Given` / `// When` /
  `// Then` sections.
- Assertions check the actual values (package names and licenses), not only `len()`.

Run: `cargo test -p <crate>` for `fundamental` (crate name resolved via
`cargo metadata --no-deps`), plus the `tests` crate.

### Documentation impact

`docs/api.md` documents `GET /api/v2/package`, so it should gain the `license` parameter.
That file is **not** in Files to Modify, so it is flagged in Step 9 for user approval and
not edited unilaterally. If the endpoint is annotated with utoipa, the regenerated OpenAPI
spec (if `CONVENTIONS.md` lists a generation command) is a generated artifact and would be
committed with the change.

## Step 8 — Acceptance Criteria mapping

| Criterion | How it is met |
|---|---|
| `?license=MIT` returns only MIT packages | join + `apply_filter` IN (`MIT`); `test_filter_single_license` |
| `?license=MIT,Apache-2.0` returns packages with either license | `apply_filter` comma-split into an IN list; distinct; `test_filter_multiple_licenses` |
| No param returns all packages | `None` skips the join/filter; `test_no_license_filter_returns_all` |
| Response shape unchanged | handler return type and `PackageSummary` untouched; test deserializes into `PaginatedResults<PackageSummary>` |
| Invalid values return 400 | token validation leading to `AppError::BadRequest`; `test_invalid_license_returns_400` |

## Step 9 — Self-verification (planned)

- **Scope containment**: expected diff = the 2 modified files + 1 new test file. Possible
  out-of-scope files to flag for approval:
  - `tests/Cargo.toml` or a `tests/api/mod.rs`/`main.rs`, if a new test file has to be
    registered (e.g. a `[[test]]` entry or `mod package_license_filter;`)
  - `docs/api.md` (documentation of the new parameter)
  - a generated OpenAPI spec file, if `CONVENTIONS.md` has a generation command
- **Duplication check**: grep for any new split/`IN`-building code. The plan adds none
  beyond the token validation, because `apply_filter` does the parsing. If `apply_filter`
  already validates its input, the local validation is dropped.
- **Symbol deduplication**: search for an existing SPDX/license validator before writing
  one.
- **Dead parameters**: none expected (code is only added).
- **CI checks**: run every command from `CONVENTIONS.md`. Any non-zero exit is a hard stop.
- **Rust module tests**: `cargo test -p` for each crate that contains a modified file.
- **Data-flow trace**: HTTP query `license` → Axum `Query<PackageListQuery>` → validation
  (400 on bad input) → `PackageService::list(license)` → SeaORM select ⋈ `package_license`
  with `apply_filter` IN → `PaginatedResults<PackageSummary>` JSON. Every stage connects.
- **Query scope**: the filter is pushed down into SQL (join + IN), with no in-memory
  filtering of all packages.
- **Contract & sibling parity**: compare against the advisory severity filter for error
  mapping, `.context()` use, OpenAPI annotations and caching middleware config (the route
  builder stays unchanged). Caller-site: every caller of `PackageService::list` is updated
  consistently.
- **Sensitive-pattern check** on the staged diff.

## Step 10 — Commit / PR (not executed)

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(package): add license filter to package list endpoint

Add optional `license` query parameter (single or comma-separated SPDX ids)
to GET /api/v2/package, reusing common::db::query::apply_filter and the
package_license entity join.

Implements TC-9203"
```

Run fork detection (`git remote get-url upstream`), then
`gh pr create --base main ...`, with a PR body containing
`Implements [TC-9203](<webUrl>)`, plus `Closes <owner>/<repo>#<n>` if the GitHub Issue field
is set.

## Step 11 — Jira (not executed)

- Set `customfield_10875` to the PR URL (ADF inlineCard)
- Add a comment with the PR link, a summary and any deviations (e.g. out-of-scope files
  approved), ending with the standard footnote
- Transition the task to In Review
