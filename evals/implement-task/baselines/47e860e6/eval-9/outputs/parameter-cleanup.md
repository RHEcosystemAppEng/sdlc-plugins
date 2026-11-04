# Dead Parameter Cleanup — TC-9207

## Why there is a dead parameter

The task tells us to remove the `VersionMatches` filter logic from `SbomService::list`. In that body, the filter block was the **only** reference to `version_filter: &str`. Once it is gone, the parameter is unused. rustc would warn `unused variable: version_filter`, and `clippy -D warnings` would fail CI.

## Rule applied (implement-task Step 9, dead parameter detection)

> The correct fix is removal, not renaming.

Ruled out:
- Renaming to `_version_filter`. This silences the warning but keeps a meaningless parameter in the public API.
- `#[allow(unused_variables)]`. Same problem.
- Keeping the parameter "for compatibility". The method is internal to the workspace (inherent `impl SbomService`, not a trait), and we control every caller.

Chosen approach: **remove the parameter from the signature and update every call site.**

## Procedure

1. **Confirm it is dead**: after deleting the filter block, run `mcp__serena_backend__find_symbol("SbomService/list", include_body=true)` and check that `version_filter` no longer appears in the body.
2. **Confirm it is not a trait method**: `list` is defined in an inherent `impl SbomService` block, so there is no trait signature or other implementations to keep in sync.
3. **Change the signature**:
   ```rust
   // before
   pub async fn list(&self, search: Query, paginated: Paginated, version_filter: &str, tx: &Transactional<'_>)
       -> Result<PaginatedResults<SbomSummary>, AppError>
   // after
   pub async fn list(&self, search: Query, paginated: Paginated, tx: &Transactional<'_>)
       -> Result<PaginatedResults<SbomSummary>, AppError>
   ```
4. **Find all call sites**: run `mcp__serena_backend__find_referencing_symbols("SbomService/list", relative_path="modules/fundamental/src/sbom/service/sbom.rs")`, backed up by `search_for_pattern("\.list\(")` and `search_for_pattern("version_filter")` to catch macro- or trait-object-mediated calls that the LSP might miss.
5. **Update each caller** (table below).
6. **Clean up the cascade**: remove anything that only existed to feed the removed argument. That includes the `version` field/extractor in the handler, any local `let version = ...` binding, OpenAPI `params(("version" = ...))` entries, and now-unused `use` imports (`VersionMatches`).
7. **Re-verify**: run `cargo check --workspace --all-targets`, `cargo clippy --all-targets -- -D warnings`, and `cargo test -p` for each affected crate. Then grep for `version_filter` again and expect zero hits.

## Call-site updates

| # | File | Before | After | In Files to Modify? |
|---|---|---|---|---|
| 1 | `modules/fundamental/src/sbom/endpoints/list.rs` | Extracts `version` from the query string; `service.list(search, paginated, &version, &tx)` | `version` field/extractor removed; `service.list(search, paginated, &tx)` | Yes |
| 2 | `modules/search/src/service/mod.rs` | `sbom_service.list(query, paginated, "", tx)` | `sbom_service.list(query, paginated, tx)` | **No**, flag for user approval |
| 3 | `tests/api/sbom.rs` | Calls pass `""`, `"1.0"`, and so on; `test_list_sboms_version_filtered` exists | Version argument dropped from all calls; `test_list_sboms_version_filtered` deleted | Yes |

### Call site 1: endpoint handler
- Delete the `version: Option<String>` field from the query-params struct, or delete the separate extractor and its struct if that struct only held `version`.
- Delete the `version` entry from the `#[utoipa::path(params(...))]` annotation so the generated OpenAPI spec no longer advertises it. Regenerate the spec if CONVENTIONS.md defines a codegen command, and commit the generated file.
- Check whether the query struct uses `#[serde(deny_unknown_fields)]`. If it does not (Axum's default), old clients sending `?version=` are silently ignored, which is the intended compatible behavior. If it does, flag the 400-response behavior change to the user.

### Call site 2: search service (out of scope, so flag it)
- Without this change the workspace will not compile, which fails Acceptance Criterion 3. The Implementation Notes explicitly name it as a call site.
- The change is a single argument removal. It does not change behavior, because `""` already meant "no version filtering".
- Per Step 9 scope containment, I list it as out of scope, explain why, and **ask the user to approve before committing**. I would not leave it out silently, and I would not keep the parameter just to avoid touching the file.

### Call site 3: integration tests
- Delete `test_list_sboms_version_filtered`. The behavior it tested is gone on purpose.
- Remove the version argument from every remaining `list` call. Do not change assertions; those tests must pass as they are.
- Remove any `?version=` query strings from HTTP-level test requests.

## Related follow-ups (reported, not done)
- If `VersionMatches` (likely in `common/src/db/query.rs` or the sbom module) has no remaining users, it is now dead code. Report it as a follow-up, because its file is outside scope.
- If `docs/api.md` / `README.md` document the `version` query parameter on `GET /api/v2/sbom`, flag them for a documentation update (needs approval, since they are out of scope).
