# Implementation Plan — TC-9203: Add package license filter to list endpoint

Skill: `/sdlc-workflow:implement-task` (eval simulation — no repo, Jira, git, or Serena calls were actually made).

## Step 0 – Project Configuration validation

`claude-md-mock.md` contains all required sections under `# Project Configuration`:

- Repository Registry: `trustify-backend` | Rust backend service | `serena_backend` | `./`
- Jira Configuration: Project key `TC`, Cloud ID `2b9e35e3-...`, Feature issue type ID `10142`, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence: naming convention `mcp__<serena-instance>__<tool>`, instance `serena_backend` (rust-analyzer; may need 30-60s to index on first use)

Result: configuration is valid, so execution continues.

## Step 1 – Parsed task (TC-9203)

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR | none, so default flow (new branch + new PR) |
| Bookend Type | none |
| Dependencies | None |
| Files to Modify | `modules/fundamental/src/package/endpoints/list.rs`, `modules/fundamental/src/package/service/mod.rs` |
| Files to Create | `tests/api/package_license_filter.rs` |
| API Changes | `GET /api/v2/package?license=MIT` and `?license=MIT,Apache-2.0` (MODIFY, optional param) |
| Reuse Candidates | `common/src/db/query.rs::apply_filter`, advisory `endpoints/list.rs` severity filter, `entity/src/package_license.rs` |
| GitHub Issue | would read `customfield_10747`; skip silently if empty |

All required sections are present, so there is no need to ask for clarification.

## Steps 1.5–3 – Jira steps (simulated)

- 1.5: would fetch comments, find the `[sdlc-workflow] Description digest:` comment, and compare it with `python3 scripts/sha256-digest.py`. If no digest comment exists, warn and proceed.
- 2: Dependencies = None, so there is nothing to verify.
- 3: would call `jira.user_info()`, assign TC-9203 to the current user, and transition it to In Progress.

## Step 4 – Understand the code (planned Serena calls on `serena_backend`)

1. `mcp__serena_backend__get_symbols_overview` on:
   - `modules/fundamental/src/package/endpoints/list.rs` (current Query struct and handler)
   - `modules/fundamental/src/package/service/mod.rs` (`PackageService::list` signature)
   - `modules/fundamental/src/advisory/endpoints/list.rs` (reference pattern)
   - `modules/fundamental/src/advisory/service/advisory.rs` (how the severity filter reaches the service)
2. `mcp__serena_backend__find_symbol` with `include_body=true`:
   - `apply_filter` in `common/src/db/query.rs`: confirm its signature, how it splits comma-separated values, and what it returns for empty or invalid input (this matters for the 400 criterion)
   - The advisory list handler and its Query struct (the `severity: Option<String>` field and how it is passed down)
   - `PackageService::list` body
   - `package_license` entity `Model` / `Relation` (columns such as `package_id` and `license`, plus the `Related<package::Entity>` impl)
3. `mcp__serena_backend__find_referencing_symbols` on `PackageService::list`: find every caller. The signature will gain a parameter, so each caller must be updated (or use a filter struct with `Default`).
4. `search_for_pattern` for `license` across `modules/fundamental` and `common` to make sure no license filter or SPDX validator already exists (symbol deduplication).
5. Sibling convention analysis: the `sbom/endpoints/list.rs` and `advisory/endpoints/list.rs` endpoints, plus the `tests/api/advisory.rs` and `tests/api/sbom.rs` tests.
6. Read `CONVENTIONS.md` at the repo root and extract the CI check commands (likely `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo check`) and any OpenAPI or codegen command.
7. Docs to check for Step 9 currency: `README.md`, `docs/api.md` (REST API reference), `CONVENTIONS.md`.

### Expected conventions (binding reference for Step 6/7)

- Error handling: handlers return `Result<T, AppError>`, wrapping errors with `.context()`. Bad input maps to an `AppError` variant that `IntoResponse` renders as 400.
- Endpoint shape: Axum `Query<...>` extractor with an `Option<String>` filter field, as in advisory `severity`.
- Responses: `PaginatedResults<PackageSummary>`, unchanged.
- DB: SeaORM entities and relations, never raw SQL. Filtering goes through `common/src/db/query.rs`.
- Tests: integration tests in `tests/api/` against real PostgreSQL. Status asserted with `assert_eq!(resp.status(), StatusCode::OK)`.

## Step 5 – Branch

```
git checkout main
git pull
git checkout -b TC-9203
```

## Step 6 – Changes per file

### 1. MODIFY `modules/fundamental/src/package/endpoints/list.rs`

- Add an optional field to the package list Query struct, copying the advisory `severity` field:
  ```rust
  /// Optional license filter: one SPDX identifier or a comma-separated list (e.g. `MIT,Apache-2.0`).
  #[serde(default)]
  pub license: Option<String>,
  ```
  If the advisory Query struct derives `utoipa::IntoParams`, add the matching `#[param(...)]` doc so the OpenAPI spec lists the new parameter.
- Validation for the "invalid license value returns 400" criterion: before calling the service, check each comma-separated token. A token is rejected if it is empty (for example `MIT,,` or `license=`) or contains characters outside the SPDX identifier set (`[A-Za-z0-9.+-]`). Rejected tokens return the same `AppError` bad-request variant the advisory endpoint uses for invalid `severity`. If `apply_filter` already performs this validation and returns an error, rely on that instead and propagate it with `?` / `.context()`, so no new validator is written.
- Pass `query.license.as_deref()` (or the parsed filter) to `PackageService::list`.
- The handler return type `Result<Json<PaginatedResults<PackageSummary>>, AppError>` stays as it is. Only the input changes.

### 2. MODIFY `modules/fundamental/src/package/service/mod.rs`

- Extend `PackageService::list` with a `license: Option<&str>` parameter, matching however the advisory service receives `severity`.
- When `license` is `Some`:
  - Join through the existing SeaORM entity: `package::Entity::find().join(JoinType::InnerJoin, package::Relation::PackageLicense.def())`, or the reverse `package_license::Relation::Package` if that is the relation that is defined.
  - Apply the filter with `common::db::query::apply_filter(select, package_license::Column::License, license)`. It splits on commas and emits `= value` for a single value and `IN (...)` for several.
  - Add `.distinct()` (or group by the package id) so a package with several matching licenses is not returned twice. Pagination counts stay correct.
- When `license` is `None`, the query is the same as today (no join), so nothing regresses.
- Keep pagination, sorting, and mapping to `PackageSummary` unchanged.
- Update every caller found via `find_referencing_symbols`. Callers inside the two listed files are in scope. Any caller elsewhere is flagged in Step 9 for approval and not silently edited.

### 3. CREATE `tests/api/package_license_filter.rs`

Integration tests following the `tests/api/advisory.rs` conventions (real test DB, same client and fixture helpers). Each test gets a `///` doc comment and Given/When/Then sections. Fixture: seed packages `pkg-mit` (MIT), `pkg-apache` (Apache-2.0), and `pkg-gpl` (GPL-3.0-only) through `package_license` rows.

- `/// Verifies a single license filter returns only packages with that license.`
  `GET /api/v2/package?license=MIT`: assert `StatusCode::OK`, and assert that the returned package names equal exactly `["pkg-mit"]`. Each item's `license` must equal `"MIT"`. These are value-based checks, not just a count.
- `/// Verifies a comma-separated license filter returns packages matching any listed license.`
  `?license=MIT,Apache-2.0`: assert OK, and assert the sorted names equal `["pkg-apache", "pkg-mit"]`, with `pkg-gpl` absent.
- `/// Verifies omitting the license filter returns all packages unchanged.`
  No parameter: assert OK, all three names present, and the response deserializes as `PaginatedResults<PackageSummary>` with `total == 3` (the shape is unchanged).
- `/// Verifies invalid license values are rejected with 400 Bad Request.`
  Invalid inputs: `license=` (empty), `license=MIT,,` and `license=MIT;DROP`. Use a parameterized/table-driven loop or `rstest` only if the siblings use one. Otherwise write a single test that iterates a data array. Each case asserts `StatusCode::BAD_REQUEST`.

Run `cargo test -p <tests crate>` (resolved through `cargo metadata`) and also `cargo test -p <fundamental crate>`.

### Documentation impact

There is no Documentation Updates section. `docs/api.md` documents `GET /api/v2/package` and would need the new `license` parameter, but it is outside Files to Modify and Files to Create. It is flagged in Step 9 for user approval and not edited unilaterally. An OpenAPI spec regenerated by a CONVENTIONS.md codegen command would be staged as part of that command's output.

## Step 7/8 – Acceptance Criteria mapping

| Criterion | How it is satisfied | Test |
|---|---|---|
| `?license=MIT` returns only MIT | `apply_filter` with a single value through the `package_license` join | single-filter test |
| `?license=MIT,Apache-2.0` returns either | `apply_filter` comma-split into `IN` | multi-filter test |
| No parameter returns all packages | `None` leaves the query unchanged (no join) | no-filter test |
| Response shape unchanged | Handler return type untouched, only Query gains an optional field | no-filter test deserializes `PaginatedResults<PackageSummary>` |
| Invalid values return 400 | Token validation or `apply_filter` error maps to the `AppError` bad-request variant | invalid-value test |

## Step 9 – Self-verification plan

- Scope containment: expected diff is exactly the three listed files. Possible out-of-scope items to flag for approval:
  - Test crate registration (`tests/Cargo.toml` `[[test]]` entry or a `tests/api/mod.rs`) if the test harness does not auto-discover `tests/api/*.rs`.
  - `docs/api.md` parameter documentation.
  - Any `PackageService::list` callers outside the two modified files.
  - Making `apply_filter` or a `package_license` relation `pub` if they are not already exported. `common` and `entity` are already dependencies of `fundamental`, so per the reuse-over-duplication rule I would export rather than duplicate, but that edit is out of scope and needs approval.
- Duplication check: grep for any new splitting or IN-clause logic. None should exist beyond calls to `apply_filter`.
- Dead parameters: none expected, since only a parameter is added.
- Sensitive patterns: run the `git diff --cached | grep -iE ...` check.
- CI: run every CONVENTIONS.md CI command. Any non-zero exit is a hard stop.
- Rust module tests: `cargo test -p` for the fundamental crate and the tests crate.
- Data-flow trace: HTTP query string, then the `Query<PackageListQuery>.license`, then validation, then `PackageService::list(license)`, then `apply_filter` on the `package_license` join, then the SeaORM query, then `PaginatedResults<PackageSummary>` JSON. All stages connect.
- Query scope: the filter is applied at the DB level (a JOIN plus WHERE IN), not in memory.
- Contract and sibling parity: Query struct derives (`Deserialize`, `IntoParams`) match advisory. Errors use the same `AppError` variant as advisory severity validation. The `package_license` join follows the same pattern as other entity joins. `PackageService::list` callers are all updated.

## Step 10 – Commit and PR (simulated)

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "feat(package): add license filter to package list endpoint

Add optional comma-separated license query parameter to GET /api/v2/package,
reusing common::db::query::apply_filter and the package_license entity join.

Implements TC-9203"
```

- Fork detection with `git remote get-url upstream`, then `gh pr create --base main` (with `-R`/`--head` when working from a fork).
- PR body includes `Implements [TC-9203](<webUrl>)`, plus `Closes <owner>/<repo>#<n>` if the GitHub Issue field is set.

## Step 11 – Jira (simulated)

- Set `customfield_10875` to the PR URL as an ADF inlineCard.
- Add a comment with the PR link, a summary, any deviations (for example out-of-scope approvals), and the implement-task footnote.
- Transition to In Review.
