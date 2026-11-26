# Implementation Plan — TC-9203: Add package license filter to list endpoint

## Step 0 — Project Configuration validation

The project CLAUDE.md (claude-md-mock.md) contains every required section:

- Repository Registry: `trustify-backend` | Rust backend service | Serena instance `serena_backend` | path `./`
- Jira Configuration: Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git Pull Request field `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence: naming convention `mcp__<serena-instance>__<tool>`. Known limitation: rust-analyzer can take 30-60s to index on first use.

Validation passes, so the plan continues.

## Step 1 — Parsed task (simulated `jira.get_issue(TC-9203)`)

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Description | Add an optional `license` query parameter to `GET /api/v2/package`. It does an exact match on the SPDX identifier and accepts one value or a comma-separated list. |
| Files to Modify | `modules/fundamental/src/package/endpoints/list.rs`, `modules/fundamental/src/package/service/mod.rs` |
| Files to Create | `tests/api/package_license_filter.rs` |
| API Changes | `GET /api/v2/package?license=MIT` and `?license=MIT,Apache-2.0` (MODIFY) |
| Target PR / Bookend Type / Review Context | Not present. This is the default flow. |
| Dependencies | None |
| GitHub Issue (customfield_10747) | Not provided in the mock, so it is skipped silently |

Every required section is present, so there are no gaps to report.

- **Step 1.5 (digest check):** the mock includes no comments. In a real run, a missing digest comment would produce the "No description digest found — skipping integrity check" warning and execution would continue.
- **Step 2 (dependencies):** there are none, so nothing needs checking.
- **Step 3 (would run):** `jira.user_info()`, then `jira.edit_issue(TC-9203, assignee=<me>)`, then transition to In Progress. Not executed, per eval rules.

## Step 4 — Understand the code (planned Serena calls on `serena_backend`)

1. `mcp__serena_backend__get_symbols_overview` on:
   - `modules/fundamental/src/package/endpoints/list.rs`: find the handler fn and any existing `Query`/params struct.
   - `modules/fundamental/src/package/service/mod.rs`: find `PackageService` and its `list` method signature.
2. `mcp__serena_backend__find_symbol` with `include_body=true` on:
   - `common/src/db/query.rs::apply_filter`: confirm its signature, how it splits comma-separated values, how it builds the `IN` condition, and its error type.
   - The advisory list handler and its query struct in `modules/fundamental/src/advisory/endpoints/list.rs`: this is the reference implementation of the `severity` filter.
   - The advisory service list method in `modules/fundamental/src/advisory/service/advisory.rs`: see how the service receives the severity filter and passes it to `apply_filter`.
   - `entity/src/package_license.rs`: column names (e.g. `package_id`, `license`) and the `Relation` / `Related<package::Entity>` definitions.
   - `entity/src/package.rs`: confirm a relation to `package_license` exists for `.join(...)`.
3. `mcp__serena_backend__find_referencing_symbols` on `PackageService::list`. This finds every caller (the package list endpoint, plus possibly search or other modules) so a signature change can be applied to all of them without breaking backward compatibility.
4. `mcp__serena_backend__search_for_pattern` for `license` across `modules/` and `common/`. This checks for any existing license validation or normalization helper.
5. **CONVENTIONS.md:** it exists at the repo root (`./CONVENTIONS.md`). Read it for naming, test conventions, the CI-check command list (likely `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`) and any OpenAPI/codegen command.
6. **Siblings for convention analysis:**
   - Production: `advisory/endpoints/list.rs`, `sbom/endpoints/list.rs`, `advisory/service/advisory.rs`
   - Tests: `tests/api/advisory.rs`, `tests/api/sbom.rs`
7. **Documentation files identified:** `README.md`, `docs/api.md` (REST API reference) and `CONVENTIONS.md`.

### Expected conventions (binding during implementation)

- **Error handling:** handlers return `Result<T, AppError>` and wrap errors with `.context(...)`. `AppError` (in `common/src/error.rs`) implements `IntoResponse`, and a `BadRequest` variant maps to 400.
- **Query params:** a `#[derive(Deserialize, IntoParams)]` struct with `Option<String>` fields, extracted with `Query<...>`, as the advisory `severity` filter does.
- **Responses:** list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- **Module layout:** `model/ + service/ + endpoints/`. Routes are registered in `endpoints/mod.rs`.
- **DB access:** SeaORM entity relations and joins, not raw SQL.
- **Tests:** integration tests against a real PostgreSQL test DB, with `assert_eq!(resp.status(), StatusCode::OK)`.
- **Skill override:** tests must assert on values, not only lengths, and every test fn gets a `///` doc comment.

No conflicts between the task description and these conventions are expected.

## Step 5 — Branch (not executed)

```
git checkout main && git pull && git checkout -b TC-9203
```

## Step 6 — Changes per file

### 1. `modules/fundamental/src/package/endpoints/list.rs` (MODIFY)

- Extend the endpoint's query-parameter struct with one optional field, following the advisory `severity` field exactly:
  ```rust
  /// Optional license filter: a single SPDX identifier or a comma-separated list
  /// (e.g. `MIT` or `MIT,Apache-2.0`). Matches exactly.
  #[serde(default)]
  pub license: Option<String>,
  ```
  - If the package endpoint has no dedicated struct yet and only uses the shared pagination/search query, add a small `PackageListQuery` struct with `#[serde(flatten)]` for the existing params plus `license`. This mirrors the advisory list `Query` struct.
- **Validation (400 on invalid values):**
  - Split the value on `,`, trim each entry, and reject an empty segment (e.g. `license=` or `MIT,,`).
  - Reject any entry containing characters outside the SPDX license-id charset (`[A-Za-z0-9.+-]`, plus the `LicenseRef-` form).
  - On failure, return `AppError::BadRequest(...)`, following the error pattern of the advisory severity validation.
  - If `apply_filter` already validates input and returns an error that maps to 400, rely on it instead of adding a duplicate check (reuse-first).
- Pass `query.license.as_deref()` through to `PackageService::list(...)`.
- Leave the response type `PaginatedResults<PackageSummary>` and the handler's return type unchanged.
- Update the `#[utoipa::path(...)]` params (if present, as in the advisory sibling) so the OpenAPI spec documents `license`.

### 2. `modules/fundamental/src/package/service/mod.rs` (MODIFY)

- Add a `license: Option<&str>` parameter to `PackageService::list`, or a field on an existing filter/options struct if the service already takes one. Follow whichever shape the advisory service uses for `severity`.
- Inside `list`, when `license` is `Some`:
  - Join `package::Entity` to `entity::package_license::Entity` using the existing SeaORM relation (`.join(JoinType::InnerJoin, package::Relation::PackageLicense.def())` or `.inner_join(package_license::Entity)`). No raw SQL.
  - Call `common::db::query::apply_filter(select, package_license::Column::License, license)`. This splits on commas and emits `= value` for a single value or `IN (...)` for several.
  - Add `.distinct()` (or group by package id) so a package with several matching license rows appears only once and pagination totals stay correct.
- When `license` is `None`, the query stays exactly as it is today (no-regression path).
- Update every caller found by `find_referencing_symbols` to pass `None` where filtering is not wanted. If a caller sits outside Files to Modify, flag it in Step 9 instead of silently editing it.
- Add or extend the doc comment on `list` to describe the new parameter.

### 3. `tests/api/package_license_filter.rs` (CREATE)

The structure follows `tests/api/advisory.rs`: the same test-DB bootstrap, app client and fixture helpers. Fixture data is three packages: `pkg-a` is MIT, `pkg-b` is Apache-2.0, `pkg-c` is GPL-3.0-only.

| Test | Asserts |
|---|---|
| `/// Verifies a single license filter returns only packages with that license.` `test_filter_single_license` | `GET /api/v2/package?license=MIT` gives `StatusCode::OK`, and the item names equal `["pkg-a"]`. Every item's `license == "MIT"`. |
| `/// Verifies comma-separated licenses return packages matching any listed license.` `test_filter_multiple_licenses` | `?license=MIT,Apache-2.0` returns the sorted names `["pkg-a","pkg-b"]`, and `pkg-c` is absent. |
| `/// Verifies omitting the license filter returns all packages unchanged.` `test_no_license_filter_returns_all` | No param returns all three packages by name, and `total == 3`. |
| `/// Verifies an invalid license value is rejected with 400 Bad Request.` `test_invalid_license_returns_400` | `?license=` and `?license=MIT,,` (or `?license=%%%`) give `StatusCode::BAD_REQUEST`. |
| (shape check inside the single-filter test) | The response deserializes into `PaginatedResults<PackageSummary>` with `items` and `total`. This covers the acceptance criterion that the response shape is unchanged. |

- Non-trivial tests use `// Given` / `// When` / `// Then` comments.
- Use `rstest` cases for the invalid-value inputs only if the sibling tests already use `rstest`. Otherwise keep the invalid inputs inside one test.
- Assertions check actual package names and licenses, not just counts.
- **Possible registration need:** if `tests/Cargo.toml` declares `[[test]]` targets or a `tests/api/mod.rs`/`main.rs` lists modules, the new file must be registered there. That file is not in Files to Modify, so it would be flagged in Step 9 for user approval rather than edited silently.

### Documentation impact

- `docs/api.md` (REST API reference) probably documents `GET /api/v2/package` parameters and would need a `license` entry.
- It is outside Files to Modify / Files to Create, so it is flagged for user approval in Step 9 instead of being edited automatically.
- The OpenAPI annotation in `list.rs` is updated in scope.

## Step 7 — Tests

- `cargo test -p tests` (or the package name `cargo metadata` resolves for `tests/`) runs the new file.
- `cargo test -p trustify-module-fundamental` (or whatever name `cargo metadata` resolves) runs the crate containing the modified files.

## Step 8 — Acceptance criteria mapping

| Criterion | Covered by |
|---|---|
| `?license=MIT` returns only MIT packages | service join + `apply_filter`; `test_filter_single_license` |
| `?license=MIT,Apache-2.0` returns packages matching either | `apply_filter` IN clause; `test_filter_multiple_licenses` |
| No param returns all packages | `None` path leaves the query unchanged; `test_no_license_filter_returns_all` |
| Response shape unchanged | handler return type untouched; deserialization into `PaginatedResults<PackageSummary>` |
| Invalid values return 400 | endpoint validation, `AppError::BadRequest`; `test_invalid_license_returns_400` |

## Step 9 — Self-verification plan

- **Scope containment:** the expected diff is exactly the three listed files. Flag for approval if they end up touched:
  - `docs/api.md`
  - `tests/Cargo.toml` or a test module index
  - any external `PackageService::list` caller
- **Duplication check:**
  - grep for `split(',')` in package code to confirm no hand-rolled parsing duplicates `apply_filter`.
  - grep `SPDX`/`license` validation to confirm no existing validator is being duplicated.
- **Dead parameters:** none expected, since nothing is removed.
- **CI checks:** run every command listed in CONVENTIONS.md (fmt, clippy, tests, plus OpenAPI regeneration if listed, staging the generated spec). Any non-zero exit is a hard stop.
- **Data-flow trace:** HTTP query string, then `Query<PackageListQuery>.license`, then validation, then `PackageService::list(license)`, then JOIN `package_license` + `apply_filter`, then `PaginatedResults<PackageSummary>` JSON. Every stage connects.
- **Query scope:** the filter is pushed into SQL (JOIN + IN), not applied in memory after loading everything.
- **Contract & sibling parity:**
  - Contract: the handler signature is unchanged.
  - Sibling parity: the param struct and error handling match the advisory `severity`.
  - Cross-module entity: `package_license` is only read, never written.
  - Caller-site: every `PackageService::list` caller is updated.
- **Sensitive patterns:** none expected.

## Step 10 — Commit / PR (not executed)

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(package): add license filter to package list endpoint

Adds optional `license` query parameter (single or comma-separated SPDX ids)
to GET /api/v2/package, reusing common::db::query::apply_filter and joining
through the package_license entity.

Implements TC-9203"
```

- The PR is opened with `--base main`; if an `upstream` remote exists, the fork flags are added.
- The PR body includes `Implements [TC-9203](<webUrl>)`. It has no `Closes` line because no GitHub issue is set.

## Step 11 — Jira (not executed)

- Set `customfield_10875` to the PR URL as an ADF inlineCard.
- Add a comment with the PR link, a summary and any deviations, ending with the skill's footnote.
- Transition the issue to In Review.
