# Implementation Plan — TC-9207: Remove version-based filter from SBOM list endpoint

## Step 0 – Project Configuration validation

`claude-md-mock.md` contains all required sections under `# Project Configuration`:
- Repository Registry: `trustify-backend` → Serena instance `serena_backend`, path `./`
- Jira Configuration: project key `TC`, Cloud ID, Feature issue type ID `10142`
  (plus Git Pull Request field `customfield_10875`, GitHub Issue field `customfield_10747`)
- Code Intelligence: naming convention `mcp__<instance>__<tool>`, `serena_backend` (rust-analyzer)

Validation passes, so the plan continues.

## Step 1 – Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Target PR / Bookend Type | none (default flow) |
| Dependencies | None (Step 2 has nothing to check) |
| Files to Modify | `modules/fundamental/src/sbom/service/sbom.rs`, `modules/fundamental/src/sbom/endpoints/list.rs`, `tests/api/sbom.rs` |
| Files to Create | none |
| API Changes | `GET /api/v2/sbom`: remove the `version` query parameter |

All required sections are present, so there is no need to ask for clarification.
Step 1.5 (digest check), Step 3 (assign + In Progress) and Jira and git operations are
simulated only. Nothing is called in this eval.

## Step 4 – Understanding the code (planned Serena calls)

- `mcp__serena_backend__get_symbols_overview` on `sbom/service/sbom.rs` and `sbom/endpoints/list.rs`.
- `mcp__serena_backend__find_symbol("SbomService/list", include_body=true)` to find the
  `VersionMatches` filter block and every reference to `version_filter`.
- `mcp__serena_backend__find_referencing_symbols("SbomService/list")` to confirm all callers.
  The task lists three. I would run this search anyway in case there are more.
- `mcp__serena_backend__search_for_pattern("VersionMatches")` to see whether the filter type
  is used anywhere else. This decides whether it becomes dead code (see "Out-of-scope findings").
- `search_for_pattern("version")` in `endpoints/list.rs` to find the query-param struct field,
  its `#[serde]`/`utoipa` `IntoParams` annotations, and any OpenAPI docs.
- Read `CONVENTIONS.md` at the repo root to pick up the CI check commands, plus any OpenAPI
  generation command (needed because the API contract changes).
- Sibling conventions: `advisory/service/advisory.rs` (`list`) and `package/service/mod.rs` (`list`)
  use the signature order `(&self, search: Query, paginated: Paginated, tx: &Transactional<'_>)`.
  After the change, `SbomService::list` will match this sibling shape exactly.
- Docs to check: `README.md`, `docs/api.md` (REST API reference) for any mention of
  `GET /api/v2/sbom?version=`.

## Step 5 – Branch

`git checkout main && git pull && git checkout -b TC-9207` (simulated).

## Step 6 – Changes per file

### 1. `modules/fundamental/src/sbom/service/sbom.rs` (in scope)

- Delete the block that applies the `VersionMatches` filter using `version_filter`. Usually
  this is a conditional such as `if !version_filter.is_empty() { query = query.filter(VersionMatches(version_filter)) }`.
- Leave the rest of the query pipeline untouched: the `search` filtering via `common/src/db/query.rs`
  helpers, sorting, `paginated` limit/offset, `tx` connection usage, and the `PaginatedResults` construction.
- **How `version_filter` is handled: it is removed from the signature completely.** After
  the filter logic is gone, `version_filter` has no references left in the body. That makes it
  a dead parameter. Following the skill's dead-parameter rule ("the correct fix is removal,
  not renaming"), I would **not** rename it to `_version_filter`, and I would not use
  `#[allow(unused_variables)]` or `let _ = version_filter;`. The new signature:

  ```rust
  pub async fn list(
      &self,
      search: Query,
      paginated: Paginated,
      tx: &Transactional<'_>,
  ) -> Result<PaginatedResults<SbomSummary>, AppError>
  ```
- If the doc comment on `list` mentions version filtering, update it. Remove any `use` of
  `VersionMatches` (or other imports) that is now unused in this file.

### 2. `modules/fundamental/src/sbom/endpoints/list.rs` (in scope)

- Remove the `version` field from the query-params struct (for example `version: Option<String>`
  with `#[serde(default)]`), or remove the separate `Query<VersionParam>` extractor if the
  handler uses one. Remove the matching `utoipa`/OpenAPI `params(...)` entry too.
- Remove any local variable created from it (for example `let version = params.version.unwrap_or_default();`).
- Change the call from `service.list(search, paginated, &version, &tx)` to
  `service.list(search, paginated, &tx)`.
- Keep the `Result<_, AppError>` return type and the `.context()` wrapping as they are.
- If CONVENTIONS.md defines an OpenAPI generation command, run it and commit the regenerated
  spec, so that `version` disappears from the `GET /api/v2/sbom` parameters.

### 3. `tests/api/sbom.rs` (in scope)

- **Remove** `test_list_sboms_version_filtered`. It only tests the feature that is being
  removed, so there is no behaviour left for it to cover. I would not "update" it, because any
  rewritten version would just duplicate an existing unfiltered list test.
- Update every other test call to `SbomService::list(...)` by dropping the version argument
  (`""`, `"1.0"`, etc.). For HTTP-level tests, remove `?version=` from request URLs used by
  tests other than the deleted one, and keep their assertions unchanged.
- Optional, but it fits Step 7 guidance: add a short regression test showing that
  `GET /api/v2/sbom?version=1.0` now returns the full, unfiltered list. Axum's `Query`
  extractor ignores unknown keys by default unless `deny_unknown_fields` is set. The test would
  use value-based assertions (SBOM ids), a `///` doc comment, and given/when/then comments.
  I would only add it if it fits sibling test patterns. Otherwise, the existing list tests are
  enough per Test Requirements ("verify other SBOM list tests still pass without changes").

### 4. `modules/search/src/service/mod.rs` (call site, not in Files to Modify, needs approval)

- The Implementation Notes list it as call site #2. It currently calls
  `SbomService::list(search, paginated, "", &tx)` with an empty version filter. Once the
  parameter is removed, this file **will not compile** unless it is updated to
  `SbomService::list(search, paginated, &tx)`.
- The file is **not** in Files to Modify. Under the skill's scope rules I would not quietly add
  it. In Step 9's scope containment check I would flag it to the user: it needs a one-line
  argument removal, and without it acceptance criterion "All call sites compile and pass
  without the version_filter argument" cannot be met. I would wait for explicit approval
  before committing it. This conflict comes from the task itself (Notes vs Files to Modify),
  and I would also mention it in the Jira comment as a deviation.
- Rejected alternative: keeping `version_filter` as an ignored `_version_filter` parameter so
  that `search` doesn't need changes. That leaves a dead parameter in a public API, goes against
  the skill's dead-parameter rule, and misleads callers. Removal plus a one-line caller update
  is the correct fix.

## Step 7 – Tests

- `cargo test -p <crate>` for each affected package, with names resolved via
  `cargo metadata --no-deps --format-version 1`. That covers the fundamental crate (e.g.
  `trustify-module-fundamental`), the search crate (e.g. `trustify-module-search`), and the
  `tests` package. Integration tests need PostgreSQL, so I would try the run first.

## Step 8 – Acceptance criteria

| Criterion | How it is satisfied |
|---|---|
| `list` no longer filters by version | `VersionMatches` block deleted, `version_filter` removed from signature |
| `version` query param no longer extracted/accepted | field/extractor and OpenAPI param removed from `endpoints/list.rs` |
| All call sites compile without `version_filter` | endpoint, search service (after approval), and tests updated; `cargo check --workspace` |
| Other tests still pass | only `test_list_sboms_version_filtered` deleted; other tests just lose the argument |

## Step 9 – Self-verification highlights

- **Dead parameter detection**: `version_filter` is the textbook case. Its only reference
  was in the removed lines, so it gets removed and all callers are updated (details in
  `parameter-cleanup.md`). I would also re-check that the endpoint handler doesn't keep an
  unused `version` local or struct field, and that no `#[allow(unused)]` was added.
- **Scope containment**: expected diff = 3 in-scope files + `modules/search/src/service/mod.rs`
  (flagged, waiting for approval) + possibly the regenerated OpenAPI spec (flagged as a code-gen
  artifact). `docs/api.md` would also be flagged if it documents `version`.
- **Out-of-scope findings (flag, don't fix)**: if `VersionMatches` has no other users after
  this change, it becomes dead code in its defining module. I would report this for a
  follow-up instead of deleting it.
- **CI checks**: run every command from CONVENTIONS.md (e.g. `cargo fmt --check`,
  `cargo clippy --all-targets -- -D warnings`). Clippy/rustc would catch any leftover unused
  import or variable. Any non-zero exit is a hard stop.
- **Contract & sibling parity**: `list` signature now matches the `AdvisoryService::list` and
  `PackageService::list` shape. No trait involved, so no contract issue. Caller-site: all
  three callers use the same new argument order.

## Step 10 – Commit / PR (simulated)

```
refactor(sbom): remove version filter from SBOM list endpoint

Remove the VersionMatches filter and the now-unused version_filter
parameter from SbomService::list; drop the `version` query parameter
from GET /api/v2/sbom and update all call sites.

Implements TC-9207
```
with `--trailer="Assisted-by: Claude Code (Claude Opus 5.5)"`. PR to `--base main`, with
`Implements [TC-9207](<webUrl>)` and a note on the search-service out-of-scope change.

## Step 11 – Jira (simulated)

Set `customfield_10875` to the PR URL (ADF inlineCard), add a comment with summary +
deviation (search service call site), with the skill footnote. Transition to In Review.
