# Implementation Plan — TC-9207: Remove version-based filter from SBOM list endpoint

> Simulated run of `/sdlc-workflow:implement-task TC-9207`. No repository files were modified and no external tools (Jira, git, Serena) were called. Every step below says what would happen.

## Step 0 – Project Configuration validation

From `claude-md-mock.md`:
- Repository Registry: `trustify-backend`, Serena instance `serena_backend`, path `./`. **Present.**
- Jira Configuration: Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`. **Present.**
- Code Intelligence: `mcp__<serena-instance>__<tool>` naming convention, with `serena_backend` running rust-analyzer. **Present.** (Limitation: indexing can take 30-60s on first use.)

Validation passes, so execution continues.

## Step 1 – Parse task

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | `main` |
| Description | Remove version-based filtering logic from `SbomService::list` |
| Files to Modify | `modules/fundamental/src/sbom/service/sbom.rs`, `modules/fundamental/src/sbom/endpoints/list.rs`, `tests/api/sbom.rs` |
| Files to Create | none |
| API Changes | `GET /api/v2/sbom`: remove the `version` query parameter |
| Target PR / Bookend Type / Review Context | none, so the default flow applies |
| Dependencies | None |

All required sections are present. The GitHub Issue field (`customfield_10747`) would be read from the issue. If it is set, the PR body gets a `Closes <owner>/<repo>#<n>` line.

## Step 1.5 – Description integrity
Fetch the comments and look for `[sdlc-workflow] Description digest:`. If one exists, compute the digest with `scripts/sha256-digest.py` and compare. If none exists, log a warning and continue.

## Step 2 – Dependencies
None, so nothing to check.

## Step 3 – Jira
Assign the issue to the current user and transition it to **In Progress** (simulated).

## Step 4 – Understand the code (via `serena_backend`)

1. `get_symbols_overview` on `modules/fundamental/src/sbom/service/sbom.rs` and `endpoints/list.rs`.
2. `find_symbol("SbomService/list", include_body=true)` to locate the `VersionMatches` filter block and confirm it is the only use of `version_filter`.
3. `find_referencing_symbols("SbomService/list")`. Expected result: the 3 call sites listed in Implementation Notes:
   - `modules/fundamental/src/sbom/endpoints/list.rs` (in scope)
   - `modules/search/src/service/mod.rs` (**NOT in Files to Modify**)
   - `tests/api/sbom.rs` (in scope)
4. `search_for_pattern("VersionMatches")` to see whether the filter type is used anywhere else. If `list` was its only user, it becomes dead code. Its definition probably lives in `common/src/db/query.rs`, which is out of scope, so I would **flag it rather than delete it**.
5. `search_for_pattern("version")` in the endpoint handler to find the query-param struct field or `Query<...>` extraction, plus any `utoipa`/OpenAPI `params(...)` annotation for `version`.
6. Sibling conventions: `advisory/service/advisory.rs::list` and `package/service/mod.rs::list`. They take `(search: Query, paginated: Paginated, tx: &Transactional<'_>)` and return `Result<PaginatedResults<T>, AppError>` with `.context()`. After the change, `SbomService::list` matches this sibling signature exactly.
7. Read `CONVENTIONS.md` at the repo root and pull out the CI check commands (e.g. `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`) and any OpenAPI generation command.
8. Docs to check: `README.md` and `docs/api.md` (REST API reference). These may document the `?version=` parameter.

## Step 5 – Branch
```
git checkout main && git pull && git checkout -b TC-9207
```

## Step 6 – Changes per file

### 1. `modules/fundamental/src/sbom/service/sbom.rs` (in scope)
- Delete the code block that builds and applies the `VersionMatches` filter (e.g. the `if !version_filter.is_empty() { query = query.filter(VersionMatches(version_filter)) }` part). Leave the rest of the query pipeline as it is: search filtering, sorting, pagination, `PaginatedResults` construction and `.context()` error wrapping.
- **Handling `version_filter` after the logic is gone:** removing the filter leaves `version_filter` with zero references in the body, so it is a **dead parameter**. The skill's Step 9 dead-parameter rule says the fix is **removal, not renaming**. So I would **not** rename it to `_version_filter`, **not** add `#[allow(unused)]`, and **not** keep it for "compatibility". The new signature is:
  ```rust
  pub async fn list(
      &self,
      search: Query,
      paginated: Paginated,
      tx: &Transactional<'_>,
  ) -> Result<PaginatedResults<SbomSummary>, AppError>
  ```
- Remove any `use` imports that become unused (e.g. `VersionMatches`) so clippy and the compiler give no warnings.
- Update the method's doc comment if it mentions version filtering.

### 2. `modules/fundamental/src/sbom/endpoints/list.rs` (in scope)
- Remove the `version` field from the query-params struct (or the separate `Query<VersionParam>` extractor). If the struct then holds only the shared `Query`/`Paginated` pieces, use the same extractors the sibling `advisory/endpoints/list.rs` uses.
- Remove the `version` entry from the OpenAPI/`utoipa` `params(...)` annotation, if there is one.
- Change the call to `SbomService::list(search, paginated, &tx)` (no version argument).
- Remove imports that become unused.

### 3. `tests/api/sbom.rs` (in scope)
- **Delete** `test_list_sboms_version_filtered`. The feature is gone, so there is nothing meaningful left for it to assert.
- Update every other direct `SbomService::list(...)` call in this file to drop the version argument (e.g. `list(q, p, "", &tx)` becomes `list(q, p, &tx)`, and `list(q, p, "1.0", &tx)` becomes `list(q, p, &tx)`). If a test passed a non-empty version and asserted a filtered subset, check whether it was really a version-filter test. If so, remove it with the main one. If not, keep it and fix its expectations.
- Optional but recommended: rewrite the removed test as a regression test that sends `GET /api/v2/sbom?version=1.0` and checks that it returns all SBOMs, not a filtered subset (value-based assertions on the returned IDs, `///` doc comment, Given/When/Then comments). This depends on how the endpoint handles unknown params: Axum's `Query` ignores unknown fields unless the struct uses `deny_unknown_fields`. I would mention this in the PR and add it only if it fits the "remove or update" test requirement.

### 4. `modules/search/src/service/mod.rs` (**OUT OF SCOPE**, but required to compile)
- This file calls `SbomService::list(..., "", &tx)` with an empty version filter. Once the parameter is removed, the crate **will not compile** unless the call becomes `SbomService::list(..., &tx)`.
- The file is **not** in Files to Modify, so under the skill's scope rules I would make only this one-line call-site change, report it in the Step 9 scope containment check with the reason ("required call-site update for the removed dead parameter, acceptance criterion: all call sites compile"), and **ask the user to approve it before committing**. The task itself lists the file as a call site, and acceptance criterion 3 says "All call sites compile", so approval is very likely. Still, it gets flagged and is not committed silently.
- The other option, keeping the dead parameter so this file needs no change, is rejected. It contradicts the skill's dead-parameter rule and leaves a misleading API.

### Documentation impact
- `docs/api.md` (and possibly `README.md`) may document `?version=` on `GET /api/v2/sbom`. These are also outside Files to Modify. If they mention the parameter, I would propose the edit and flag it for approval in Step 9.
- If `CONVENTIONS.md` lists an OpenAPI generation command, run it. The regenerated spec (without the `version` param) gets staged as part of the deliverable.

## Step 7 – Tests
- `cargo test -p <crate>` for each affected crate. Crate names come from `cargo metadata --no-deps --format-version 1`: the fundamental crate, the search crate, and the tests crate.
- All other SBOM list tests should pass unchanged. The search tests (`tests/api/search.rs`) must still pass. They exercise the path that previously passed `""`, which was effectively a no-op filter, so behavior is unchanged.

## Step 8 – Acceptance criteria
| Criterion | How it is satisfied |
|---|---|
| `list` no longer filters by version | `VersionMatches` block deleted from `SbomService::list` |
| `version` query param no longer extracted or accepted | Field and OpenAPI param removed from `endpoints/list.rs` |
| All call sites compile without `version_filter` | Parameter removed from the signature; all 3 call sites updated (search module after user approval) |
| Tests not depending on version filtering still pass | `cargo test` on the affected crates |

## Step 9 – Self-verification
- **Scope containment:** expected diff is `sbom.rs`, `list.rs`, `tests/api/sbom.rs` (in scope) plus `modules/search/src/service/mod.rs`, and maybe `docs/api.md` or the generated OpenAPI spec (out of scope). Out-of-scope files are listed with reasons, and approval is required before committing.
- **Dead parameter detection:** see `parameter-cleanup.md`. `version_filter` was detected as dead and removed (not renamed), and all callers were updated. Also check `endpoints/list.rs` for a now-unused params struct or field, and check for an orphaned `VersionMatches` symbol.
- **Sensitive-pattern check:** `git diff --cached | grep -iE ...` on the staged diff.
- **CI checks from CONVENTIONS.md:** run each command. Any non-zero exit is a hard stop. `cargo clippy` would catch any leftover unused variable or import.
- **Rust module-level tests:** `cargo test -p` for the fundamental, search and tests crates.
- **Contract and sibling parity:** the new `list` signature matches the `AdvisoryService::list` and `PackageService::list` siblings. Every caller now uses the same `(search, paginated, &tx)` pattern.
- **Data-flow trace:** HTTP `GET /api/v2/sbom?q=&offset=&limit=` → handler extracts `Query` + `Paginated` → `SbomService::list` → SeaORM query (search filter, sort, paginate) → `PaginatedResults<SbomSummary>` → JSON response. Complete, with no version stage left.

## Step 10 – Commit and PR
```
git commit --trailer="Assisted-by: Claude Code (Claude Opus 5.5)" -m "refactor(sbom): remove version filter from SBOM list endpoint

Remove VersionMatches filtering from SbomService::list and drop the now-dead
version_filter parameter. Remove the version query parameter from
GET /api/v2/sbom and update all call sites (endpoint, search service, tests).

Implements TC-9207"
gh pr create --base main ...
```
The PR body includes `Implements [TC-9207](<webUrl>)`, a note about the API change (the `version` param is removed, and clients now filter on their side), the out-of-scope `search` call-site change, and `Closes ...` if a GitHub issue is linked.

## Step 11 – Jira
Set `customfield_10875` to the PR URL (ADF inlineCard). Add a comment with the PR link, a summary, and the deviation (the out-of-scope search service call-site update), ending with the standard comment footnote. Transition the issue to **In Review**.
