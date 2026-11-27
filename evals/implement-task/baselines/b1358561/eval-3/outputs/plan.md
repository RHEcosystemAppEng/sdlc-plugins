# Implementation Plan — TC-9203: Add package license filter to list endpoint

## Step 0 – Project Configuration validation

CLAUDE.md (claude-md-mock.md) contains all required sections:
- Repository Registry: `trustify-backend` | Serena instance `serena_backend` | Path `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142 (plus PR field `customfield_10875`, GitHub Issue field `customfield_10747`)
- Code Intelligence: `mcp__<serena-instance>__<tool>` naming convention present

Result: PASS, so execution continues.

## Step 1 – Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR | none |
| Bookend Type | none |
| **Mode** | **default** (create branch `TC-9203` from `main`, PR targets `main`) |
| Dependencies | None |
| GitHub Issue (customfield_10747) | would be read from the issue. If it is set, the PR body gets a `Closes <owner>/<repo>#<n>` line. |

All required sections are present (Repository, Target Branch, Description, Files to Modify/Create, API Changes, Implementation Notes, Acceptance Criteria, Test Requirements). The task also includes an optional **Reuse Candidates** section, which drives the reuse plan below.

## Steps 1.5–3 – Jira (simulated, not executed)

- 1.5: fetch comments and find the latest `[sdlc-workflow] Description digest:` comment. Compute the digest with `scripts/sha256-digest.py` and compare. If no digest comment exists, warn and continue.
- 2: no dependencies, so nothing to verify.
- 3: `jira.user_info()`, then assign TC-9203 to the current user, then transition it to **In Progress**.

## Step 4 – Understand the code (planned Serena calls on `serena_backend`)

1. `mcp__serena_backend__get_symbols_overview` on:
   - `modules/fundamental/src/package/endpoints/list.rs` (the current handler and its Query struct, if one exists)
   - `modules/fundamental/src/package/service/mod.rs` (`PackageService::list` signature)
   - `modules/fundamental/src/advisory/endpoints/list.rs` (reference severity filter)
   - `common/src/db/query.rs` (`apply_filter`)
   - `entity/src/package_license.rs` (columns, `Relation` to `package`)
2. `find_symbol(include_body=true)` on `apply_filter`, the advisory list handler and its Query struct, `AdvisoryService::list`, `PackageService::list`, and `package_license::Entity` / `Relation`.
3. `find_referencing_symbols` on `PackageService::list`. Every caller has to keep compiling once a new parameter is added. Likely callers are the package list endpoint and possibly the search module or tests.
4. `search_for_pattern` for:
   - visibility of `apply_filter` (`pub fn apply_filter`) and whether `common` is already a dependency of `modules/fundamental/Cargo.toml` (expected: yes, because the endpoints already use `PaginatedResults` and `AppError` from `common`)
   - naming variants of any existing license-validation helper (`validate_license`, `is_valid_spdx`, `SPDX`, `spdx`) so a validator is not duplicated
   - how the advisory endpoint rejects invalid severity values with 400 (`AppError::BadRequest` or similar)
5. **CONVENTIONS.md**: read `./CONVENTIONS.md` at the repo root. Record its CI-check commands (for example `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test -p <crate>`) for Step 9, plus any OpenAPI or code-generation command, because the API gains a new query param.
6. **Documentation files to note**: `README.md`, `docs/api.md` (REST API reference, which documents `GET /api/v2/package`), `docs/architecture.md`, `CONVENTIONS.md`.

### Conventions from sibling code (binding for Steps 6 and 7)

- **Module layout**: `model/ + service/ + endpoints/`. The endpoint extracts the query, and the service builds the SeaORM query.
- **Error handling**: handlers return `Result<T, AppError>` and wrap errors with `.context()`. Invalid input maps to the 400 variant of `AppError` (`common/src/error.rs`), which implements `IntoResponse`.
- **Query params**: the advisory list uses a `#[derive(Deserialize)]` Query struct with an optional field (`severity: Option<String>`), extracted via `Query<...>` and passed to the service.
- **Filtering**: shared helpers in `common/src/db/query.rs` (`apply_filter`) are used instead of hand-rolled parsing or SQL.
- **Responses**: list endpoints return `PaginatedResults<T>`.
- **Tests**: integration tests live in `tests/api/<area>.rs` against a real PostgreSQL test DB, using `assert_eq!(resp.status(), StatusCode::OK)`. Body assertions are value-based on top of that, because the skill rule overrides any sibling length-only checks.

## Step 5 – Branch (default mode)

```
git checkout main && git pull && git checkout -b TC-9203
```

## Step 6 – Changes per file

### 1. `modules/fundamental/src/package/endpoints/list.rs` (MODIFY)

- Add an optional `license` field to the package list Query struct, mirroring the advisory `severity` field exactly:
  ```rust
  /// Query parameters for `GET /api/v2/package`.
  #[derive(Debug, Deserialize, IntoParams)]
  pub struct PackageListQuery {
      // ...existing pagination/sort fields kept unchanged...
      /// Optional license filter: one SPDX identifier or a comma-separated list (e.g. `MIT,Apache-2.0`).
      #[serde(default)]
      pub license: Option<String>,
  }
  ```
  If the endpoint already has a query struct (for pagination or sorting), add the field to it rather than creating a second extractor.
- Validation, which answers AC "Invalid license values return 400": before calling the service, split the value on `,`, trim each entry, and reject it with the 400 variant of `AppError` if any entry is empty (`license=` or `license=MIT,,`) or is not a syntactically valid SPDX identifier (characters `[A-Za-z0-9.\-+]`). This follows the same pattern the advisory handler uses to reject invalid severity values. If `apply_filter` already returns an error for malformed or empty values, reuse that path and do not duplicate the check. If the Step 4 search finds an existing SPDX validation helper, import it.
- Pass `query.license.as_deref()` into `PackageService::list(...)`.
- Leave the handler's return type (`Result<Json<PaginatedResults<PackageSummary>>, AppError>`) and the response construction untouched, so the response shape does not change.
- If the endpoint uses utoipa / OpenAPI annotations, add the `license` param to `#[utoipa::path(params(...))]` the same way the advisory endpoint documents `severity`.

### 2. `modules/fundamental/src/package/service/mod.rs` (MODIFY)

- Extend `PackageService::list` with a `license: Option<&str>` parameter, following the shape of the advisory service's severity parameter.
- When `license` is `Some`, join `package` to `package_license` through the SeaORM relation defined in `entity/src/package_license.rs`. Use `.join(JoinType::InnerJoin, package_license::Relation::Package.def().rev())` or the `Related` impl, whichever the entity exposes. Then call `common::db::query::apply_filter(select, package_license::Column::License, license)`, which handles the single and comma-separated cases and generates the `IN (...)` clause.
- Add `.distinct()` (or a group by package id) when the join is applied, so a package with several matching licenses appears once and pagination totals stay correct.
- When `license` is `None`, skip the join and the filter so the existing query path is unchanged (no-regression AC).
- Update every caller found by `find_referencing_symbols` to pass `None`. Any caller outside the listed files is flagged in Step 9 check 1 for user approval.

### 3. `tests/api/package_license_filter.rs` (CREATE)

These are integration tests that follow the `tests/api/advisory.rs` setup (test DB fixture, HTTP client, `StatusCode` asserts). The fixtures seed packages with known licenses: pkg-a MIT, pkg-b Apache-2.0, pkg-c GPL-3.0-only.

Every test gets a `///` doc comment and `// Given / When / Then` sections.

- `test_license_filter_single_value`: `?license=MIT` returns 200. The body contains exactly the names `{pkg-a}`, checked by value.
- `test_license_filter_comma_separated`: `?license=MIT,Apache-2.0` returns 200. The set of names equals `{pkg-a, pkg-b}`, and pkg-c is absent.
- `test_no_license_filter_returns_all`: no param returns 200. The names equal `{pkg-a, pkg-b, pkg-c}`, and the body still deserializes as `PaginatedResults<PackageSummary>` (`items` and `total` present, `total == 3`), which covers the response-shape AC.
- `test_invalid_license_returns_bad_request`: parameterized with `rstest` only if the tests crate already uses it. Otherwise these are separate tests or a loop over inputs, because they share the same algorithm. Inputs are `license=`, `license=MIT,,`, and `license=not%20valid!`, each expecting `StatusCode::BAD_REQUEST`.

Registration: `tests/api/*.rs` may need an entry in `tests/Cargo.toml` (`[[test]]`) or a `mod` line, depending on how siblings are wired. That file is not in Files to Modify, so the edit would be raised as a Step 9 scope flag for user approval rather than made silently.

### Documentation impact

There is no Documentation Updates section, and no doc file is listed in the task scope. `docs/api.md` documents `GET /api/v2/package` and would ideally mention the new `license` param. Because it is outside the listed files, it would be raised as a **Step 9 scope flag** (proposed edit shown to the user) and not edited automatically.

## Step 7 – Tests

Run the per-crate tests with crates resolved via `cargo metadata`, never from the nearest `Cargo.toml`:
`cargo test -p trustify-module-fundamental` (or whatever the fundamental crate is actually named) and `cargo test -p <tests crate> --test package_license_filter`. Plus the CI commands from CONVENTIONS.md.

## Step 8 – Acceptance criteria mapping

| AC | Satisfied by |
|---|---|
| `?license=MIT` returns only MIT packages | service join + `apply_filter`, test 1 |
| `?license=MIT,Apache-2.0` returns either | `apply_filter` multi-value IN, test 2 |
| No param returns all packages | filter skipped when `None`, test 3 |
| Response shape unchanged | handler return type untouched, test 3 deserializes `PaginatedResults<PackageSummary>` |
| Invalid values return 400 | endpoint validation leading to `AppError` 400, test 4 |

## Step 9 – Self-verification (expected results)

| # | Check | Expected |
|---|---|---|
| 1 | Scope containment | FLAGGED: possible `tests/Cargo.toml` registration, `docs/api.md`, and any extra `PackageService::list` callers. Presented for approval. |
| 2 | Untracked files | PASS: only `tests/api/package_license_filter.rs` is new and it is intended |
| 3 | Sensitive patterns | PASS |
| 5 | Duplication | PASS: `apply_filter` is reused, the advisory Query pattern is mirrored, and the `package_license` entity is used with no raw SQL |
| 6 | Documentation currency | FLAGGED: `docs/api.md` (public API param added). Handled as in check 1. |
| 10 | Cross-section references | PASS: all listed paths exist in the repo structure |
| 11 | Data-flow trace | PASS: query string, then `PackageListQuery.license`, then validation, then `PackageService::list(license)`, then JOIN `package_license` + `apply_filter`, then `PaginatedResults<PackageSummary>` |
| 13 | Contract & sibling parity | PASS: matches the advisory severity filter (optional field, 400 on invalid input, same helper) |
| 14 | CI checks | run the CONVENTIONS.md commands (fmt, clippy, tests) plus OpenAPI regeneration if documented |
| 15 | Module tests (Rust) | run `cargo test -p` for the fundamental crate and the tests crate |
| 16 | Validated-value override paths | PASS: the license list is validated in one place before reaching the service, with no bypass path |

## Step 10 – Commit and PR

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(package): add license filter to package list endpoint

Add optional comma-separated \`license\` query parameter to GET /api/v2/package,
reusing common::db::query::apply_filter and joining through the
package_license entity, mirroring the advisory severity filter.

Implements TC-9203"
```

Run fork detection (`git remote get-url upstream`), then `gh pr create --base main ...`. The PR body starts with `Implements [TC-9203](<webUrl>)`, adds `Closes <owner>/<repo>#<n>` if the GitHub Issue field is set, and includes a note on reuse choices. If `apply_filter` had to be made `pub`, the PR description records that decision and why.

## Step 11 – Jira

- Set `customfield_10875` to the PR URL as an ADF `inlineCard`.
- Post a comment with the PR link, a summary of the changes, and any deviations (for example approved scope-flag edits), ending with the `implement-task` comment footnote.
- Transition the issue to **In Review**.
