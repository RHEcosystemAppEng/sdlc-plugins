# Implementation Plan — TC-9207: Remove version-based filter from SBOM list endpoint

## Step 0 – Project Configuration validation

The project CLAUDE.md (claude-md-mock.md) contains all required sections:
- Repository Registry: `trustify-backend` → Serena instance `serena_backend`, path `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID 10142 (plus Git Pull Request field `customfield_10875` and GitHub Issue field `customfield_10747`)
- Code Intelligence: `mcp__<serena-instance>__<tool>` naming convention, `serena_backend` (rust-analyzer)

Validation passes, so execution continues.

## Step 1 – Parsed task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Target PR / Bookend Type | none, so this is the default flow |
| Dependencies | None. Step 2 is a no-op |
| API Changes | `GET /api/v2/sbom`: remove the `version` query parameter |

All required sections are present, so there is no reason to stop for clarification.

Simulated Jira actions (not performed): fetch the issue, check the description digest comment (Step 1.5), assign to the current user, and transition to In Progress (Step 3).

## Step 4 – Code understanding (planned Serena calls)

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/service/sbom.rs` and `modules/fundamental/src/sbom/endpoints/list.rs`
- `mcp__serena_backend__find_symbol("SbomService/list", include_body=true)` to locate the `VersionMatches` filter block and confirm it is the only use of `version_filter`
- `mcp__serena_backend__find_referencing_symbols("SbomService/list")` to confirm the 3 call sites in the Implementation Notes and find any others
- `mcp__serena_backend__search_for_pattern("VersionMatches")` to see whether the filter type or helper is used anywhere else. If `list` was its only user, its definition becomes dead code. I would flag that as a follow-up and not delete it, because its definition file is not in scope.
- `mcp__serena_backend__search_for_pattern("version_filter|version=")` across `tests/`, `docs/`, and `modules/` to find leftover references, including OpenAPI annotations such as `utoipa` `params(...)`
- Read `CONVENTIONS.md` at the repo root to extract the CI check commands (fmt, clippy, check, OpenAPI generation)
- Sibling conventions: compare with `advisory/service/advisory.rs::list` and `package/service/mod.rs::list`. Those signatures are `(&self, search: Query, paginated: Paginated, tx: &Transactional<'_>)`, so the new `SbomService::list` signature brings SBOM back in line with its siblings.
- Docs to check: `README.md`, `docs/api.md` (REST API reference). These may document the `version` query parameter.

## Step 5 – Branch

```
git checkout main && git pull && git checkout -b TC-9207
```

## Step 6 – Changes per file

### 1. `modules/fundamental/src/sbom/service/sbom.rs` (in scope)

- Delete the block in `list` that builds and applies the `VersionMatches` filter from `version_filter`. This includes any `if !version_filter.is_empty() { query = query.filter(...) }` guard.
- Keep the rest of the pipeline exactly as it is: search/`Query` filtering, sorting, pagination via the `common/src/db/query.rs` helpers, and the `PaginatedResults<SbomSummary>` construction.
- **Remove the `version_filter: &str` parameter from the signature.** It would be dead after the logic is removed. I would delete it, not rename it to `_version_filter` and not leave it unused. The new signature:
  ```rust
  pub async fn list(
      &self,
      search: Query,
      paginated: Paginated,
      tx: &Transactional<'_>,
  ) -> Result<PaginatedResults<SbomSummary>, AppError>
  ```
- Remove any `use` imports that become unused, such as `VersionMatches`, so clippy/rustc do not warn about unused imports.
- Update the method's doc comment if it mentions version filtering.

### 2. `modules/fundamental/src/sbom/endpoints/list.rs` (in scope)

- Remove the `version` field from the query-param extraction. That means either:
  - dropping the `version: Option<String>` field from the handler's query struct (e.g., `ListParams`) and its `#[serde(default)]` attributes, or
  - removing a separate `Query<VersionParam>` extractor from the handler arguments, along with the struct if nothing else uses it.
- Remove the `version` entry from the OpenAPI/`utoipa::path` `params(...)` annotation, if there is one.
- Change the call from `service.list(search, paginated, &version, &tx)` (or `version.as_deref().unwrap_or("")`) to `service.list(search, paginated, &tx)`.
- Unknown `?version=` query strings: by default Axum's `Query` extractor ignores unknown fields unless the struct uses `#[serde(deny_unknown_fields)]`. Existing clients that still send `version` keep working and the value is ignored. If the struct does deny unknown fields, I would flag this to the user as a behavior change (400 response) before going ahead.

### 3. `tests/api/sbom.rs` (in scope)

- **Remove `test_list_sboms_version_filtered`.** It tests a feature that no longer exists. Rewriting it to assert that "version is ignored" would test an absence and add little value.
- Update every other `SbomService::list(...)` call in this file to drop the version argument (e.g., `list(q, p, "", &tx)` becomes `list(q, p, &tx)`, and `list(q, p, "1.0", &tx)` becomes `list(q, p, &tx)`).
- If any HTTP-level tests send `?version=...` to `/api/v2/sbom` only incidentally, remove the query param from them.
- Leave the other list tests' assertions unchanged. They must pass as they are (Test Requirement 2).

### 4. `modules/search/src/service/mod.rs` (call site, not in Files to Modify, so I would flag it)

- The Implementation Notes list this file as call site #2 (`list` is called with an empty version filter `""`). Removing the parameter means this call must change from `.list(query, paginated, "", tx)` to `.list(query, paginated, tx)`, or the workspace does not compile. That would break Acceptance Criterion 3: "All call sites compile and pass without the version_filter argument".
- The file is **not** in Files to Modify. Following the skill's scope containment rule, I would report it in Step 9 as out of scope, say why it changed (it is a mechanical call-site update forced by removing the parameter, and it is named in the Implementation Notes), and **get explicit user approval before committing**. The change is one line and does not change behavior, because the search service already passed an empty filter (no filtering).

## How `version_filter` is handled after the filtering logic is removed

1. Removing the `VersionMatches` filter leaves `version_filter` with zero references in the body, so it is a dead parameter (Step 9 dead parameter detection).
2. The fix is to **remove it**. Renaming it to `_version_filter` or adding `#[allow(unused_variables)]` would hide the dead code, keep a misleading API, and make callers keep passing meaningless values.
3. `SbomService::list` is an inherent method, not a trait method, so there is no trait contract to keep. It can be removed safely.
4. All callers are updated (see `parameter-cleanup.md`). Only after `find_referencing_symbols` and a grep for `version_filter` / `.list(` both show nothing left is the work done.

## Step 7 – Tests

- `cargo test -p <crate>` for every affected crate. Get the package names from `cargo metadata --no-deps --format-version 1`, likely `trustify-module-fundamental`, `trustify-module-search`, and the `tests` crate.
- Confirm the remaining SBOM list tests pass without assertion changes. Also run the search tests (`tests/api/search.rs`), because the search service call site changed.

## Step 8 – Acceptance criteria

| Criterion | How it is satisfied |
|---|---|
| `list` no longer filters by version | `VersionMatches` block deleted |
| `version` query param no longer extracted or accepted | Field/extractor removed from `endpoints/list.rs` and its OpenAPI params |
| All call sites compile without `version_filter` | Signature changed; 3 call sites updated; `cargo check --workspace` |
| Other tests still pass | `cargo test` on affected crates |

## Step 9 – Self-verification

- **Scope containment**: `git diff --name-only` should show the 3 in-scope files plus `modules/search/src/service/mod.rs`. The search file is flagged for user approval as described above.
- **Dead parameter detection**: `version_filter` removed (not prefixed with an underscore). Also check `endpoints/list.rs` for any local variable or struct field (`version`) left unused after the call change, and remove it.
- **Dead code follow-up**: if `VersionMatches` has no remaining users, report it as a follow-up cleanup instead of editing an out-of-scope file.
- **Documentation currency**: if `docs/api.md` or `README.md` documents `GET /api/v2/sbom?version=`, flag that it needs an update. The file is out of scope, so it needs approval first. If a generated OpenAPI spec (e.g., `openapi.yaml`) comes from the CONVENTIONS.md codegen command, regenerate it and include it in the commit as a generated artifact.
- **CI checks**: run every command from CONVENTIONS.md (e.g., `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`). Any failure is a hard stop.
- **Contract & sibling parity**: the new signature matches the advisory and package `list` signatures. All callers already handled `Result` the same way, so no caller-site anomalies are expected.
- **Sensitive-pattern check**: run `git diff --cached` against the secrets regex.

## Step 10 – Commit and PR

```
git commit --trailer="Assisted-by: Claude Code" -m "refactor(sbom): remove version filter from SBOM list endpoint

Remove VersionMatches filtering from SbomService::list and drop the now-dead
version_filter parameter. The GET /api/v2/sbom handler no longer extracts the
version query parameter. All callers (endpoint, search service, integration
tests) are updated; test_list_sboms_version_filtered is removed.

Implements TC-9207"
```

The PR is created with `gh pr create --base main` (or the fork form if an `upstream` remote exists). The body includes `Implements [TC-9207](<webUrl>)`, a note on the out-of-scope search service call-site change, and `Closes <owner>/<repo>#<n>` if the GitHub Issue field (`customfield_10747`) is set.

## Step 11 – Jira (simulated)

- Set `customfield_10875` to the PR URL using an ADF inlineCard.
- Add a comment with the PR link, a summary, and the deviation (the search service call site was updated outside Files to Modify, with approval), ending with the implement-task footnote.
- Transition to In Review.
