# Parameter Cleanup — TC-9207

How I would handle the `version_filter` parameter after removing the `VersionMatches` logic. This applies the implement-task skill's **Step 9 → Dead parameter detection** rule.

## 1. Find the dead parameter

- The diff for `SbomService::list` (`modules/fundamental/src/sbom/service/sbom.rs`) removes the lines that build and apply the `VersionMatches` filter. Those lines were the **only** references to `version_filter`.
- To confirm, run `mcp__serena_backend__find_symbol("SbomService/list", include_body=true)` after the edit and check that the body has zero references to `version_filter`. `cargo check` / `cargo clippy` would report an `unused variable: version_filter` warning.
- So `version_filter` is a dead parameter.

## 2. Decision: remove it, do not rename or suppress

| Option | Verdict |
|---|---|
| Rename to `_version_filter` | Rejected. The skill says "the correct fix is removal, not renaming". It hides the warning but keeps a meaningless argument in the API. |
| `#[allow(unused_variables)]` | Rejected for the same reason. |
| Keep it "for compatibility" | Rejected. `SbomService::list` is an inherent `impl` method, not a trait method, so no other implementation relies on the signature. Every caller is in this workspace. |
| **Remove it from the signature and update every caller** | **Chosen** |

This also matches sibling services. `AdvisoryService::list` and `PackageService::list` both use `(&self, search: Query, paginated: Paginated, tx: &Transactional<'_>)`.

New signature:
```rust
pub async fn list(
    &self,
    search: Query,
    paginated: Paginated,
    tx: &Transactional<'_>,
) -> Result<PaginatedResults<SbomSummary>, AppError>
```

## 3. Find every call site

Use `mcp__serena_backend__find_referencing_symbols(name_path="SbomService/list", relative_path="modules/fundamental/src/sbom/service/sbom.rs")`. As a fallback, grep for `\.list\(` together with `SbomService` / `sbom_service` and `version_filter` across the whole workspace, not only the files in scope. Expected results, matching the Implementation Notes:

| # | Call site | Current call (illustrative) | Updated call | In Files to Modify? |
|---|---|---|---|---|
| 1 | `modules/fundamental/src/sbom/endpoints/list.rs` | `service.list(search, paginated, &params.version, &tx)` | `service.list(search, paginated, &tx)` | Yes |
| 2 | `modules/search/src/service/mod.rs` | `sbom_service.list(search, paginated, "", &tx)` | `sbom_service.list(search, paginated, &tx)` | **No (flag)** |
| 3 | `tests/api/sbom.rs` (several calls) | `service.list(q, p, "1.0", &tx)` / `list(q, p, "", &tx)` | `service.list(q, p, &tx)` | Yes |

If `find_referencing_symbols` finds callers beyond these 3, each one would be updated the same way and listed for scope approval.

## 4. Changes at each call site

### Call site 1: endpoint handler (`list.rs`)
- Drop the argument from the call.
- The `version` value then has no use in the handler, which is the same dead-value problem one level up. Remove the `version` field from the query-param struct (or the separate `Query<...>` extractor) and its `utoipa` `IntoParams` / `params(...)` entry. This satisfies AC2 ("`version` query parameter is no longer extracted or accepted") and keeps the OpenAPI spec accurate.
- Remove imports that become unused.

### Call site 2: search service (`modules/search/src/service/mod.rs`)
- One-line change: remove the `""` argument. Behaviour stays the same, because an empty filter already meant "no version filtering".
- **Scope handling:** this file is not in Files to Modify. AC3 ("All call sites compile and pass without the version_filter argument") requires the change, and without it the workspace does not compile. Following the skill, I would make the minimal edit and then flag it in the Step 9 scope containment check, with an explanation, for explicit user approval before committing. It would also be noted as a deviation in the PR description and the Jira comment.

### Call site 3: integration tests (`tests/api/sbom.rs`)
- Delete `test_list_sboms_version_filtered`. The behaviour it tested no longer exists, and keeping it with the argument removed would make it a duplicate of the plain list test.
- In every other test, remove only the version argument (`""` / `"..."`). Leave assertions unchanged so Test Requirement 2 ("other SBOM list tests still pass without changes") holds for the test logic.
- Check whether any test helper in this file takes a `version` argument only to forward it to `list`. If so, it is also dead, so remove it there and from its callers.

## 5. Cascading cleanup (dead code beyond the parameter)
- `VersionMatches`: run `search_for_pattern("VersionMatches")`. If its only consumer was `SbomService::list`, it is now dead code. If it is defined in an in-scope file, remove it. If it is defined elsewhere (for example `common/src/db/query.rs`), flag it to the user instead of deleting it, because that file is out of scope.
- Unused `use` statements in `sbom.rs` and `list.rs`: remove them. `cargo clippy -- -D warnings` would catch them.
- Docs: if `docs/api.md` or the OpenAPI spec documents `?version=` on `GET /api/v2/sbom`, update it (after scope approval) or regenerate it with the OpenAPI command from CONVENTIONS.md.

## 6. Verification
1. `grep -rn "version_filter" .` returns 0 matches. Also check there is no `_version_filter`.
2. Run every CI command from CONVENTIONS.md (fmt, clippy, check, and so on). Any non-zero exit is a hard stop.
3. `cargo test -p <crate>` for each affected crate, resolved through `cargo metadata`: fundamental, search, and the tests crate. This includes `tests/api/search.rs`, which covers the search service call site.
4. `git diff --name-only`: 3 in-scope files plus `modules/search/src/service/mod.rs` (and any docs), shown to the user for approval before `git commit`.
