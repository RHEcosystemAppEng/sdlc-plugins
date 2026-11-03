# Implementation Plan: TC-9207 — Remove version-based filter from SBOM list endpoint

## Step 0 – Project Configuration validation

CLAUDE.md (claude-md-mock.md) contains all required sections:
- Repository Registry: `trustify-backend` → Serena instance `serena_backend`, path `./`
- Jira Configuration: Project key `TC`, Cloud ID, Feature issue type ID `10142`,
  Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
- Code Intelligence: `mcp__<serena-instance>__<tool>` convention, `serena_backend` (rust-analyzer)

Validation passes. Proceed.

## Step 1 – Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR | none (default flow — new branch + new PR) |
| Bookend Type | none |
| Dependencies | none |
| GitHub Issue | read from `customfield_10747` if set; otherwise skipped |
| Files to Modify | `modules/fundamental/src/sbom/service/sbom.rs`, `modules/fundamental/src/sbom/endpoints/list.rs`, `tests/api/sbom.rs` |
| Files to Create | none |
| API Changes | `GET /api/v2/sbom` — remove `version` query parameter |

All required sections are present. Description digest check (Step 1.5) would run against the
`[sdlc-workflow] Description digest:` comment (simulated — not called in this eval).

## Steps 2–3 – Dependencies / Jira transition (simulated)

No dependencies. Would assign TC-9207 to the current user and transition to **In Progress**.

## Step 4 – Understand the code (planned Serena calls)

- `mcp__serena_backend__get_symbols_overview` on `sbom/service/sbom.rs` and `sbom/endpoints/list.rs`
- `mcp__serena_backend__find_symbol("SbomService/list", include_body=true)` to see exactly where
  `version_filter` is used (the `VersionMatches` filter application) and confirm it is the
  **only** use of the parameter in the body
- `mcp__serena_backend__find_referencing_symbols("SbomService/list")` to confirm the full caller
  list. The task names 3 call sites; I would verify there are no others (e.g., in
  `modules/fundamental/src/sbom/endpoints/get.rs` or other tests)
- `mcp__serena_backend__search_for_pattern("VersionMatches")` to see whether the filter type is
  used anywhere else (decides whether it becomes dead code — see below)
- `mcp__serena_backend__search_for_pattern("version")` in `endpoints/list.rs` to find the query
  param struct field / `Query<...>` extraction
- Read `CONVENTIONS.md` at the repo root and extract CI check commands (fmt, clippy, check, test)
  and any OpenAPI generation command (relevant because an API query parameter is removed)
- Sibling convention analysis: `advisory/service/advisory.rs::list`, `package/service/mod.rs::list`,
  and `advisory/endpoints/list.rs` — confirm the canonical `list(&self, search: Query,
  paginated: Paginated, tx: &Transactional<'_>)` shape, which is exactly what `SbomService::list`
  becomes after this change
- Documentation files to check: `README.md`, `docs/api.md` (REST API reference — likely documents
  the `version` query param), `CONVENTIONS.md`

## Step 5 – Branch

```
git checkout main
git pull
git checkout -b TC-9207
```

## Step 6 – Changes per file

### 1. `modules/fundamental/src/sbom/service/sbom.rs` (in scope)

- Remove the `VersionMatches` filter logic from the body of `SbomService::list`, leaving the
  rest of the query pipeline (search filter → sorting → pagination → `PaginatedResults`
  construction) intact.
- **Handling `version_filter` after the logic is removed:** once the filter is gone,
  `version_filter: &str` has zero references in the body — it is a dead parameter. Per the skill's
  dead-parameter rule, the fix is **removal from the signature**, not renaming it to
  `_version_filter` and not leaving it unused with `#[allow(unused_variables)]`. New signature:

  ```rust
  pub async fn list(
      &self,
      search: Query,
      paginated: Paginated,
      tx: &Transactional<'_>,
  ) -> Result<PaginatedResults<SbomSummary>, AppError>
  ```

  This also matches the task's acceptance criterion "All call sites compile and pass without
  the version_filter argument", and brings `SbomService::list` into parity with sibling
  `AdvisoryService::list` / `PackageService::list`.
- Remove any `use` imports that become unused (e.g., `VersionMatches` import) so clippy/rustc
  emit no new `unused_imports` warnings.
- If the `VersionMatches` type itself is defined in this file and has no other users, remove it
  too. If it lives in `common/src/db/query.rs` (outside scope), do not touch it — flag it as
  potential dead code in the PR description instead.
- Update the doc comment on `list` if it mentions version filtering.

### 2. `modules/fundamental/src/sbom/endpoints/list.rs` (in scope)

- Remove the `version` field from the query-params struct (e.g., `version: Option<String>`) or
  remove the separate `Query<VersionParam>` extractor — whichever form exists.
- Remove any `#[param(...)]`/utoipa `IntoParams` annotation for `version` so the generated
  OpenAPI spec no longer advertises it.
- Change the call from `service.list(search, paginated, &version, &tx)` (or
  `version.as_deref().unwrap_or("")`) to `service.list(search, paginated, &tx)`.
- Remove now-unused imports.

### 3. `tests/api/sbom.rs` (in scope)

- **Remove** `test_list_sboms_version_filtered` — the feature it tests no longer exists, so
  there is nothing meaningful to update it to. (Converting it into a "version param is
  ignored" test would encode a non-contract behaviour; Axum's `Query` extractor ignores unknown
  params by default, so such a test would add little value.)
- Update every other call to `SbomService::list` in this file to drop the version argument
  (e.g., `service.list(q, p, "", &tx)` → `service.list(q, p, &tx)`).
- Update any HTTP-level test URLs that pass `?version=...` for other purposes.
- Leave other test logic unchanged (Test Requirement: "Verify other SBOM list tests still pass
  without changes" — only the mechanical argument removal is applied).

### 4. `modules/search/src/service/mod.rs` — OUT OF SCOPE, requires approval

The task's Implementation Notes list this as call site #2 (`SearchService` calls `list` with an
empty version filter, e.g., `sbom_service.list(q, p, "", tx)`), but the file is **not** in Files
to Modify. Removing the parameter will break compilation here unless the argument is dropped.

Planned handling (Step 9 scope containment):
- Make the minimal one-line change: remove the `""` argument from the call.
- Flag it explicitly to the user as an out-of-scope modification with justification
  ("required for compilation after removing the dead `version_filter` parameter; the task's
  Implementation Notes identify it as a call site; acceptance criterion 'All call sites compile'
  requires it"), and **do not commit until the user approves**.
- If the user declines, the alternative is to stop and ask how to proceed — keeping the dead
  parameter just to avoid touching this file is not acceptable per the skill's dead-parameter
  rule.

### Documentation impact

- `docs/api.md` likely documents `GET /api/v2/sbom?version=`. It is not in Files to Modify, so
  I would flag it (not silently edit) as an out-of-scope documentation update needed for
  currency, and ask the user to approve.
- If CONVENTIONS.md lists an OpenAPI generation command, run it; the regenerated spec diff
  (removal of `version`) is part of the deliverable and would be included with the commit
  (also noted to the user since it is a generated file outside the explicit list).

## Step 7 – Tests

- Run `cargo test -p <crate>` for each affected crate, resolving crate names via
  `cargo metadata --no-deps --format-version 1` (likely `trustify-module-fundamental`,
  `trustify-module-search`, and the `tests` crate).
- No new tests are required. If any test is touched, ensure it has a `///` doc comment.

## Step 8 – Acceptance criteria verification

| Criterion | How it is satisfied |
|---|---|
| `list` no longer filters by version | `VersionMatches` filter removed from body |
| `version` query param no longer extracted/accepted | field/extractor and OpenAPI param removed from `list.rs` |
| All call sites compile without `version_filter` | parameter removed from signature; all 3 callers updated (search service pending approval) |
| Other tests still pass | `cargo test` on affected crates |

## Step 9 – Self-verification

- **Scope containment:** `git diff --name-only` expected to show the 3 in-scope files plus
  `modules/search/src/service/mod.rs` (flagged, needs approval) and possibly `docs/api.md` /
  generated OpenAPI spec (flagged).
- **Dead parameter detection:** `version_filter` is the dead parameter — removed, not
  underscore-prefixed. Also check the endpoint handler for any now-unused extractor argument.
  Check for any helper function (e.g., `apply_version_filter(query, version)`) that becomes
  unreferenced and remove it.
- **CI checks:** run every command from CONVENTIONS.md (e.g., `cargo fmt --check`,
  `cargo clippy --all-targets -- -D warnings`, `cargo check`); hard stop on any failure.
- **Sensitive-pattern check**, **duplication check**, **contract & sibling parity** (signature
  now matches sibling services; all callers use the same 3-argument form).

## Step 10 – Commit and PR

```
git commit --trailer="Assisted-by: Claude Code" -m "refactor(sbom): remove version filter from SBOM list endpoint

Drop the VersionMatches filter from SbomService::list and remove the now
dead version_filter parameter. Update all call sites (endpoint handler,
search service, integration tests) and remove the version query parameter
from GET /api/v2/sbom.

Implements TC-9207"
```

`gh pr create --base main` (with `-R`/`--head` if an upstream remote exists). PR body includes
`Implements [TC-9207](<webUrl>)`, a note on the out-of-scope search-service change, and
`Closes <owner>/<repo>#<n>` if the GitHub Issue field is set.

## Step 11 – Jira (simulated)

Set `customfield_10875` to the PR URL (ADF inlineCard), add a comment with PR link, summary, and
deviations (search service call-site update; dead parameter removal), with the implement-task
footnote; transition to **In Review**.
