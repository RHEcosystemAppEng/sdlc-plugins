# Implementation Plan — TC-9207: Remove version-based filter from SBOM list endpoint

Skill: `/sdlc-workflow:implement-task` (followed from SKILL.md; external tools simulated, no repository files modified)

## Step 0 — Project Configuration validation

The mock CLAUDE.md (`claude-md-mock.md`) has everything the skill needs:
- Repository Registry: `trustify-backend` uses Serena instance `serena_backend`, path `./`
- Jira Configuration: Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence: naming convention `mcp__<serena-instance>__<tool>`. Known limitation: rust-analyzer can take 30–60s to index.

Result: validation passes, so execution continues.

## Step 1 — Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR / Bookend Type | none, so the default flow applies |
| Dependencies | None (Step 2 is a no-op) |
| Files to Modify | `modules/fundamental/src/sbom/service/sbom.rs`, `modules/fundamental/src/sbom/endpoints/list.rs`, `tests/api/sbom.rs` |
| Files to Create | none |
| API Changes | `GET /api/v2/sbom`: remove the `version` query parameter |

All required sections are present, so no clarification is needed.
GitHub Issue field (`customfield_10747`): I would read it from the issue. If it is set, I would add `Closes <owner>/<repo>#<n>` to the PR body.

## Step 1.5 / 2 / 3 — Simulated Jira steps
- Step 1.5: fetch comments and look for `[sdlc-workflow] Description digest:`. If found, compare it using `scripts/sha256-digest.py`. If not found, log a warning and continue.
- Step 2: no dependencies to check.
- Step 3: `jira.user_info()`, assign TC-9207 to the current user, then move it to **In Progress**.

## Step 4 — Understand the code (using `serena_backend`)

1. `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/service/sbom.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`.
2. `mcp__serena_backend__find_symbol(name_path_pattern="SbomService/list", include_body=true)` to read the `VersionMatches` filter block and confirm it is the only use of `version_filter`.
3. `mcp__serena_backend__find_referencing_symbols` on `SbomService/list` to confirm the 3 call sites listed in the task:
   - `modules/fundamental/src/sbom/endpoints/list.rs` (REST handler)
   - `modules/search/src/service/mod.rs` (SearchService, which passes `""`)
   - `tests/api/sbom.rs` (integration tests)
4. `mcp__serena_backend__search_for_pattern("VersionMatches")` to find out whether the filter type is used anywhere else. If this was its only use, it may become dead code. If it lives outside the files in scope (for example in `common/src/db/query.rs`), I would flag it instead of deleting it.
5. `search_for_pattern("version")` in `list.rs` to find the query-param struct field (for example `version: Option<String>` on the list query struct) and any `utoipa` `IntoParams`/OpenAPI annotation that documents it.
6. Read `CONVENTIONS.md` at the repo root and record its CI check commands (expected: `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo check`, plus any OpenAPI generation command).
7. Sibling conventions: compare `advisory/service/advisory.rs::list` and `package/service/mod.rs::list`. They take `(&self, search: Query, paginated: Paginated, tx: &Transactional<'_>)`. That is exactly the signature `SbomService::list` should have after this change, which supports removing the parameter outright.
8. Docs to check: `README.md`, `docs/api.md` (REST API reference, which may document `?version=`), and the OpenAPI spec.

## Step 5 — Branch
```
git checkout main && git pull && git checkout -b TC-9207
```

## Step 6 — Changes per file

### 1. `modules/fundamental/src/sbom/service/sbom.rs` (in scope)
- Delete the block that builds and applies the `VersionMatches` filter using `version_filter`. Leave the rest of the query pipeline as it is: base select, `search` filtering through `common/src/db/query.rs` helpers, pagination, and conversion into `PaginatedResults<SbomSummary>`.
- **Handling `version_filter`:** once the filter is gone, the parameter has no references. Under the skill's *Dead parameter detection* rule, the fix is removal, not renaming it to `_version_filter` and not adding `#[allow(unused_variables)]`. New signature:
  ```rust
  pub async fn list(
      &self,
      search: Query,
      paginated: Paginated,
      tx: &Transactional<'_>,
  ) -> Result<PaginatedResults<SbomSummary>, AppError>
  ```
- Remove any `use` of `VersionMatches` (or related imports) from this file that is now unused.
- Update the doc comment on `list` if it mentions version filtering.

### 2. `modules/fundamental/src/sbom/endpoints/list.rs` (in scope)
- Remove the `version` field from the query-param struct, or drop the separate `Query<VersionParam>` extractor, depending on how it is written.
- Remove the matching `utoipa` `#[utoipa::path(params(...))]` / `IntoParams` entry so the OpenAPI spec no longer advertises `version`.
- Change the call from `service.list(search, paginated, &version, &tx)` (or `version.as_deref().unwrap_or("")`) to `service.list(search, paginated, &tx)`.
- Keep the `Result<_, AppError>` / `.context()` error handling pattern unchanged.

### 3. `tests/api/sbom.rs` (in scope)
- Delete `test_list_sboms_version_filtered`, since the feature no longer exists. The task allows "remove or update". Deleting is better than rewriting it into a duplicate of the unfiltered list test.
- Update every remaining `SbomService::list(...)` call in this file to drop the version argument. For example, `list(q, p, "", &tx)` becomes `list(q, p, &tx)`.
- Do not change any assertions in the other tests. They must pass unmodified (Test Requirement 2).
- Optional, matching the skill's test quality guidance: add a test that `GET /api/v2/sbom?version=1.0` returns the same items as the unfiltered list (the parameter is ignored), with a `///` doc comment and given/when/then comments. It should assert on returned SBOM IDs, not only the count. Whether an unknown query param is ignored or rejected depends on the extractor (Axum `Query` ignores unknown fields unless `deny_unknown_fields` is set). Check that before asserting.

### 4. `modules/search/src/service/mod.rs` (out of scope, needs user approval)
- This is the 2nd call site. It calls `SbomService::list(..., "", ...)`. Once the parameter is removed it will not compile unless it changes to `list(search, paginated, &tx)`.
- It is **not** listed in Files to Modify, but Implementation Notes name it as a call site and Acceptance Criterion 3 says "All call sites compile and pass without the version_filter argument", so the change is required.
- Following the skill's scope rule, I would not add it silently. I would make the one-line argument removal and then report it in Step 9's scope containment check for explicit user approval before committing. I would also suggest that plan-feature should have listed it.

### Documentation
- If `docs/api.md` or the OpenAPI spec documents `version` on `GET /api/v2/sbom`, it would need updating. Neither file is in Files to Modify, so both would be flagged for approval. Any OpenAPI generation command from CONVENTIONS.md would be run, and its output staged as a generated artifact.

## Step 7 — Tests
- `cargo test -p <crate>` for each affected crate. Crate names come from `cargo metadata --no-deps --format-version 1`, not guessed from directory names. Likely: the fundamental crate, the search crate, and the tests crate.
- `tests/api/search.rs` must still pass, because SearchService behaviour is unchanged (it used to pass an empty filter, which meant no filtering).

## Step 8 — Acceptance Criteria
| AC | How it is met |
|---|---|
| `list` no longer filters by version | `VersionMatches` block removed from `SbomService::list` |
| `version` query param not extracted or accepted | Field/extractor and OpenAPI param removed from `list.rs` |
| All call sites compile without `version_filter` | Parameter removed from the signature. All 3 callers updated (endpoint, search service, tests) |
| Non-version tests still pass | Their assertions are untouched. Only the call arguments change. Full crate test runs |

## Step 9 — Self-verification
- **Scope containment:** `git diff --name-only` should show the 3 in-scope files plus `modules/search/src/service/mod.rs`, which is flagged for user approval. The same applies to `docs/api.md` or the OpenAPI spec if they change.
- **Dead parameter detection:** this step applies directly. `version_filter` is removed, and `grep -rn "version_filter"` across the workspace should return 0 hits. Check that `cargo clippy` reports no unused variable or unused import warnings, and that no `_version_filter` rename exists.
- Also check that `VersionMatches` is not left as dead code.
- **CI checks:** run every command from CONVENTIONS.md. Any non-zero exit is a hard stop.
- **Contract and sibling parity:** the new signature matches `AdvisoryService::list` and `PackageService::list`. `SbomService::list` is an inherent method, not a trait method, so there are no trait implementations to update.
- **Sensitive-pattern check:** run on the staged diff.

## Step 10 — Commit and PR
```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "refactor(sbom): remove version filter from SBOM list endpoint

Remove VersionMatches filtering from SbomService::list and drop the now-unused
version_filter parameter. Update all call sites (list endpoint, search service,
integration tests) and remove the version query parameter from GET /api/v2/sbom.

Implements TC-9207"
```
`gh pr create --base main` (with `-R`/`--head` if an `upstream` remote exists). The body includes `Implements [TC-9207](<webUrl>)`, `Closes ...` if a GitHub issue is linked, and a note about the out-of-scope search service change.

## Step 11 — Jira
Set `customfield_10875` to the PR URL using ADF `inlineCard`. Add a comment covering the PR link, a summary, and the deviation (the search service call site was updated with approval), ending with the implement-task footnote. Move the issue to **In Review**.
