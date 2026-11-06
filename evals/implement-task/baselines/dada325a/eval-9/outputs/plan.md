# Implementation Plan — TC-9207: Remove version-based filter from SBOM list endpoint

## Step 0 – Project Configuration validation

`claude-md-mock.md` contains all required sections under `# Project Configuration`:

- Repository Registry — `trustify-backend`, Serena instance `serena_backend`, path `./`
- Jira Configuration — Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence — `mcp__<serena-instance>__<tool>` naming convention; `serena_backend` (rust-analyzer), with a 30-60s first-index note

Validation passes, so execution continues.

## Step 1 – Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR | none, so the default flow applies (new branch, new PR) |
| Bookend Type | none |
| Dependencies | None |
| GitHub Issue | would be read from `customfield_10747`. Skip if empty |

All required sections are present, so the task does not need clarification before continuing.

**Step 1.5 (digest):** would fetch comments and look for `[sdlc-workflow] Description digest:`. Not run in this eval.
**Steps 2–3:** No dependencies. Would assign to the current user and transition to In Progress. Not run in this eval.

## Step 4 – Understand the code (planned Serena calls)

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/service/sbom.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`
- `mcp__serena_backend__find_symbol("SbomService/list", include_body=true)` to find exactly where `version_filter` is used (the `VersionMatches` filter applied to the query)
- `mcp__serena_backend__find_referencing_symbols("SbomService/list")` to confirm all callers. The task names 3, but I would check for more (e.g. other tests, benches, mocks).
- `mcp__serena_backend__search_for_pattern("VersionMatches")` to see whether `VersionMatches` is used anywhere else. If `list` was its only user, removing the filter leaves it as dead code. I would flag that rather than delete it, because `common/src/db/query.rs` is not in scope.
- `mcp__serena_backend__search_for_pattern("version")` in `list.rs` to find the query-param struct (e.g. a `#[derive(Deserialize, IntoParams)] struct ListParams { version: Option<String>, ... }`) and the utoipa `#[utoipa::path(params(...))]` annotation
- Sibling conventions: `advisory/endpoints/list.rs`, `package/endpoints/list.rs`, `advisory/service/advisory.rs`. These show how list handlers take `Query<SearchOptions>` plus `Query<Paginated>` and call the service without extra filter args. That is the target shape after this change.
- Read `CONVENTIONS.md` at the repo root to collect CI commands (fmt, clippy, check, test, OpenAPI generation)
- Documentation files to check: `README.md`, `docs/api.md` (REST API reference, which may document `?version=`), and an OpenAPI spec if the repo has one

## Step 5 – Branch

```
git checkout main && git pull && git checkout -b TC-9207
```

## Step 6 – Changes per file

### 1. `modules/fundamental/src/sbom/service/sbom.rs` (in scope)

- In `SbomService::list`, delete the block that applies the `VersionMatches` filter using `version_filter`, for example:
  ```rust
  // REMOVE
  if !version_filter.is_empty() {
      query = query.filter(VersionMatches::new(version_filter));
  }
  ```
- Keep everything else in the query pipeline as it is: the `search` filtering, sorting, pagination via `paginated`, the `tx` connection, and the `PaginatedResults<SbomSummary>` mapping.
- **What happens to `version_filter`:** with the filter logic gone, the parameter has no references left in the body, so it is a dead parameter. The skill's dead-parameter rule says to **remove** it, not rename it to `_version_filter` and not leave it unused. The new signature is:
  ```rust
  pub async fn list(
      &self,
      search: Query,
      paginated: Paginated,
      tx: &Transactional<'_>,
  ) -> Result<PaginatedResults<SbomSummary>, AppError>
  ```
  Acceptance criterion 3 ("All call sites compile and pass without the version_filter argument") also requires this.
- Remove the now-unused `use ...::VersionMatches` import so no `unused_imports` warning is introduced and clippy stays clean.
- Update the method's doc comment if it mentions version filtering.

### 2. `modules/fundamental/src/sbom/endpoints/list.rs` (in scope)

- Remove the `version` field from the query-params struct. If the struct only exists to carry `version`, remove the struct and its `Query<...>` extractor.
- Remove the `version` entry from the `#[utoipa::path(params(...))]` OpenAPI annotation.
- Change the call from `service.list(search, paginated, &version, &tx)` (or `version.as_deref().unwrap_or("")`) to `service.list(search, paginated, &tx)`.
- After this change, `GET /api/v2/sbom?version=x` no longer filters. Axum's `Query` extractor ignores unknown fields by default (unless `deny_unknown_fields` is set), so old clients get unfiltered results rather than a 400. I would check for `deny_unknown_fields` and mention the behavior in the PR.

### 3. `tests/api/sbom.rs` (in scope)

- **Remove** `test_list_sboms_version_filtered`. The feature no longer exists, so the test has nothing to assert. Rewriting it to assert "version is ignored" would pin down unspecified behavior that the task does not ask for.
- Update every other `SbomService::list(...)` call in this file to drop the version-filter argument, e.g. `list(q, p, "", &tx)` becomes `list(q, p, &tx)`, and `list(q, p, "1.0", &tx)` becomes `list(q, p, &tx)`.
- Remove any HTTP test that sends `?version=` purely to exercise filtering. Other list tests (pagination, search, empty list) stay unchanged apart from the call-site signature, as Test Requirement 2 asks.

### 4. `modules/search/src/service/mod.rs` (out of scope: needs user approval)

- This is call site #2. It calls `SbomService::list(..., "", ...)` with an empty version filter. Once the parameter is removed, this file **will not compile** unless the `""` argument is removed too.
- The file is **not** listed in Files to Modify. Following the scope rule, I would not quietly add it to the work. In Step 9's scope-containment check I would flag it and ask the user:
  > `modules/search/src/service/mod.rs` is not in Files to Modify, but it is a call site of `SbomService::list` (the task's Implementation Notes list it as call site #2). Removing the dead `version_filter` parameter needs a one-line change here: drop the `""` argument. Approve this change?
- The change is mechanical, a single argument removed: `sbom_service.list(query, paginated, "", &tx)` becomes `sbom_service.list(query, paginated, &tx)`.
- If the user refuses, the only alternative that compiles is to keep a dead `_version_filter` parameter. The skill explicitly says not to do that, and it contradicts acceptance criterion 3, so I would present the tradeoff and wait for the user's decision.

### Documentation impact

- `docs/api.md` probably documents the `version` query parameter on `GET /api/v2/sbom`. It is not in Files to Modify, so I would flag it in Step 9 (documentation currency plus scope containment) and propose deleting that parameter row once the user approves.
- If `CONVENTIONS.md` lists an OpenAPI generation command, I would run it. The regenerated spec (with `version` removed from `/api/v2/sbom`) is a generated artifact and gets committed with the change.

## Step 7 – Tests

- `cargo test -p <crate>` for every crate that owns a modified file. Crate names come from `cargo metadata --no-deps --format-version 1`: the fundamental crate, the tests crate, and the search crate if approved.
- No new tests are needed. The task removes behavior. The doc-comment and given-when-then rules do not apply because no tests are added.

## Step 8 – Acceptance criteria

| AC | How it is met |
|---|---|
| `list` no longer filters by version | `VersionMatches` block removed from `SbomService::list` |
| `version` query param no longer extracted or accepted | field removed from the params struct and the utoipa annotation in `list.rs` |
| All call sites compile without `version_filter` | parameter removed from the signature. All 3 call sites updated (search needs approval) |
| Other tests still pass | crate test runs |

## Step 9 – Self-verification highlights

- **Scope containment:** expected diff is `sbom.rs`, `list.rs`, `tests/api/sbom.rs`, plus `modules/search/src/service/mod.rs` (flagged), possibly `docs/api.md` (flagged), and the OpenAPI spec (generated).
- **Dead parameter detection:** `version_filter` removed from the signature, and its callers updated (see `parameter-cleanup.md`). I would also check `list.rs` for anything that has become unused, such as the `version` binding, the params struct, or imports.
- **Dead code:** if `VersionMatches` has no remaining users, flag it as removable in a follow-up (it lives in `common/`, which is out of scope).
- **Unused imports and warnings:** run `cargo clippy` and `cargo check` and compare against the baseline. No new warnings are allowed.
- **CI checks:** every command from `CONVENTIONS.md`. A non-zero exit is a hard stop.
- **Contract and sibling parity:** `SbomService::list` now has the same shape as `AdvisoryService::list` and `PackageService::list` (search, paginated, tx). Caller-site parity: every caller passes the same three arguments.
- **Sensitive-pattern check** on the staged diff.

## Step 10 – Commit and PR

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "refactor(sbom): remove version-based filter from SBOM list endpoint

Remove VersionMatches filtering from SbomService::list and drop the
now-dead version_filter parameter. Update all call sites (endpoint
handler, search service, integration tests) and remove the version
query parameter from GET /api/v2/sbom.

Implements TC-9207"
```

`gh pr create --base main` (adding `-R <upstream> --head <fork-owner>:TC-9207` if an `upstream` remote exists). The PR body includes `Implements [TC-9207](<webUrl>)`, a `Closes owner/repo#N` line if the GitHub Issue field is set, a note that `?version=` is now ignored, and the reason the search-service call site changed.

## Step 11 – Jira

- Set `customfield_10875` to the PR URL (ADF `inlineCard`).
- Add a comment with the PR link, a summary of changes, and the deviations: the out-of-scope search-service call-site edit, and the docs update if it was done. End the comment with the implement-task footnote.
- Transition to In Review.
