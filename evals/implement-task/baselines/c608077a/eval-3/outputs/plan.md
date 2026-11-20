# Implementation Plan — TC-9203: Add package license filter to list endpoint

> Eval mode: no repository files modified, no Jira/git/Serena calls made. Steps that would
> touch external systems are described as the actions that *would* be taken.

## Step 0 — Project Configuration validation

`claude-md-mock.md` contains all required sections under `# Project Configuration`:

- Repository Registry: `trustify-backend` → Serena instance `serena_backend`, path `./`
- Jira Configuration: Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git PR field
  `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence: naming convention `mcp__<serena-instance>__<tool>`; limitation noted
  (rust-analyzer can take 30-60s to index on first use)

Result: **valid, proceed**.

## Step 1 — Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` (direct-to-main flow) |
| Target PR | none — default flow (new branch + new PR) |
| Bookend Type | none |
| Dependencies | None |
| GitHub Issue field | would be read from `customfield_10747`; if set, append `Closes <owner>/<repo>#<n>` to the PR body |

All required sections are present (Repository, Target Branch, Description, Files to Modify,
Files to Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements,
Dependencies). An additional **Reuse Candidates** section is present and is used as the
main input to the reuse analysis (see `reuse-analysis.md`).

## Steps 1.5 – 3 — Jira actions (would be performed, not performed in eval)

- 1.5: fetch comments, find the latest `[sdlc-workflow] Description digest:` comment, compute
  digest with `scripts/sha256-digest.py`, compare. If none is found, warn and continue.
- 2: no dependencies, nothing to check.
- 3: `jira.user_info()` → assign TC-9203 to the current user → transition to **In Progress**.

## Step 4 — Understand the code (Serena instance `serena_backend`)

Planned inspection calls:

1. `mcp__serena_backend__get_symbols_overview` on
   - `modules/fundamental/src/package/endpoints/list.rs`
   - `modules/fundamental/src/package/service/mod.rs`
2. `mcp__serena_backend__find_symbol(include_body=true)` on:
   - the advisory list handler and its Query struct in
     `modules/fundamental/src/advisory/endpoints/list.rs` (reference pattern for `severity`)
   - the advisory service `list` in `modules/fundamental/src/advisory/service/advisory.rs`
     (to see how the endpoint passes the filter down to the service)
   - `apply_filter` in `common/src/db/query.rs` (exact signature: input type, column type,
     return type, and whether it already returns an error for empty or invalid tokens)
   - `package_license` `Entity`/`Model`/`Relation` in `entity/src/package_license.rs`, plus
     `entity/src/package.rs` to confirm the `Related<package_license::Entity>` relation exists
   - `PackageSummary` in `modules/fundamental/src/package/model/summary.rs` (read only, to
     confirm the response shape stays the same)
3. `mcp__serena_backend__find_referencing_symbols` on `PackageService::list` to find
   every caller that the signature change will affect.
4. `mcp__serena_backend__search_for_pattern` for `license` in `common/` and
   `modules/fundamental/` to look for an existing SPDX/license validation helper (needed for
   the "invalid license → 400" criterion) before writing any new validation.
5. Sibling conventions: `get_symbols_overview` on `sbom/endpoints/list.rs`,
   `advisory/endpoints/list.rs`, and the test files `tests/api/advisory.rs` and `tests/api/sbom.rs`.
6. Read `CONVENTIONS.md` at the repo root and pull out its CI check commands (fmt/clippy/
   check/test) and any code-generation commands (e.g. OpenAPI spec generation).
7. Documentation to check: `README.md`, `docs/api.md` (REST API reference),
   `docs/architecture.md`.

### Conventions to follow (from the repo structure doc, to be confirmed with Serena)

- **Framework**: Axum handlers, SeaORM queries.
- **Module layout**: `model/ + service/ + endpoints/`. The endpoint parses input and the service builds the query.
- **Error handling**: handlers return `Result<T, AppError>`, with `.context()` for wrapping.
  `AppError` (`common/src/error.rs`) implements `IntoResponse`, so a bad-request variant
  maps to 400.
- **Responses**: list endpoints return `PaginatedResults<T>` (`common/src/model/paginated.rs`).
- **Query helpers**: filtering, pagination, and sorting go through `common/src/db/query.rs`.
- **Tests**: integration tests in `tests/api/` run against a real PostgreSQL test DB and use
  `assert_eq!(resp.status(), StatusCode::OK)`.
- **Skill overrides**: assert on values rather than only lengths, add a `///` doc comment on every test, use
  given/when/then comments in non-trivial tests, and use parameterized tests only if siblings already use them (e.g. `rstest`).

## Step 5 — Branch (would run)

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 — Changes

Scope is limited to exactly these three files:

### 1. MODIFY `modules/fundamental/src/package/endpoints/list.rs`

Mirror the `severity` filter in `advisory/endpoints/list.rs`:

- Add an optional field to the package list Query struct (or create one if the handler
  currently takes only pagination params, using the same shape as the advisory one):
  ```rust
  /// Query parameters accepted by `GET /api/v2/package`.
  #[derive(Debug, Default, Deserialize, IntoParams)]
  pub struct PackageListQuery {
      /// Optional license filter: one SPDX identifier or a comma-separated list
      /// (e.g. `MIT` or `MIT,Apache-2.0`). Exact match.
      #[serde(default)]
      pub license: Option<String>,
      // ...existing pagination / search fields stay unchanged (flatten as in advisory)
  }
  ```
- In the handler, pass `query.license.as_deref()` to `PackageService::list` the same way the
  advisory handler passes `severity`.
- Validation for the 400 criterion: before calling the service, split the value into tokens
  (via `apply_filter`'s parsing if it exposes it, see reuse analysis) and reject the request
  with the repo's bad-request `AppError` variant when:
  - the parameter is present but empty, or contains empty tokens (`license=`, `license=MIT,,`)
  - a token is not a syntactically valid SPDX identifier (characters `[A-Za-z0-9.+-]`, e.g.
    `MIT`, `Apache-2.0`, `GPL-2.0+`, `LicenseRef-foo`).
  If Step 4 finds an existing license/SPDX validator, or `apply_filter` already returns an
  error for malformed input, reuse that instead of writing a new check. No new crate
  dependency (such as `spdx`) will be added without asking the user, because `Cargo.toml` is
  outside the task's file list.
- If utoipa annotations are used (as the `IntoParams` derive on the advisory query would
  suggest), add the `license` param to the `#[utoipa::path(...)]` params so the OpenAPI spec
  documents it, and document the `400` response.
- The response type stays `PaginatedResults<PackageSummary>`. Only the input changes.

### 2. MODIFY `modules/fundamental/src/package/service/mod.rs`

- Extend `PackageService::list` with a `license: Option<&str>` parameter (or a field on an
  existing filter/options struct if the service already takes one, matching how
  `AdvisoryService::list` receives `severity`).
- When `license` is `Some`, add a JOIN to `entity::package_license` using the SeaORM
  relation (`.join(JoinType::InnerJoin, package::Relation::PackageLicense.def())` or
  `.inner_join(package_license::Entity)`), then call
  `common::db::query::apply_filter(select, package_license::Column::License, license)` to add
  the `= value` / `IN (...)` condition.
- Add `.distinct()` (or group by package id) so that a package with several matching licenses
  (e.g. dual-licensed `MIT OR Apache-2.0` stored as two rows) shows up once and pagination
  totals stay correct. The count query must apply the same join and filter.
- When `license` is `None`, the query is the same as it is today (no-regression criterion).
- Update every caller of `PackageService::list` found by `find_referencing_symbols`. Normally
  the endpoint is the only one. Any caller outside the task's file list is flagged in Step 9
  instead of being edited silently.
- Add or adjust the `///` doc comment on `list` to describe the new parameter.

### 3. CREATE `tests/api/package_license_filter.rs`

Integration tests that follow the `tests/api/advisory.rs` setup (test DB fixture, app/client
construction, `assert_eq!(resp.status(), StatusCode::OK)`):

| Test | Given / When / Then |
|---|---|
| `filter_single_license_returns_only_matching` | Seed pkg-a (MIT), pkg-b (Apache-2.0), pkg-c (GPL-3.0-only). `GET /api/v2/package?license=MIT`. Expect 200, and the returned package names equal `["pkg-a"]` (compared by value, not just by count). |
| `filter_multiple_licenses_returns_any_match` | Same seed. `?license=MIT,Apache-2.0`. Expect 200, sorted names equal `["pkg-a","pkg-b"]`, and pkg-c absent. Also seed a dual-licensed pkg-d (MIT + Apache-2.0) and check it appears only once. |
| `no_license_filter_returns_all_packages` | Same seed. `GET /api/v2/package`. Expect 200, all seeded names present, `total` matches, and the response deserializes into `PaginatedResults<PackageSummary>` (checks the shape did not change). |
| `invalid_license_returns_bad_request` | `?license=` (empty), `?license=MIT,,` and `?license=not%20valid!`. Expect `StatusCode::BAD_REQUEST`. These cases run the same algorithm with different inputs, so they would be parameterized with `rstest` if sibling tests already use it. If not, a loop over a small case table inside one test, following project patterns. |

Each test gets a `///` doc comment and `// Given / // When / // Then` sections.

Test-file registration: if `tests/Cargo.toml` declares each test target explicitly
(`[[test]]`), or if the tests use a `tests/api/main.rs`/`mod.rs` aggregator, the new file
needs a registration line. That file is **not** in Files to Modify, so I would flag it for
user approval in Step 9 rather than edit it silently. If the test crate auto-discovers files, no
change is needed.

### Documentation impact

The task has no Documentation Updates section. `docs/api.md` (REST API reference) probably
documents `GET /api/v2/package` query params, so adding `license` there would be the natural
doc update. It is outside Files to Modify/Create, so it gets **flagged for user approval**
and is not changed. If utoipa generates the OpenAPI spec, the annotation change above covers
the generated docs, and any regenerated spec file produced by a CONVENTIONS.md codegen command
would be staged together with the code.

## Step 7 — Tests (would run)

`cargo test -p tests` (or the package name resolved through `cargo metadata`), plus
`cargo test -p trustify-module-fundamental` (or whatever the fundamental crate's real name is,
also resolved through `cargo metadata --no-deps --format-version 1`).

## Step 8 — Acceptance criteria mapping

| Criterion | Covered by |
|---|---|
| `?license=MIT` returns only MIT packages | service join + `apply_filter` single value; test 1 |
| `?license=MIT,Apache-2.0` returns either | `apply_filter` IN clause + distinct; test 2 |
| No param returns all packages | `None` skips join/filter; test 3 |
| Response shape unchanged | handler return type not changed; test 3 deserializes `PaginatedResults<PackageSummary>` |
| Invalid values return 400 | endpoint validation → `AppError` bad request; test 4 |

## Step 9 — Self-verification plan

- **Scope containment**: `git diff --name-only` must list only the 3 files above. Possible
  out-of-scope items to flag: `tests/Cargo.toml`/test aggregator registration, `docs/api.md`,
  any other caller of `PackageService::list`, and a generated OpenAPI file.
- **Untracked files**: `tests/api/package_license_filter.rs` is new and gets staged on purpose.
  Nothing else should be untracked.
- **Dead parameters**: none expected, since only parameters are added.
- **Sensitive patterns**: run the grep over `git diff --cached`.
- **Duplication check**: grep for any new split-on-comma or `is_in(` code in the diff. All of
  that logic should go through `apply_filter`.
- **CI checks**: every command from `CONVENTIONS.md` (e.g. `cargo fmt --check`,
  `cargo clippy -- -D warnings`, `cargo check`). Any non-zero exit is a hard stop.
- **Rust module tests**: `cargo test -p <crate>` for the fundamental crate and the tests crate.
- **Data-flow trace**: query string `license` → Axum `Query<PackageListQuery>` deserialize →
  validate (400 on bad input) → `PackageService::list(license)` → JOIN `package_license` +
  `apply_filter` → SeaORM select with distinct + paginate → `PaginatedResults<PackageSummary>`
  JSON. Every stage connects to the next.
- **Query scope**: the filter runs in SQL (a JOIN with IN), not in memory after loading all
  packages.
- **Contract / sibling parity**: the Query struct derives and the utoipa params match the
  advisory endpoint. Error handling uses `AppError` and `.context()`. No other module writes
  to `package_license` (reads only). The caller-site check makes sure that the `apply_filter`
  call matches the way the advisory service calls it.

## Steps 10–11 — Commit, PR, Jira (would run)

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(package): add license filter to package list endpoint

Adds an optional `license` query parameter (single or comma-separated SPDX
identifiers) to GET /api/v2/package, reusing common::db::query::apply_filter
and joining through the package_license entity.

Implements TC-9203"
```

- No `upstream` remote → `gh pr create --base main`. With a fork →
  `gh pr create -R <upstream> --head <fork-owner>:TC-9203 --base main`.
- PR body: summary, reuse notes, `Implements [TC-9203](<webUrl>)`, and `Closes ...` if the
  GitHub Issue field is set.
- Jira: set `customfield_10875` to the PR URL as an ADF inlineCard, add a comment (PR link,
  summary, deviations, with the footnote from `shared/comment-footnote.md` and skill name
  `implement-task`), then transition to **In Review**.
