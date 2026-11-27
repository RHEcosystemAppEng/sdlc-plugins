# Implementation Plan — TC-9207: Remove version-based filter from SBOM list endpoint

## Step 0 – Project Configuration validation

CLAUDE.md (claude-md-mock.md) contains all required sections:
- Repository Registry: `trustify-backend` → Serena instance `serena_backend`, path `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142, PR field `customfield_10875`, GitHub Issue field `customfield_10747`
- Code Intelligence: `mcp__<serena-instance>__<tool>` convention; `serena_backend` (rust-analyzer)

Result: PASS. Proceed.

## Step 1 – Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Target PR | none |
| Bookend Type | none |
| Dependencies | none |
| GitHub Issue | (would be read from `customfield_10747`; not present in mock — skipped) |

**Mode: default** (no Target PR, no Bookend Type) → Steps 1–11 run; branch `TC-9207` from `main`; PR → `main`; Jira: set PR field, comment, transition to In Review.

## Steps 1.5 / 2 / 3 (simulated)

- 1.5 Digest check: would fetch comments and look for `[sdlc-workflow] Description digest:`; none available in mock → warn and proceed.
- 2 Dependencies: none.
- 3 Would assign to current user and transition TC-9207 to In Progress (not executed — eval).

## Step 4 – Understand the code (planned Serena calls)

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/service/sbom.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`
- `mcp__serena_backend__find_symbol("SbomService/list", include_body=true)` to read the `VersionMatches` filter block
- `mcp__serena_backend__find_referencing_symbols("SbomService/list")` to confirm the 3 call sites listed in Implementation Notes (and detect any others)
- `mcp__serena_backend__search_for_pattern("VersionMatches")` to see whether the filter type is used anywhere else (to decide whether it becomes dead code)
- `mcp__serena_backend__search_for_pattern("version_filter|\\bversion\\b")` in `modules/`, `tests/`, `docs/` for stragglers (e.g. a `ListQuery { version: Option<String> }` struct, OpenAPI `IntoParams` attributes, docs/api.md entries)
- Read `CONVENTIONS.md` at repo root; extract the CI check commands (e.g. `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`) and any OpenAPI generation command.
- Sibling conventions: compare with `advisory/endpoints/list.rs` and `package/endpoints/list.rs` (handler shape: `Query<Q>` + `Paginated` extractors, `Result<Json<PaginatedResults<T>>, AppError>`, `.context()` wrapping) and `advisory/service/advisory.rs::list` (signature `list(&self, search, paginated, tx)`). Removing `version_filter` actually brings `SbomService::list` into parity with sibling service `list` methods.
- Documentation candidates: `docs/api.md` (REST API reference — likely documents `version` query param on `GET /api/v2/sbom`), `README.md`.

## Step 5 – Branch

```
git checkout main && git pull && git checkout -b TC-9207
```

## Step 6 – Changes per file

### 1. `modules/fundamental/src/sbom/service/sbom.rs` (in scope)

- Remove the block that applies the `VersionMatches` filter to the query (e.g. `.filter(VersionMatches(version_filter))` / `if !version_filter.is_empty() { query = query.filter(...) }`). Keep the rest of the pipeline intact: search filtering (`Query`), sorting, pagination, `PaginatedResults` construction.
- **Handling `version_filter` after the logic is removed:** once the filter block is gone, `version_filter` has zero references in the body — it is a dead parameter. Per Step 9 check 4 (Dead parameters) the correct fix is **removal from the signature**, not renaming to `_version_filter` and not leaving it with `#[allow(unused)]`. The Acceptance Criterion "All call sites compile and pass without the version_filter argument" also explicitly requires removal. New signature:

  ```rust
  pub async fn list(
      &self,
      search: Query,
      paginated: Paginated,
      tx: &Transactional<'_>,
  ) -> Result<PaginatedResults<SbomSummary>, AppError>
  ```
- Remove now-unused imports (`VersionMatches`, etc.) so clippy `unused_imports` does not fail. If `VersionMatches` is defined in this module/`common/src/db/query.rs` and has no other users, flag it (it would be dead code but its file is out of scope — see scope flags).
- Update the doc comment on `list` if it mentions version filtering.

### 2. `modules/fundamental/src/sbom/endpoints/list.rs` (in scope)

- Remove extraction of the `version` query parameter (e.g. the `version: Option<String>` field on the handler's query struct, or a separate `Query<VersionParam>` extractor, plus `.as_deref().unwrap_or("")`).
- If the query struct exists solely to carry `version`, remove the struct and its extractor entirely; if it is shared with other fields, remove just the field.
- Remove `version` from the `utoipa` `#[utoipa::path(params(...))]` / `IntoParams` annotations so the OpenAPI spec no longer advertises it.
- Change the call to `service.list(search, paginated, &tx)` (drop the argument).

### 3. `modules/search/src/service/mod.rs` (NOT in Files to Modify — call site)

- Change `sbom_service.list(query, paginated, "", &tx)` → `sbom_service.list(query, paginated, &tx)`.
- This edit is required for the crate to compile (AC: "All call sites compile"), and the Implementation Notes name it as a call site, but the file is not listed under Files to Modify. Per Step 6 / Step 9 check 1 it is recorded as an **out-of-scope file requiring explicit user approval before commit**.

### 4. `tests/api/sbom.rs` (in scope)

- **Remove** `test_list_sboms_version_filtered` — the feature no longer exists, so there is no behavior to assert. (Optionally replace with a test that `GET /api/v2/sbom?version=x` returns the unfiltered list — but Axum's `Query` extractor ignores unknown params by default, so this would only test framework behavior; I'd prefer removal unless the reviewer wants a regression guard. If kept, it must have a `///` doc comment, given/when/then sections, and value-based assertions on returned SBOM IDs, not just length.)
- Update every other direct call to `SbomService::list` in this file to drop the version argument (e.g. `service.list(q, p, "", &tx)` → `service.list(q, p, &tx)`; calls that passed non-empty versions belonged to the removed test or must be rewritten to assert the unfiltered result).
- Do not otherwise change other SBOM list tests (Test Requirement: "Verify other SBOM list tests still pass without changes").

### Documentation impact

- No Documentation Updates section in the task. `docs/api.md` likely documents the `version` query param on `GET /api/v2/sbom`; it is not in Files to Modify → Step 9 scope flag (propose the one-line removal, ask user approval).
- Regenerate OpenAPI spec if CONVENTIONS.md defines a generation command (artifact from a documented codegen command may be staged without approval).

## Step 7 – Tests

- Run the CI checks from CONVENTIONS.md; for Rust, resolve modified crates via `cargo metadata` (fundamental, search, tests) and run `cargo test -p <crate>` for each, plus `cargo clippy --all-targets -- -D warnings` to confirm no unused-variable/import warnings remain.

## Step 8 – Acceptance Criteria

| AC | How satisfied |
|---|---|
| `list` no longer filters by version | `VersionMatches` filter block removed from `SbomService::list` |
| `version` query param not extracted/accepted | Field/extractor and OpenAPI param removed from `endpoints/list.rs` |
| All call sites compile without `version_filter` | Parameter removed from signature; 3 call sites updated (endpoint, search service, tests) |
| Other tests still pass | Only `test_list_sboms_version_filtered` removed; other tests just drop the argument |

## Step 9 – Self-verification (expected results)

| # | Check | Result |
|---|---|---|
| 1 | Scope containment | FLAGGED `modules/search/src/service/mod.rs` (required call-site update — needs user approval); FLAGGED `docs/api.md` if it documents `version` (proposed, needs approval); FLAGGED `VersionMatches` definition if now unused (report, do not edit without approval) |
| 3 | Sensitive patterns | PASS (no secrets in diff) |
| 4 | Dead parameters | Fires (removed lines referenced `version_filter`). Resolved: `version_filter` removed from signature, all callers updated → PASS |
| 6 | Documentation currency | Fires (public API changed) — see docs/api.md flag |
| 10 | Cross-section references | PASS — all listed paths exist in repo structure |
| 13 | Contract & sibling parity | PASS — new signature matches sibling `AdvisoryService::list` / `PackageService::list` |
| 14 | CI checks | Run CONVENTIONS.md commands (fmt, clippy, test) |
| 15 | Module tests (Rust) | `cargo test` for fundamental, search, and tests crates |

## Step 10 – Commit & PR

```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "refactor(sbom): remove version filter from SBOM list endpoint

Remove VersionMatches filtering from SbomService::list and drop the now-dead
version_filter parameter. The GET /api/v2/sbom endpoint no longer accepts the
version query parameter; version filtering is performed client-side. Update
all call sites (endpoint handler, search service, integration tests) and
remove test_list_sboms_version_filtered.

Implements TC-9207"
```

`gh pr create --base main` with body containing `Implements [TC-9207](<webUrl>)` (+ `Closes owner/repo#N` if the GitHub Issue field is set), noting the out-of-scope search-service edit.

## Step 11 – Jira

Set `customfield_10875` to the PR URL (ADF inlineCard), add a comment with the PR link, summary, and deviation (search service call site edited outside listed files; dead parameter removed from signature), ending with the implement-task footnote; transition to In Review.
