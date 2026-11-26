# Implementation Plan — TC-9207: Remove version-based filter from SBOM list endpoint

## Step 0 – Project Configuration validation

The project CLAUDE.md (claude-md-mock.md) has everything the skill needs:
- Repository Registry: `trustify-backend` uses Serena instance `serena_backend` at path `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence: the `mcp__<serena-instance>__<tool>` naming convention, and rust-analyzer as the language server

Validation passes, so execution continues.

## Step 1 – Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR / Bookend Type | none, so the default flow applies |
| Dependencies | None |
| Files to Modify | `modules/fundamental/src/sbom/service/sbom.rs`, `modules/fundamental/src/sbom/endpoints/list.rs`, `tests/api/sbom.rs` |
| Files to Create | none |
| API Changes | `GET /api/v2/sbom`: the `version` query parameter is removed |

Every required section is present, so there is no reason to stop.

## Steps 1.5–3 (simulated, no external calls)

- Step 1.5: would fetch comments and check the `[sdlc-workflow] Description digest:` comment, if one exists.
- Step 2: no dependencies to verify.
- Step 3: would assign TC-9207 to the current user and move it to In Progress.

## Step 4 – Code understanding (planned Serena calls)

- `mcp__serena_backend__get_symbols_overview` on `sbom/service/sbom.rs` and `sbom/endpoints/list.rs`.
- `mcp__serena_backend__find_symbol("SbomService/list", include_body=true)` to find the exact `VersionMatches` filter block.
- `mcp__serena_backend__find_referencing_symbols("SbomService/list")` to confirm the 3 call sites the task lists and find any others.
- `mcp__serena_backend__search_for_pattern("version_filter|VersionMatches|\"version\"")` across the workspace, to find leftover uses: query structs, OpenAPI `utoipa` params, helper imports.
- Read `CONVENTIONS.md` at the repo root and extract the CI check commands (fmt, clippy, check, OpenAPI generation) for Step 9.
- Sibling conventions to check: `advisory/service/advisory.rs::list` and `package/service/mod.rs::list`. These show the expected list signature shape `(&self, search: Query, paginated: Paginated, tx: &Transactional<'_>)` and how the endpoint handlers extract `Query`/`Paginated`.
- Docs to check: `docs/api.md` (REST API reference) and `README.md`, for any mention of the `version` query param on `GET /api/v2/sbom`.

## Step 5 – Branch

```
git checkout main && git pull && git checkout -b TC-9207
```

## Step 6 – Changes per file

### 1. `modules/fundamental/src/sbom/service/sbom.rs`
- Delete the block in `SbomService::list` that applies the `VersionMatches` filter using `version_filter`. Keep the rest of the pipeline exactly as it is: search/filtering via `Query`, sorting, pagination, `PaginatedResults` construction, and `.context()` error wrapping.
- **Handling `version_filter` after the logic is removed:** with the filter gone, `version_filter` has no references left in the method body. That makes it a dead parameter. The fix is to **remove it from the signature completely**. I would **not** rename it to `_version_filter`, and I would **not** keep it with `#[allow(unused)]`. Either of those would hide the warning while leaving a meaningless argument in the public API. New signature:
  ```rust
  pub async fn list(
      &self,
      search: Query,
      paginated: Paginated,
      tx: &Transactional<'_>,
  ) -> Result<PaginatedResults<SbomSummary>, AppError>
  ```
  This also matches the sibling `list` methods in the advisory and package services.
- Remove any imports that become unused, such as `VersionMatches` or a version-filter helper, if nothing else in the file uses them. Clippy/`cargo check` would flag them.
- If `VersionMatches` is defined only for this purpose in `common/src/db/query.rs`, it would become dead code. That file is outside the task scope, so I would **flag it** and leave it alone.

### 2. `modules/fundamental/src/sbom/endpoints/list.rs`
- Remove extraction of the `version` query parameter. Concretely, delete the `version` field from the query-params struct (or the separate `Query<VersionParam>` extractor) and its `utoipa` `IntoParams` / `#[param]` annotation. That removes it from the generated OpenAPI spec.
- Change the call to `SbomService::list(search, paginated, &version, &tx)` so it reads `SbomService::list(search, paginated, &tx)`.
- If the params struct only existed for `version`, delete it and drop it from the handler signature.

### 3. `tests/api/sbom.rs`
- Delete `test_list_sboms_version_filtered`. The feature no longer exists, so there is nothing for it to assert.
- Update every other direct call to `SbomService::list(..., "<version>", ...)` in this file to remove the version argument.
- If any HTTP-level test sends `?version=...`, remove that query string. If the test was only about version filtering, delete the test.
- Other SBOM list tests stay as they are, apart from the call-site argument fix.

### 4. Out-of-scope call site: `modules/search/src/service/mod.rs` (flagged)
- This file calls `SbomService::list(..., "", ...)` with an empty version filter. It must change from `list(search, paginated, "", &tx)` to `list(search, paginated, &tx)`, or the workspace will not compile. Acceptance criterion 3 also requires that "All call sites compile".
- The file is **not** in Files to Modify. Per the skill's scope rules, I would make only this one-argument change and list it in the Step 9 scope-containment report, with the reason. I would ask the user to approve it explicitly before committing. I would make no other changes to this file.

### Documentation impact
- If `docs/api.md` documents the `version` query parameter for `GET /api/v2/sbom`, it would need updating. It is not in Files to Modify, so I would flag it in Step 9 for user approval instead of editing it silently.
- If CONVENTIONS.md lists an OpenAPI generation command, run it and include the regenerated spec, with `version` removed, as a generated artifact.

## Step 7 – Tests
- No new tests are needed, since this removes a feature. Remaining tests keep the existing `assert_eq!(resp.status(), StatusCode::OK)` style.
- Optional, if the user wants it: a small test checking that the list endpoint still returns all SBOMs, with value-based assertions on the returned IDs. It would carry a `///` doc comment and Given/When/Then comments.
- Run `cargo test -p <fundamental crate>`, `cargo test -p <search crate>`, and the `tests` crate, with crate names resolved via `cargo metadata --no-deps --format-version 1`.

## Step 8 – Acceptance criteria
| Criterion | How it is satisfied |
|---|---|
| `list` no longer filters by version | The `VersionMatches` block and the `version_filter` parameter are both removed |
| `version` query param not extracted or accepted | The field/extractor and the OpenAPI param are removed from `endpoints/list.rs` |
| All call sites compile without `version_filter` | The endpoint, the search service (flagged) and the tests are updated; `cargo check --workspace` passes |
| Other tests still pass | The crate-level test runs in Step 9 |

## Step 9 – Self-verification highlights
- **Scope containment:** `git diff --name-only` should show the 3 in-scope files plus `modules/search/src/service/mod.rs`, which needs user approval. `docs/api.md` and `common/src/db/query.rs` are also flagged if they apply.
- **Dead parameter detection:** this check is the main risk for this task. See parameter-cleanup.md for the procedure. Confirm there are no `_version_filter` renames, no unused-variable warnings, and no leftover `version` arguments anywhere.
- **CI checks:** run every command from CONVENTIONS.md (e.g. `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`) and stop hard on any failure.
- **Contract and sibling parity:** `list` now has the same signature as the Advisory and Package `list` methods. `list` is an inherent method, not a trait method, so there is no trait contract to keep in step. Caller-site check: all callers now pass `(search, paginated, &tx)`.
- **Sensitive-pattern check:** run `git diff --cached` through the grep from the skill.

## Steps 10–11 (simulated)
- Commit: `refactor(sbom): remove version filter from SBOM list endpoint`. The body notes the removed parameter and the search-service call-site update. Footer: `Implements TC-9207`, plus the `--trailer="Assisted-by: Claude Code (Claude Opus 5.5)"` flag.
- `gh pr create --base main`, with `Implements [TC-9207](<webUrl>)` in the description. Mark it as a breaking API change, because the `version` query param is gone.
- Jira: set `customfield_10875` to the PR URL as an ADF inlineCard, add a comment (with the footnote) that lists the flagged out-of-scope file, and move the issue to In Review.
